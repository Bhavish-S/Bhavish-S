#!/usr/bin/env python3
"""Render the README's live telemetry cards from the GitHub GraphQL API.

Writes six self-contained SVGs to assets/stats/ (contributions, overview and
languages, each in a dark and a light variant). The cards use only system fonts
and inline CSS so they render inside GitHub's sandboxed <img> tags.

API failures exit non-zero before anything is written, so the last good cards stay.
Run locally against saved data with:  python tools/refresh_stats.py --data fixture.json
"""
import argparse
import datetime as dt
import json
import math
import os
import urllib.request
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'stats'
WIDTH = 900

MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Inter,Roboto,'Helvetica Neue',Arial,sans-serif"

# Obsidian-Emerald palette shared with the editorial section banners.
THEMES = {
    'dark': dict(
        bg='#07131B', bg2='#0B1A22', panel='#0F212B', line='#16323F', grid='#13303D',
        ink='#F1F5F9', muted='#94A3B8', dim='#5B7083', accent='#00E5A8', cyan='#38BDF8', gold='#F59E0B',
        levels=['#173240', '#0B4F3C', '#08805A', '#00B886', '#00E5A8'],
    ),
    'light': dict(
        bg='#FFFFFF', bg2='#F8FAFC', panel='#F8FAFC', line='#E2E8F0', grid='#F1F5F9',
        ink='#0F172A', muted='#64748B', dim='#94A3B8', accent='#059669', cyan='#0284C7', gold='#D97706',
        levels=['#E8EEF3', '#A7F3D0', '#4ADE9B', '#10B981', '#047857'],
    ),
}
LEVELS = ['NONE', 'FIRST_QUARTILE', 'SECOND_QUARTILE', 'THIRD_QUARTILE', 'FOURTH_QUARTILE']


# ───────────────────────────── data ─────────────────────────────

def graphql(query, variables, token):
    request = urllib.request.Request(
        'https://api.github.com/graphql',
        data=json.dumps({'query': query, 'variables': variables}).encode(),
        headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json',
                 'User-Agent': 'profile-telemetry-cards'})
    with urllib.request.urlopen(request, timeout=45) as response:
        result = json.load(response)
    if result.get('errors'):
        raise RuntimeError('GitHub GraphQL request failed: ' + str(result['errors']))
    return result['data']


CALENDAR = 'contributionCalendar{totalContributions weeks{contributionDays{date contributionCount contributionLevel}}}'


def fetch(login, token):
    user = graphql('''query($login:String!){user(login:$login){
        login createdAt
        followers{totalCount}
        repositories(privacy:PUBLIC,ownerAffiliations:OWNER){totalCount}
        repositoriesContributedTo(contributionTypes:[COMMIT,PULL_REQUEST,ISSUE,PULL_REQUEST_REVIEW],includeUserRepositories:false){totalCount}
        pullRequests(states:MERGED){totalCount}
        issues{totalCount}
        contributionsCollection{''' + CALENDAR + '''}
    }}''', {'login': login}, token)['user']
    if not user:
        raise RuntimeError('GitHub account not found')

    # One contribution calendar per calendar year since the account was created.
    first = int(user['createdAt'][:4])
    now = dt.datetime.now(dt.timezone.utc)
    parts = []
    for year in range(first, now.year + 1):
        parts.append(f'y{year}: contributionsCollection(from:"{year}-01-01T00:00:00Z",to:"{year}-12-31T23:59:59Z")'
                     f'{{{CALENDAR}}}')
    years = graphql('query($login:String!){user(login:$login){' + ' '.join(parts) + '}}', {'login': login}, token)['user']
    user['years'] = {key[1:]: value for key, value in years.items()}

    repos, cursor = [], None
    while True:
        page = graphql('''query($login:String!,$cursor:String){user(login:$login){
            repositories(first:100,after:$cursor,privacy:PUBLIC,ownerAffiliations:OWNER,isFork:false){
              nodes{name stargazerCount languages(first:100){edges{size node{name color}}}}
              pageInfo{hasNextPage endCursor}}}}''', {'login': login, 'cursor': cursor}, token)['user']['repositories']
        repos.extend(page['nodes'])
        if not page['pageInfo']['hasNextPage']:
            break
        cursor = page['pageInfo']['endCursor']
    user['publicRepositories'] = repos
    user['generatedAt'] = now.strftime('%Y-%m-%d %H:%M UTC')
    return user


def days_of(calendar):
    return [d for week in calendar['weeks'] for d in week['contributionDays']]


def streaks(data):
    """Current and longest streak across every year fetched, GitHub-style."""
    counts = {}
    for year in data.get('years', {}).values():
        for d in days_of(year['contributionCalendar']):
            counts[d['date']] = d['contributionCount']
    for d in days_of(data['contributionsCollection']['contributionCalendar']):
        counts[d['date']] = d['contributionCount']
    today = data['generatedAt'][:10]
    dates = sorted(d for d in counts if d <= today)
    if not dates:
        return (0, None, None), (0, None, None)
    best, run, start = (0, None, None), 0, None
    for date in dates:
        if counts[date] > 0:
            if run == 0:
                start = date
            run += 1
            if run > best[0]:
                best = (run, start, date)
        else:
            run = 0
    # Current streak: an empty "today" does not break it yet.
    idx = len(dates) - 1
    if counts[dates[idx]] == 0:
        idx -= 1
    end = dates[idx] if idx >= 0 else None
    cur = 0
    while idx >= 0 and counts[dates[idx]] > 0:
        cur += 1
        idx -= 1
    return (cur, dates[idx + 1] if cur else None, end if cur else None), best


# ───────────────────────────── svg helpers ─────────────────────────────

def t(x, y, value, size=13, fill='#000', weight=400, font=SANS, anchor='start', extra=''):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{font}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}" {extra}>{escape(str(value))}</text>')


def shade(hex_color, factor):
    hex_color = hex_color.lstrip('#')
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
    return '#%02X%02X%02X' % tuple(max(0, min(255, round(v * factor))) for v in (r, g, b))


def luminance(hex_color):
    hex_color = hex_color.lstrip('#')
    r, g, b = (int(hex_color[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def fmt_date(iso):
    return dt.date.fromisoformat(iso).strftime('%b %d').upper() if iso else '—'


def fmt_bytes(n):
    return f'{n / 1_048_576:.1f} MB' if n >= 1_048_576 else f'{max(1, round(n / 1024))} KB'


def frame(c, height, label, meta, body, title, desc):
    style = (
        '<style>'
        '.in{opacity:0;animation:in .7s cubic-bezier(.2,.7,.2,1) forwards}'
        '@keyframes in{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}'
        '.pop{opacity:0;animation:pop .5s ease-out forwards}'
        '@keyframes pop{to{opacity:1}}'
        '.draw{stroke-dasharray:1200;stroke-dashoffset:1200;animation:draw 1.6s cubic-bezier(.6,0,.2,1) .4s forwards}'
        '@keyframes draw{to{stroke-dashoffset:0}}'
        '.pulse{animation:pulse 2.4s ease-in-out infinite}'
        '@keyframes pulse{0%,100%{opacity:1}50%{opacity:.35}}'
        '@media (prefers-reduced-motion:reduce){.in,.pop,.draw{animation:none;opacity:1;stroke-dashoffset:0}.pulse{animation:none}}'
        '</style>'
    )
    defs = (
        f'<defs><pattern id="g" width="24" height="24" patternUnits="userSpaceOnUse">'
        f'<path d="M24 0H0V24" fill="none" stroke="{c["grid"]}" stroke-opacity=".55"/></pattern>'
        f'<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c["bg2"]}"/>'
        f'<stop offset="1" stop-color="{c["bg"]}"/></linearGradient>'
        f'<linearGradient id="acc" x1="0" x2="1"><stop offset="0" stop-color="{c["accent"]}"/>'
        f'<stop offset="1" stop-color="{c["cyan"]}"/></linearGradient></defs>'
    )
    chrome = (
        f'<rect x=".5" y=".5" width="{WIDTH - 1}" height="{height - 1}" rx="14" fill="url(#bg)" stroke="{c["line"]}"/>'
        f'<rect x=".5" y=".5" width="{WIDTH - 1}" height="{height - 1}" rx="14" fill="url(#g)"/>'
        f'<path d="M28 1.2H248" stroke="url(#acc)" stroke-width="2.4" stroke-linecap="round"/>'
        f'<circle class="pulse" cx="33" cy="33" r="4" fill="{c["accent"]}"/>'
        + t(46, 37.5, label, 11.5, c['accent'], 700, MONO, extra='letter-spacing="3"')
        + t(WIDTH - 28, 37.5, meta, 10.5, c['muted'], 600, MONO, 'end', 'letter-spacing="1.6"')
    )
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" viewBox="0 0 {WIDTH} {height}" '
            f'role="img" aria-labelledby="t d"><title id="t">{escape(title)}</title><desc id="d">{escape(desc)}</desc>'
            f'{style}{defs}{chrome}{body}</svg>\n')


def tile(c, x, y, w, h, label, value, unit='', sub='', delay=0.0, value_size=30):
    out = f'<g class="in" style="animation-delay:{delay:.2f}s">'
    out += f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="10" fill="{c["panel"]}" stroke="{c["line"]}"/>'
    out += t(x + 16, y + 24, label, 11.5, c['muted'], 600)
    out += t(x + 16, y + 24 + value_size + 6, value, value_size, c['ink'], 800)
    if unit:
        width = len(str(value)) * value_size * 0.6
        out += t(x + 22 + width, y + 24 + value_size + 6, unit[:-1] if str(value) == '1' and unit.endswith('s') else unit, 12.5, c['muted'], 600)
    if sub:
        out += t(x + 16, y + h - 14, sub, 9.5, c['dim'], 600, MONO, extra='letter-spacing="1.2"')
    return out + '</g>'


# ───────────────────────────── cards ─────────────────────────────

def contributions_card(data, c):
    calendar = data['contributionsCollection']['contributionCalendar']
    weeks = calendar['weeks']
    total = calendar['totalContributions']
    all_days = days_of(calendar)
    peak = max(all_days, key=lambda d: d['contributionCount'], default=None)
    peak_n = peak['contributionCount'] if peak else 0
    (cur, cs, ce), (best, bs, be) = streaks(data)
    active = sum(1 for d in all_days if d['contributionCount'])
    height = 550

    body = ''
    tw = (WIDTH - 56 - 2 * 14) / 3
    body += tile(c, 28, 58, tw, 92, 'Current streak', cur, 'days',
                 f'{fmt_date(cs)} → {fmt_date(ce)}' if cur else 'NEXT COMMIT STARTS IT', .05)
    body += tile(c, 28 + tw + 14, 58, tw, 92, 'Longest streak', best, 'days',
                 f'{fmt_date(bs)} → {fmt_date(be)}' if best else '—', .15)
    body += tile(c, 28 + 2 * (tw + 14), 58, tw, 92, 'Contributions · past 12 months', f'{total:,}', '',
                 f'{total / max(1, len(all_days)):.1f}/DAY · {active} ACTIVE DAYS', .25)

    # Isometric contribution city: weeks run along u, weekdays along v.
    ux, uy, vx, vy = 12.2, 4.3, -6.6, 5.4
    ox = WIDTH / 2 - (len(weeks) * ux + 7 * vx) / 2
    oy = 236
    max_h = 76

    def P(w, d):
        return ox + w * ux + d * vx, oy + w * uy + d * vy

    def pts(*ps):
        return ' '.join(f'{x:.1f},{y:.1f}' for x, y in ps)

    # Board slab with a little thickness.
    p0, p1, p2, p3 = P(0, 0), P(len(weeks), 0), P(len(weeks), 7), P(0, 7)
    drop = lambda p: (p[0], p[1] + 7)
    body += f'<polygon points="{pts(p3, p2, drop(p2), drop(p3))}" fill="{shade(c["levels"][0], .72)}"/>'
    body += f'<polygon points="{pts(p1, p2, drop(p2), drop(p1))}" fill="{shade(c["levels"][0], .55)}"/>'
    body += f'<polygon points="{pts(p0, p1, p2, p3)}" fill="{shade(c["levels"][0], .88)}" stroke="{c["line"]}" stroke-width=".8"/>'

    cells = []
    for w, week in enumerate(weeks):
        for day in week['contributionDays']:
            d = (dt.date.fromisoformat(day['date']).weekday() + 1) % 7
            cells.append((w, d, day))
    cells.sort(key=lambda item: item[0] * uy + item[1] * vy)

    peak_top = None
    inset = .12
    for w, d, day in cells:
        n = day['contributionCount']
        level = LEVELS.index(day['contributionLevel']) if day['contributionLevel'] in LEVELS else 0
        top = c['levels'][level]
        h = 1.2 if n == 0 else 4 + (max_h - 4) * math.sqrt(n / max(1, peak_n))
        a, b = P(w + inset, d + inset), P(w + 1 - inset, d + inset)
        cc, e = P(w + 1 - inset, d + 1 - inset), P(w + inset, d + 1 - inset)
        A, B, C, E = ((p[0], p[1] - h) for p in (a, b, cc, e))
        g = (f'<g class="pop" style="animation-delay:{.35 + w * .018:.2f}s">'
             f'<title>{day["date"]}: {n} contribution{"" if n == 1 else "s"}</title>')
        if n:
            g += f'<polygon points="{pts(e, cc, C, E)}" fill="{shade(top, .62)}"/>'
            g += f'<polygon points="{pts(b, cc, C, B)}" fill="{shade(top, .45)}"/>'
        g += f'<polygon points="{pts(A, B, C, E)}" fill="{top}"/>'
        body += g + '</g>'
        if peak is day and n:
            peak_top = ((A[0] + C[0]) / 2, (A[1] + C[1]) / 2)

    # Month labels along the front edge, weekday labels at the right end.
    last_month = None
    for w, week in enumerate(weeks):
        first = dt.date.fromisoformat(week['contributionDays'][0]['date'])
        if first.month != last_month:
            last_month = first.month
            if w == 0 and first.day > 21 or w >= len(weeks) - 2:
                continue
            x, y = P(w + .5, 7)
            body += t(x - 4, y + 20, first.strftime('%b'), 10, c['muted'], 600, MONO)
    for d, name in ((1, 'Mon'), (3, 'Wed'), (5, 'Fri')):
        x, y = P(len(weeks), d + .5)
        body += t(x + 10, y + 4, name, 9.5, c['dim'], 600, MONO)

    if peak_top:
        px, py = peak_top
        label_y = max(180, py - 30)
        peak_date = dt.date.fromisoformat(peak['date']).strftime('%b %d').upper()
        anchor = 'end' if px > WIDTH - 140 else 'middle'
        lx = px + 6 if anchor == 'end' else px
        body += (f'<g class="in" style="animation-delay:1.5s"><line x1="{px:.1f}" y1="{py - 3:.1f}" x2="{px:.1f}" y2="{label_y + 6:.1f}" '
                 f'stroke="{c["gold"]}" stroke-width="1.2" stroke-dasharray="2 3"/>'
                 f'<circle cx="{px:.1f}" cy="{py - 3:.1f}" r="2.6" fill="{c["gold"]}"/>'
                 + t(lx, label_y, f'PEAK {peak_n} · {peak_date}', 10.5, c['gold'], 800, MONO, anchor, 'letter-spacing="1.2"')
                 + '</g>')

    fy = height - 26
    body += t(28, fy + 4, 'Less', 10, c['muted'], 600, MONO)
    for i, col in enumerate(c['levels']):
        body += f'<rect x="{62 + i * 15}" y="{fy - 6}" width="11" height="11" rx="2.5" fill="{col}"/>'
    body += t(62 + 5 * 15 + 4, fy + 4, 'More', 10, c['muted'], 600, MONO)
    body += t(WIDTH - 28, fy + 4, f'REFRESHED {data["generatedAt"]}', 10, c['dim'], 600, MONO, 'end', 'letter-spacing="1.2"')

    desc = (f'Contribution activity for {data["login"]}: {total} contributions in the past 12 months, '
            f'current streak {cur} days, longest streak {best} days.')
    return frame(c, height, 'CONTRIBUTIONS', 'PAST 12 MONTHS · 3D ACTIVITY CITY · LIVE', body, 'Contributions', desc)


def overview_card(data, c):
    years = data.get('years', {})
    yearly = {int(y): v['contributionCalendar']['totalContributions'] for y, v in years.items()}
    all_time = sum(yearly.values())
    today = dt.date.fromisoformat(data['generatedAt'][:10])
    ytd = yearly.get(today.year, 0)
    elapsed = today.timetuple().tm_yday
    since = int(data.get('createdAt', str(today.year))[:4])

    monthly, cumulative, run = {}, [], 0
    for y, v in sorted(years.items()):
        for d in days_of(v['contributionCalendar']):
            monthly[d['date'][:7]] = monthly.get(d['date'][:7], 0) + d['contributionCount']
            if d['date'][:4] == str(today.year) and d['date'] <= data['generatedAt'][:10]:
                run += d['contributionCount']
                cumulative.append(run)
    first_active = next((k for k in sorted(monthly) if monthly[k]), None)
    months = [monthly[k] for k in sorted(monthly) if first_active and k >= first_active][-24:]
    calendar = data['contributionsCollection']['contributionCalendar']
    weekly = [sum(d['contributionCount'] for d in w['contributionDays']) for w in calendar['weeks']]
    active = sum(1 for d in days_of(calendar) if d['contributionCount'])

    height = 300
    body = ''
    tw = (WIDTH - 56 - 2 * 14) / 3

    def spark_line(x, y, w, h, series, delay, gid):
        if len(series) < 2 or max(series) == 0:
            return ''
        hi = max(series)
        p = [(x + i * w / (len(series) - 1), y + h - h * v / hi) for i, v in enumerate(series)]
        line = ' '.join(f'{px:.1f},{py:.1f}' for px, py in p)
        area = f'{x:.1f},{y + h:.1f} {line} {x + w:.1f},{y + h:.1f}'
        return (f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">'
                f'<stop offset="0" stop-color="{c["accent"]}" stop-opacity=".3"/>'
                f'<stop offset="1" stop-color="{c["accent"]}" stop-opacity="0"/></linearGradient></defs>'
                f'<polygon class="pop" style="animation-delay:{delay + .6:.2f}s" points="{area}" fill="url(#{gid})"/>'
                f'<polyline class="draw" points="{line}" fill="none" stroke="{c["accent"]}" stroke-width="1.8" '
                f'stroke-linejoin="round" stroke-linecap="round"/>'
                f'<circle class="pop" style="animation-delay:{delay + 1.5:.2f}s" cx="{p[-1][0]:.1f}" cy="{p[-1][1]:.1f}" r="3" fill="{c["accent"]}"/>')

    def spark_bars(x, y, w, h, series, delay, gid):
        if not series or max(series) == 0:
            return ''
        hi, bw = max(series), w / len(series)
        out = ''
        for i, v in enumerate(series):
            bh = max(1.2, h * v / hi)
            out += (f'<rect class="pop" style="animation-delay:{delay + .3 + i * .012:.2f}s" x="{x + i * bw + .6:.1f}" '
                    f'y="{y + h - bh:.1f}" width="{max(1, bw - 1.2):.1f}" height="{bh:.1f}" rx="1" '
                    f'fill="{c["accent"] if v else c["line"]}" fill-opacity="{.35 + .65 * v / hi if v else 1:.2f}"/>')
        return out

    tops = [
        ('Contributions · all time', f'{all_time:,}', '', f'SINCE {since} · MONTHLY TREND', spark_line, months),
        (f'Contributions · {today.year}', f'{ytd:,}', '', f'AVG {ytd / max(1, elapsed):.1f}/DAY · YEAR TO DATE', spark_line, cumulative),
        ('Active days · 12 months', f'{active}', 'days', 'WEEKLY CADENCE', spark_bars, weekly),
    ]
    for i, (label, value, unit, sub, fn, series) in enumerate(tops):
        x = 28 + i * (tw + 14)
        body += tile(c, x, 58, tw, 128, label, value, unit, sub, .05 + i * .1)
        body += fn(x + 16, 118, tw - 32, 36, series, .2 + i * .1, f'sg{i}')

    stars = sum(r['stargazerCount'] for r in data['publicRepositories'])
    langs = {e['node']['name'] for r in data['publicRepositories'] for e in r['languages']['edges']}
    bottoms = [
        ('PRs merged', data.get('pullRequests', {}).get('totalCount', 0), 'AUTHORED'),
        ('Issues opened', data.get('issues', {}).get('totalCount', 0), 'ALL TIME'),
        ('Stars earned', stars, 'FORKS EXCL.'),
        ('Followers', data['followers']['totalCount'], 'GITHUB'),
        ('Public repos', data['repositories']['totalCount'], f'{len(langs)} LANGUAGES'),
        ('Contributed to', data.get('repositoriesContributedTo', {}).get('totalCount', 0), 'OTHER REPOS'),
    ]
    bw = (WIDTH - 56 - 5 * 12) / 6
    for i, (label, value, sub) in enumerate(bottoms):
        body += tile(c, 28 + i * (bw + 12), 200, bw, 82, label, f'{value:,}', '', sub, .35 + i * .06, 24)

    desc = (f'GitHub overview for {data["login"]}: {all_time} contributions all time, {ytd} in {today.year}, '
            f'{stars} stars, {data["followers"]["totalCount"]} followers.')
    meta = f'@{data["login"]} · PUBLIC ACTIVITY'.upper()
    return frame(c, height, 'OVERVIEW', meta, body, 'Overview', desc)


def squarify(items, x, y, w, h):
    """Squarified treemap layout -> list of (item, x, y, w, h)."""
    total = sum(v for _, v in items)
    if not items or total <= 0:
        return []
    areas = [(it, it[1] * w * h / total) for it in items if it[1] > 0]
    out = []

    def worst(row, side):
        s = sum(a for _, a in row)
        return max(max(side * side * a / (s * s), (s * s) / (side * side * a)) for _, a in row)

    while areas:
        side = min(w, h)
        row = [areas.pop(0)]
        while areas and worst(row + [areas[0]], side) <= worst(row, side):
            row.append(areas.pop(0))
        s = sum(a for _, a in row)
        if w >= h:
            cw, cy = s / h, y
            for it, a in row:
                out.append((it, x, cy, cw, a / cw))
                cy += a / cw
            x, w = x + cw, w - cw
        else:
            ch, cx = s / w, x
            for it, a in row:
                out.append((it, cx, y, a / ch, ch))
                cx += a / ch
            y, h = y + ch, h - ch
    return out


def languages_card(data, c):
    sizes, colors, repos = {}, {}, {}
    for repo in data['publicRepositories']:
        for edge in repo['languages']['edges']:
            name = edge['node']['name']
            sizes[name] = sizes.get(name, 0) + edge['size']
            colors[name] = edge['node']['color'] or c['muted']
            repos[name] = repos.get(name, 0) + 1
    ordered = sorted(sizes.items(), key=lambda kv: kv[1], reverse=True)
    total = sum(sizes.values())
    visible = ordered[:8]
    if len(ordered) > 8:
        visible.append(('Other', sum(n for _, n in ordered[8:])))
        colors['Other'] = c['dim']
    height = 360
    body = ''

    if not total:
        body += t(28, 98, 'No public repository language data available yet.', 14, c['muted'])
    for i, (item, x, y, w, h) in enumerate(squarify(visible, 28, 58, 500, height - 58 - 48)):
        name, value = item
        col = colors.get(name, c['muted'])
        ink = '#0F172A' if luminance(col) > .55 else '#FFFFFF'
        body += (f'<g class="in" style="animation-delay:{.1 + i * .08:.2f}s">'
                 f'<title>{escape(name)}: {fmt_bytes(value)} ({100 * value / total:.1f}%)</title>'
                 f'<rect x="{x + 1.5:.1f}" y="{y + 1.5:.1f}" width="{max(0, w - 3):.1f}" height="{max(0, h - 3):.1f}" rx="6" fill="{col}"/>')
        if w > 70 and h > 42:
            body += t(x + 11, y + 22, name, 13 if w > 110 else 11.5, ink, 800)
            body += t(x + 11, y + 38, f'{100 * value / total:.1f}%', 11, ink, 600, MONO, extra='fill-opacity=".85"')
            if h > 64:
                body += t(x + 11, y + 53, fmt_bytes(value), 10, ink, 500, MONO, extra='fill-opacity=".7"')
        body += '</g>'

    lx, right = 556, WIDTH - 28
    head = lambda x, s, a='start': t(x, 72, s, 9.5, c['dim'], 700, MONO, a, 'letter-spacing="1.4"')
    body += head(lx, 'LANGUAGE') + head(lx + 186, 'REPOS', 'end') + head(lx + 252, 'SIZE', 'end') + head(right, 'SHARE', 'end')
    body += f'<line x1="{lx}" y1="82" x2="{right}" y2="82" stroke="{c["line"]}"/>'
    for i, (name, value) in enumerate(visible):
        y = 106 + i * 25
        pct = 100 * value / total
        body += f'<g class="in" style="animation-delay:{.2 + i * .07:.2f}s">'
        body += f'<rect x="{lx}" y="{y - 10}" width="10" height="10" rx="2.5" fill="{colors.get(name, c["muted"])}"/>'
        body += t(lx + 18, y, name, 12.5, c['ink'], 600)
        body += t(lx + 186, y, repos.get(name, '—'), 11.5, c['muted'], 600, MONO, 'end')
        body += t(lx + 252, y, fmt_bytes(value), 11.5, c['muted'], 600, MONO, 'end')
        bx, bwid = lx + 262, 18
        body += f'<rect x="{bx}" y="{y - 6}" width="{bwid}" height="4" rx="2" fill="{c["line"]}"/>'
        body += f'<rect x="{bx}" y="{y - 6}" width="{max(1.5, bwid * pct / 100):.1f}" height="4" rx="2" fill="{c["accent"]}"/>'
        body += t(right, y, f'{pct:.1f}%', 11.5, c['ink'], 700, MONO, 'end')
        body += '</g>'

    n_repos = len(data['publicRepositories'])
    body += t(28, height - 22, f'{len(ordered)} languages · {n_repos} source repositories · {fmt_bytes(total)} of code',
              11, c['muted'], 600)
    body += t(right, height - 22, 'BY BYTES · FORKS EXCLUDED', 10, c['dim'], 600, MONO, 'end', 'letter-spacing="1.2"')
    desc = ('Language breakdown: ' + ', '.join(f'{n} {100 * v / total:.1f}%' for n, v in visible)) if total else 'No language data.'
    return frame(c, height, 'LANGUAGES', 'PUBLIC SOURCE REPOSITORIES · TREEMAP', body, 'Languages', desc)


def render(data):
    out = {}
    for theme, c in THEMES.items():
        out[f'contributions.{theme}.svg'] = contributions_card(data, c)
        out[f'overview.{theme}.svg'] = overview_card(data, c)
        out[f'languages.{theme}.svg'] = languages_card(data, c)
    return out


def main():
    parser = argparse.ArgumentParser(description='Render the README telemetry cards.')
    parser.add_argument('--data', type=Path, help='render from a saved JSON payload instead of the API')
    parser.add_argument('--dump', type=Path, help='also save the fetched payload to this path')
    args = parser.parse_args()
    if args.data:
        data = json.loads(args.data.read_text())
    else:
        token = os.environ.get('METRICS_TOKEN') or os.environ.get('GITHUB_TOKEN')
        if not token:
            raise SystemExit('GITHUB_TOKEN is required; existing cards were not changed.')
        data = fetch(os.environ.get('PROFILE_USERNAME', 'Bhavish-S'), token)
        if args.dump:
            args.dump.write_text(json.dumps(data))
    cards = render(data)
    OUT.mkdir(parents=True, exist_ok=True)
    for name, content in cards.items():
        (OUT / name).write_text(content)
    print(f'Updated {len(cards)} profile cards for {data["login"]} at {data["generatedAt"]}.')


if __name__ == '__main__':
    main()
