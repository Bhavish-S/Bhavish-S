#!/usr/bin/env python3
"""Build the README's static artwork (v2 "Obsidian-Emerald Glass" design system).

Every asset is rendered twice (dark + light) into assets/v2/. SVGs are fully
self-contained: system fonts, inline CSS animation, and embedded JPEG data for
photos/screenshots, so they render inside GitHub's sandboxed <img> tags.

Requires Pillow (for the photo/screenshot embeds):  pip install pillow
Run:  python tools/build_profile_art.py
"""
import base64
import io
import re
import textwrap
from html import escape
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'v2'
SHOTS = ROOT / 'public' / 'images'

SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Inter,Roboto,'Helvetica Neue',Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"

T = {
    'dark': dict(
        bg0='#05090E', bg1='#0A141C', panel='#0B1720', panel2='#0F1F2A', line='#173040', line2='#24485C',
        ink='#F1F5F9', sub='#CBD5E1', muted='#8EA3B5', dim='#5B7083',
        em='#00E5A8', cy='#38BDF8', vi='#A78BFA', am='#F59E0B', ro='#FB7185',
        glow=.20, grid='#11283A', chip='#0D2230', name0='#FFFFFF', name1='#B8FFE9', shade='#05090E',
    ),
    'light': dict(
        bg0='#FFFFFF', bg1='#F5F8FB', panel='#FFFFFF', panel2='#F8FAFC', line='#E2E8F0', line2='#CBD5E1',
        ink='#0F172A', sub='#334155', muted='#64748B', dim='#94A3B8',
        em='#059669', cy='#0284C7', vi='#7C3AED', am='#D97706', ro='#E11D48',
        glow=.10, grid='#EEF2F6', chip='#F1F5F9', name0='#0F172A', name1='#065F46', shade='#FFFFFF',
    ),
}

# 24×24 line icons (stroke-based).
ICON = {
    'globe': 'M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18zM3 12h18M12 3c2.5 2.6 3.8 5.6 3.8 9s-1.3 6.4-3.8 9c-2.5-2.6-3.8-5.6-3.8-9S9.5 5.6 12 3z',
    'doc': 'M7 3h7l5 5v13H7zM14 3v5h5M10 13h6M10 17h6',
    'building': 'M4 21V8l8-5 8 5v13M9 21v-5h6v5M8 11h2M14 11h2M3 21h18',
    'linkedin': 'M4 4h16v16H4zM8 10v6M8 7.2v.01M12 16v-3.5a2 2 0 0 1 4 0V16M12 10v6',
    'mail': 'M3 6h18v12H3zM3 7l9 6 9-6',
    'instagram': 'M7 3h10a4 4 0 0 1 4 4v10a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4V7a4 4 0 0 1 4-4zM12 8.5a3.5 3.5 0 1 0 0 7 3.5 3.5 0 0 0 0-7zM17.2 6.8v.01',
    'shield': 'M12 3l7 3v5c0 4.6-3 8.4-7 10-4-1.6-7-5.4-7-10V6zM9 12l2 2 4-4',
    'bolt': 'M13 3L5 14h6l-1 7 8-11h-6z',
    'code': 'M8 8l-4 4 4 4M16 8l4 4-4 4M14 5l-4 14',
    'cloud': 'M7 18h10a4 4 0 0 0 .6-8A6 6 0 0 0 6 11.3 3.4 3.4 0 0 0 7 18z',
    'terminal': 'M3 5h18v14H3zM7 10l3 2-3 2M12 15h5',
    'user': 'M12 4a4 4 0 1 1 0 8 4 4 0 0 1 0-8zM4 21c0-4 3.6-6 8-6s8 2 8 6',
    'award': 'M12 3a6 6 0 1 1 0 12 6 6 0 0 1 0-12zM8.6 13.8L7 21l5-3 5 3-1.6-7.2',
    'landmark': 'M3 21h18M4 10h16M12 3l9 5H3zM6 10v8M10 10v8M14 10v8M18 10v8',
    'satellite': 'M13 7l3-3 4 4-3 3zM9 11l4-4 4 4-4 4zM5 15l4-4M14 14l-4 4M3 21c0-3.3 2.7-6 6-6',
    'repo': 'M5 5a2 2 0 0 1 2-2h12v15H7a2 2 0 0 0-2 2zM5 20a2 2 0 0 0 2 1h12M9 7h6',
    'star': 'M12 3l2.8 5.7 6.2.9-4.5 4.4 1 6.2L12 17.3 6.5 20.2l1-6.2L3 9.6l6.2-.9z',
    'trophy': 'M8 4h8v5a4 4 0 0 1-8 0zM8 6H5a3 3 0 0 0 3 4M16 6h3a3 3 0 0 1-3 4M12 13v4M8 21h8M10 17h4',
    'arrow': 'M7 17L17 7M8 7h9v9',
    'check': 'M5 12l4 4 10-10',
    'lock': 'M6 11h12v9H6zM8 11V8a4 4 0 0 1 8 0v3',
    'radar': 'M12 12l6-6M12 3a9 9 0 1 0 9 9M12 7a5 5 0 1 0 5 5',
    'paw': 'M8 10a1.6 2 0 1 0 0-4 1.6 2 0 0 0 0 4zM16 10a1.6 2 0 1 0 0-4 1.6 2 0 0 0 0 4zM5 14a1.5 1.8 0 1 0 0-3.6A1.5 1.8 0 0 0 5 14zM19 14a1.5 1.8 0 1 0 0-3.6 1.5 1.8 0 0 0 0 3.6zM12 12c-3 0-5 4-5 6s2 2.5 5 1c3 1.5 5 1 5-1s-2-6-5-6z',
    'grad': 'M2 9l10-5 10 5-10 5zM6 11v5c3 2.5 9 2.5 12 0v-5M22 9v6',
    'brief': 'M3 8h18v12H3zM8 8V5h8v3M3 13h18',
    'flask': 'M9 3h6M10 3v6l-5 9a2 2 0 0 0 1.7 3h10.6a2 2 0 0 0 1.7-3l-5-9V3M7.5 15h9',
    'cpu': 'M7 7h10v10H7zM10 10h4v4h-4zM10 3v4M14 3v4M10 17v4M14 17v4M3 10h4M3 14h4M17 10h4M17 14h4',
    'layers': 'M12 3l9 5-9 5-9-5zM3 13l9 5 9-5M3 17l9 5 9-5',
}

CSS = (
    '<style>'
    '.fi{opacity:0;animation:fi .8s cubic-bezier(.2,.7,.2,1) forwards}'
    '@keyframes fi{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}'
    '.fo{opacity:0;animation:fo .7s ease forwards}@keyframes fo{to{opacity:1}}'
    '.pulse{animation:pulse 2.2s ease-in-out infinite}@keyframes pulse{0%,100%{opacity:1}50%{opacity:.3}}'
    '.ring{transform-box:fill-box;transform-origin:center;animation:ring 2.4s ease-out infinite}'
    '@keyframes ring{0%{transform:scale(.6);opacity:.9}100%{transform:scale(2.4);opacity:0}}'
    '.spin{transform-box:view-box;animation:spin 14s linear infinite}@keyframes spin{to{transform:rotate(360deg)}}'
    '.spinr{transform-box:view-box;animation:spin 22s linear infinite reverse}'
    '.flow{animation:flow 1.6s linear infinite}@keyframes flow{to{stroke-dashoffset:-24}}'
    '.comet{animation:comet 7s linear infinite}@keyframes comet{to{stroke-dashoffset:-3200}}'
    '.sweep{animation:sweep 5.5s ease-in-out infinite}@keyframes sweep{0%{transform:translateX(-420px)}60%,100%{transform:translateX(1400px)}}'
    '.blink{animation:blink 1s steps(1) infinite}@keyframes blink{50%{opacity:0}}'
    '.draw{stroke-dasharray:1400;stroke-dashoffset:1400;animation:draw 2s cubic-bezier(.6,0,.2,1) .3s forwards}'
    '@keyframes draw{to{stroke-dashoffset:0}}'
    '@media (prefers-reduced-motion:reduce){.fi,.fo,.draw{animation:none;opacity:1;stroke-dashoffset:0}'
    '.pulse,.ring,.spin,.spinr,.flow,.comet,.sweep,.blink{animation:none}.ring{opacity:0}}'
    '</style>'
)


# ───────────────────────────── primitives ─────────────────────────────

def t(x, y, s, size=13, fill='#000', weight=400, font=SANS, anchor='start', extra=''):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{font}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}" {extra}>{escape(str(s))}</text>')


def mono(x, y, s, size=11, fill='#000', weight=700, anchor='start', ls=2):
    return t(x, y, s, size, fill, weight, MONO, anchor, f'letter-spacing="{ls}"')


def icon(name, x, y, size=24, stroke='#000', width=1.8):
    k = size / 24
    return (f'<g transform="translate({x:.1f},{y:.1f}) scale({k:.4f})" fill="none" stroke="{stroke}" '
            f'stroke-width="{width / k:.2f}" stroke-linecap="round" stroke-linejoin="round"><path d="{ICON[name]}"/></g>')


def icon_tile(name, x, y, size, color, c, r=None):
    r = size * .28 if r is None else r
    return (f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="{r:.1f}" fill="{color}" fill-opacity=".12" '
            f'stroke="{color}" stroke-opacity=".45"/>' + icon(name, x + size * .25, y + size * .25, size * .5, color))


def chip(x, y, label, color, c, h=22, size=10, pad=10, fill=None):
    w = len(label) * (size * .6 + 1) + pad * 2
    out = (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h}" rx="{h / 2:.1f}" fill="{fill or color}" '
           f'fill-opacity="{1 if fill else .1}" stroke="{color}" stroke-opacity=".4"/>'
           + mono(x + w / 2, y + h / 2 + size * .36, label, size, color, 700, 'middle', 1))
    return out, w


def defs(c, uid=''):
    return (
        f'<defs>'
        f'<linearGradient id="bg{uid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c["bg1"]}"/><stop offset="1" stop-color="{c["bg0"]}"/></linearGradient>'
        f'<linearGradient id="acc{uid}" x1="0" x2="1"><stop offset="0" stop-color="{c["em"]}"/><stop offset=".55" stop-color="{c["cy"]}"/><stop offset="1" stop-color="{c["vi"]}"/></linearGradient>'
        f'<linearGradient id="edge{uid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c["em"]}" stop-opacity=".55"/>'
        f'<stop offset=".35" stop-color="{c["line"]}"/><stop offset=".7" stop-color="{c["line"]}"/><stop offset="1" stop-color="{c["cy"]}" stop-opacity=".45"/></linearGradient>'
        f'<linearGradient id="shine{uid}" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity="{.06 if c is T["dark"] else .5}"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
        f'<radialGradient id="ge{uid}"><stop offset="0" stop-color="{c["em"]}" stop-opacity="{c["glow"]}"/><stop offset="1" stop-color="{c["em"]}" stop-opacity="0"/></radialGradient>'
        f'<radialGradient id="gc{uid}"><stop offset="0" stop-color="{c["cy"]}" stop-opacity="{c["glow"]}"/><stop offset="1" stop-color="{c["cy"]}" stop-opacity="0"/></radialGradient>'
        f'<radialGradient id="gv{uid}"><stop offset="0" stop-color="{c["vi"]}" stop-opacity="{c["glow"] * .8}"/><stop offset="1" stop-color="{c["vi"]}" stop-opacity="0"/></radialGradient>'
        f'<radialGradient id="ga{uid}"><stop offset="0" stop-color="{c["am"]}" stop-opacity="{c["glow"]}"/><stop offset="1" stop-color="{c["am"]}" stop-opacity="0"/></radialGradient>'
        f'<pattern id="grid{uid}" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" fill="none" stroke="{c["grid"]}" stroke-width="1"/></pattern>'
        f'<pattern id="dots{uid}" width="16" height="16" patternUnits="userSpaceOnUse"><circle cx="1.5" cy="1.5" r="1" fill="{c["grid"]}"/></pattern>'
        f'</defs>'
    )


def shell(c, w, h, r=18, grid='grid', glows=(), sweep=True, comet=False, uid=''):
    out = defs(c, uid)
    out += f'<clipPath id="clip{uid}"><rect width="{w}" height="{h}" rx="{r}"/></clipPath><g clip-path="url(#clip{uid})">'
    out += f'<rect width="{w}" height="{h}" fill="url(#bg{uid})"/>'
    if grid:
        out += f'<rect width="{w}" height="{h}" fill="url(#{grid}{uid})" opacity=".9"/>'
    for gid, cx, cy, rr in glows:
        out += f'<circle cx="{cx}" cy="{cy}" r="{rr}" fill="url(#{gid}{uid})"/>'
    if sweep:
        out += f'<rect class="sweep" x="0" y="0" width="300" height="{h}" fill="url(#shine{uid})" transform="skewX(-18)"/>'
    out += '</g>'
    out += f'<rect x=".75" y=".75" width="{w - 1.5}" height="{h - 1.5}" rx="{r}" fill="none" stroke="url(#edge{uid})" stroke-width="1.5"/>'
    if comet:
        per = 2 * (w + h)
        out += (f'<rect class="comet" x=".75" y=".75" width="{w - 1.5}" height="{h - 1.5}" rx="{r}" fill="none" stroke="url(#acc{uid})" '
                f'stroke-width="2" stroke-linecap="round" stroke-dasharray="160 {per}" />')
    return out


def svg(w, h, label, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label)}"><title>{escape(label)}</title>{CSS}{body}</svg>\n')


def jpeg_data(path, size, crop_top=None, quality=78, circle=False):
    im = Image.open(path).convert('RGB')
    if crop_top:
        w, h = im.size
        im = im.crop((0, 0, w, int(w * crop_top)))
    im = im.resize(size, Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, 'JPEG', quality=quality, optimize=True, progressive=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()


def write(name, theme, content):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f'{name}.{theme}.svg').write_text(content)


# ───────────────────────────── hero ─────────────────────────────

def hero(c, theme):
    W, H = 1000, 440
    b = shell(c, W, H, 22, glows=(('ge', 170, 190, 260), ('gc', 860, 140, 260), ('gv', 640, 440, 240)), comet=True)
    b += f'<g class="fo">' + mono(48, 46, 'BHAVISH S // CYBERSECURITY & AUTOMATION ARCHITECT', 10.5, c['muted'], 700, ls=2.6) + '</g>'
    # status pill
    b += (f'<g class="fo"><rect x="724" y="28" width="230" height="26" rx="13" fill="{c["em"]}" fill-opacity=".1" stroke="{c["em"]}" stroke-opacity=".45"/>'
          f'<circle class="ring" cx="742" cy="41" r="4" fill="{c["em"]}"/><circle cx="742" cy="41" r="4" fill="{c["em"]}"/>'
          + mono(756, 45, 'AVAILABLE // MYSORE, IN', 10.5, c['em'], 800, ls=1.6) + '</g>')
    b += f'<line x1="48" y1="66" x2="952" y2="66" stroke="{c["line"]}"/>'

    b += (f'<defs><linearGradient id="nm" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c["name0"]}"/>'
          f'<stop offset="1" stop-color="{c["name1"]}"/></linearGradient></defs>')
    # name + roles
    b += (f'<g class="fi" style="animation-delay:.15s"><text x="46" y="160" font-family="{SANS}" font-size="80" font-weight="800" '
          f'letter-spacing="-2.5" fill="url(#nm)">Bhavish S<tspan fill="{c["em"]}">.</tspan></text></g>')
    b += f'<g class="fi" style="animation-delay:.3s">' + t(48, 198, 'Cybersecurity Specialist · Full-Stack Systems Architect', 15.5, c['cy'], 700, MONO) + '</g>'
    b += (f'<g class="fi" style="animation-delay:.45s">' + f'<text x="48" y="226" font-family="{MONO}" font-size="15.5" font-weight="800" fill="{c["ink"]}">CFO, CRO &amp; Security Lead <tspan fill="{c["em"]}">@ Vovalyx</tspan></text></g>')
    x = 48
    for i, (label, col) in enumerate((('ETHICAL HACKING & SIEM', c['em']), ('ZERO-TRUST SAAS & RBAC', c['cy']),
                                      ('VOVALYX SOFTWARE STUDIO', c['am']))):
        g, w = chip(x, 250, label, col, c, 26, 10, 12)
        b += f'<g class="fi" style="animation-delay:{.6 + i * .1:.2f}s">{g}</g>'
        x += w + 10

    # radar
    rx, ry = 894, 146
    b += f'<g class="fo" style="animation-delay:.4s" opacity=".9">'
    for rr in (21, 41, 60):
        b += f'<circle cx="{rx}" cy="{ry}" r="{rr}" fill="none" stroke="{c["line2"]}" stroke-dasharray="3 4"/>'
    b += (f'<line x1="{rx - 60}" y1="{ry}" x2="{rx + 60}" y2="{ry}" stroke="{c["line"]}"/><line x1="{rx}" y1="{ry - 60}" x2="{rx}" y2="{ry + 60}" stroke="{c["line"]}"/>'
          f'<defs><linearGradient id="sw" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{c["em"]}" stop-opacity="0"/><stop offset="1" stop-color="{c["em"]}" stop-opacity=".55"/></linearGradient></defs>'
          f'<g class="spin" style="transform-origin:{rx}px {ry}px;animation-duration:4s"><path d="M{rx} {ry}L{rx + 60} {ry}A60 60 0 0 0 {rx + 42.4} {ry - 42.4}z" fill="url(#sw)"/></g>')
    for bx, by, d in ((rx + 26, ry - 30, 0), (rx - 36, ry + 16, .8), (rx + 16, ry + 38, 1.6)):
        b += f'<circle class="pulse" style="animation-delay:{d}s" cx="{bx}" cy="{by}" r="3.2" fill="{c["em"]}"/>'
    b += f'<circle cx="{rx}" cy="{ry}" r="3" fill="{c["cy"]}"/></g>'
    b += mono(rx, ry + 80, 'THREAT SURFACE // MONITORED', 8.5, c['dim'], 700, 'middle', 1.4)

    # identity rows
    b += f'<line x1="48" y1="300" x2="952" y2="300" stroke="{c["line"]}"/>'
    rows = (('IDENTITY', 'Google-Certified Cybersecurity Student @ MIT Mysore (B.E. CSE) · SIEM & Threat Defense', c['ink']),
            ('IMPACT', "Built Campus-Adopted ERPs (Principal's Letter of Appreciation) · ISRO BAH 2026 Finalist", c['em']),
            ('VENTURE', 'Executive Leadership @ Vovalyx (vovalyx.in) · Universal File Converter (UniConv SaaS) · Zero-Trust RBAC', c['ink']))
    for i, (k, v, col) in enumerate(rows):
        y = 330 + i * 27
        b += (f'<g class="fi" style="animation-delay:{.9 + i * .12:.2f}s">' + mono(48, y, k, 10, c['dim'], 800, ls=2)
              + t(130, y, '▸', 11, c['em'], 700, MONO) + t(150, y, v, 12.5, col, 600, MONO) + '</g>')
    b += f'<line x1="48" y1="402" x2="952" y2="402" stroke="{c["line"]}"/>'
    b += (f'<g class="fo" style="animation-delay:1.3s">' + mono(48, 424, 'SECURITY MINDED. BUILDER BY DESIGN.', 10, c['muted'], 700, ls=2.2)
          + mono(952, 424, 'IAMBHAVISHS.VERCEL.APP ↗', 10.5, c['em'], 800, 'end', 1.6) + '</g>')
    return svg(W, H, 'Bhavish S — Cybersecurity Specialist, Full-Stack Systems Architect, CFO, CRO & Security Lead @ Vovalyx', b)


# ───────────────────────────── section banner ─────────────────────────────

SECTIONS = [
    ('01', 'WHOAMI', 'EXECUTIVE SUMMARY', '~/01-whoami.sh', 'user'),
    ('02', 'THE ROUTE', 'ENGINEERING MILESTONES', '~/02-timeline.sh', 'radar'),
    ('03', 'VENTURE STUDIO', '& PRODUCTION SYSTEMS', '~/03-projects.sh', 'layers'),
    ('04', 'TELEMETRY', 'LIVE ACTIVITY MATRIX', '~/04-telemetry.sh', 'cpu'),
    ('05', 'TECHNICAL ARSENAL', 'PRODUCTION STACK', '~/05-stack.sh', 'terminal'),
    ('06', 'VERIFIED CREDENTIALS', '& ACHIEVEMENTS', '~/06-credentials.sh', 'award'),
    ('07', 'ESTABLISH SECURE LINK', 'CONNECT', '~/07-contact.sh', 'lock'),
]


def banner(c, theme, num, head, tail, node, ic):
    W, H = 1000, 92
    b = shell(c, W, H, 16, grid='dots', glows=(('ge', 60, 46, 160),), comet=False)
    b += f'<rect x="0" y="18" width="4" height="56" rx="2" fill="url(#acc)"/>'
    b += (f'<text x="30" y="62" font-family="{SANS}" font-size="44" font-weight="900" fill="none" stroke="url(#acc)" '
          f'stroke-width="1.4" letter-spacing="-1">{num}</text>')
    b += f'<line x1="104" y1="24" x2="104" y2="68" stroke="{c["line2"]}"/>'
    b += icon_tile(ic, 122, 26, 40, c['em'], c)
    sep = ' // ' if not tail.startswith('&') else ' '
    b += (f'<g class="fi"><text x="180" y="51" font-family="{SANS}" font-size="20" font-weight="800" letter-spacing="2.4" fill="{c["ink"]}">'
          f'{escape(head)}<tspan fill="{c["em"]}">{escape(sep + tail)}</tspan></text></g>')
    b += mono(181, 70, f'NODE: {node}', 9.5, c['muted'], 700, ls=1.4)
    # signal meter + index
    for i in range(7):
        on = i < int(num)
        b += (f'<rect x="{846 + i * 9}" y="{54 - i * 3}" width="5" height="{8 + i * 3}" rx="1.5" fill="{c["em"] if on else c["line2"]}" '
              f'fill-opacity="{.35 + .65 * (i + 1) / 7 if on else 1:.2f}"/>')
    b += mono(970, 36, f'{num} / 07', 10, c['dim'], 800, 'end', 1.6)
    return svg(W, H, f'{num} — {head}{sep}{tail}', b)


# ───────────────────────────── about ─────────────────────────────

def about(c, theme):
    W, H = 1000, 360
    b = ''
    # left card
    b += f'<g>{defs(c, "a")}<rect x=".75" y=".75" width="478" height="{H - 1.5}" rx="18" fill="url(#bga)" stroke="url(#edgea)" stroke-width="1.5"/>'
    b += f'<circle cx="60" cy="40" r="140" fill="url(#gea)"/></g>'
    b += icon_tile('user', 26, 24, 34, c['em'], c) + mono(72, 46, 'BIOGRAPHY & PROVEN IMPACT', 11, c['em'], 800, ls=2.2)
    bio = ['Google-certified cybersecurity engineer & CS student at',
           'Maharaja Institute of Technology, Mysore. Specializing in',
           'SIEM log correlation, penetration testing, and enterprise SaaS.',
           'Serving as CFO, CRO & Security Lead at Vovalyx (vovalyx.in).']
    for i, line in enumerate(bio):
        b += f'<g class="fi" style="animation-delay:{.1 + i * .06:.2f}s">' + t(28, 86 + i * 19, line, 13, c['sub'], 500) + '</g>'
    items = [('Google Cybersecurity Pro', 'Verified Feb 2026', c['em']),
             ('MIT Mysore Appreciation Letter', 'Ref: MITM/2026/128', c['cy']),
             ('ISRO BAH 2026', 'Satellite Road Resilience Platform', c['am']),
             ('CFO, CRO & Security Lead @ Vovalyx', 'Custom Software Studio & Enterprise ERPs', c['vi']),
             ('UniConv & NOC Portal', 'Digitizing Real Institutional Workflows', c['ro'])]
    for i, (head, sub, col) in enumerate(items):
        y = 182 + i * 34
        b += (f'<g class="fi" style="animation-delay:{.4 + i * .1:.2f}s"><circle cx="38" cy="{y}" r="10" fill="{col}" fill-opacity=".14" stroke="{col}" stroke-opacity=".5"/>'
              + icon('check', 32, y - 6, 12, col, 2.4) + t(58, y + 1, head, 13, c['ink'], 700) + t(58, y + 16, sub, 11, c['muted'], 500) + '</g>')

    # terminal
    x0 = 500
    b += f'<g>{defs(c, "b")}<rect x="{x0 + .75}" y=".75" width="{W - x0 - 1.5}" height="{H - 1.5}" rx="18" fill="{"#060B10" if theme == "dark" else "#0B1220"}" stroke="url(#edgeb)" stroke-width="1.5"/></g>'
    b += f'<path d="M{x0 + 18} 44H{W - 18}" stroke="#1E2A36"/>'
    for i, col in enumerate(('#FF5F57', '#FEBC2E', '#28C840')):
        b += f'<circle cx="{x0 + 26 + i * 18}" cy="23" r="5.5" fill="{col}"/>'
    b += t((x0 + W) / 2 + 20, 27, 'bhavish@mitm-node:~$ whoami --verbose', 11, '#8EA3B5', 600, MONO, 'middle')
    lines = [('$ ', 'cat dossier.json', None),
             ('identity', 'Bhavish S', '#F1F5F9'),
             ('education', 'B.E. CSE @ MIT Mysore (VTU)', '#F1F5F9'),
             ('studio', 'CFO, CRO & Security Lead @ Vovalyx', '#FBBF24'),
             ('', '(vovalyx.in)', '#FBBF24'),
             ('focus', 'SIEM, Pentest, SOC, Zero-Trust RBAC', '#38BDF8'),
             ('portfolio', 'iambhavishs.vercel.app', '#A78BFA'),
             ('status', 'Active // Building enterprise security', '#00E5A8')]
    y = 76
    for i, (k, v, col) in enumerate(lines):
        g = f'<g class="fo" style="animation-delay:{.3 + i * .22:.2f}s">'
        if k == '$ ':
            g += t(x0 + 24, y, 'bhavish@mitm-node', 12.5, '#00E5A8', 700, MONO) + t(x0 + 24 + 17 * 7.6, y, ':~$', 12.5, '#38BDF8', 700, MONO)
            g += t(x0 + 24 + 21 * 7.6, y, v, 12.5, '#F1F5F9', 600, MONO)
        else:
            if k:
                g += t(x0 + 24, y, '"' + k + '"', 12.5, '#7DD3FC', 600, MONO) + t(x0 + 140, y, ':', 12.5, '#5B7083', 600, MONO)
            g += t(x0 + 156, y, v, 12.5, col, 600, MONO)
        b += g + '</g>'
        y += 26 if i == 0 else 23
    b += (f'<g class="fo" style="animation-delay:2.2s"><rect class="blink" x="{x0 + 156 + 38 * 7.55}" y="{y - 39}" width="8" height="15" fill="#00E5A8"/></g>')
    b += (f'<g class="fo" style="animation-delay:2.4s"><rect x="{x0 + 22}" y="{H - 66}" width="{W - x0 - 44}" height="44" rx="10" fill="#00E5A8" fill-opacity=".06" stroke="#00E5A8" stroke-opacity=".35" stroke-dasharray="4 4"/>'
          + icon('lock', x0 + 36, H - 56, 22, '#00E5A8', 2)
          + t(x0 + 68, H - 46, 'HARDENED NODE // VTU & VOVALYX', 11, '#00E5A8', 800, MONO, extra='letter-spacing="1.4"')
          + t(x0 + 68, H - 30, 'Verified Certificate: Coursera I4I0BFTGQ6G2', 10.5, '#8EA3B5', 600, MONO) + '</g>')
    return svg(W, H, 'Biography and terminal dossier for Bhavish S', b)


# ───────────────────────────── timeline ─────────────────────────────

def timeline(c, theme):
    W, H = 1000, 270
    b = shell(c, W, H, 18, glows=(('ge', 120, 135, 220), ('gv', 880, 135, 220)))
    b += mono(30, 34, 'THE ROUTE SO FAR // VERIFIED MILESTONES', 10.5, c['muted'], 800, ls=2.6)
    b += mono(970, 34, '~/02-timeline.sh', 10.5, c['em'], 800, 'end', 1.2)
    steps = [('2022', 'First Commit', 'CS & Linux Ops', c['sub']),
             ('2023', 'MIT Mysore', 'B.E. Computer Science', c['cy']),
             ('2024', 'Google Certified', 'Cybersecurity Pro', c['em']),
             ('2025', 'Vovalyx', 'Principal Letter of Appreciation', c['am']),
             ('2026', 'ISRO BAH 2026', 'National Finalist', c['vi']),
             ('NOW', 'Available', 'Open to Roles', c['em'])]
    y0 = 148
    x_at = lambda i: 96 + i * 161.6
    b += f'<line x1="60" y1="{y0}" x2="940" y2="{y0}" stroke="{c["line2"]}" stroke-width="2"/>'
    b += f'<line class="draw" x1="60" y1="{y0}" x2="940" y2="{y0}" stroke="url(#acc)" stroke-width="2.5"/>'
    b += f'<line class="flow" x1="60" y1="{y0}" x2="940" y2="{y0}" stroke="{c["ink"]}" stroke-opacity=".35" stroke-width="1" stroke-dasharray="2 10"/>'
    for i, (yr, head, sub, col) in enumerate(steps):
        x = x_at(i)
        up = i % 2 == 0
        cy = y0 - 86 if up else y0 + 22
        d = .4 + i * .18
        b += f'<g class="fi" style="animation-delay:{d:.2f}s">'
        b += f'<line x1="{x}" y1="{y0 - 10 if up else y0 + 10}" x2="{x}" y2="{cy + 64 if up else cy}" stroke="{col}" stroke-opacity=".6" stroke-dasharray="2 3"/>'
        b += f'<rect x="{x - 77}" y="{cy}" width="154" height="64" rx="12" fill="{c["panel"]}" fill-opacity=".92" stroke="{col}" stroke-opacity=".45"/>'
        b += mono(x, cy + 19, yr, 11, col, 900, 'middle', 2.4)
        b += t(x, cy + 38, head, 13, c['ink'], 800, anchor='middle')
        b += t(x, cy + 54, sub, 9.6 if len(sub) > 24 else 11, c['muted'], 600, anchor='middle')
        b += '</g>'
        if yr == 'NOW':
            b += f'<circle class="ring" cx="{x}" cy="{y0}" r="7" fill="{col}"/>'
        b += (f'<circle cx="{x}" cy="{y0}" r="9" fill="{c["bg0"]}" stroke="{col}" stroke-width="2.5"/>'
              f'<circle cx="{x}" cy="{y0}" r="3.5" fill="{col}"/>')
    return svg(W, H, 'Engineering milestones timeline 2022 to now', b)


# ───────────────────────────── Vovalyx studio ─────────────────────────────

def studio(c, theme):
    W, H = 1000, 200
    b = shell(c, W, H, 18, glows=(('ga', 120, 40, 300), ('gc', 900, 200, 240)), comet=True)
    b += f'<rect x="0" y="26" width="4" height="148" rx="2" fill="{c["am"]}"/>'
    b += icon_tile('building', 30, 30, 46, c['am'], c)
    b += mono(92, 48, 'VENTURE // CUSTOM SOFTWARE DEVELOPMENT', 10.5, c['am'], 800, ls=2.4)
    b += (f'<g class="fi"><text x="92" y="82" font-family="{SANS}" font-size="30" font-weight="900" letter-spacing="-.5" fill="{c["ink"]}">'
          f'VOVALYX <tspan fill="{c["am"]}">—</tspan> ENGINEER YOUR VISION<tspan fill="{c["em"]}">.</tspan></text></g>')
    b += t(32, 122, 'Custom software development studio building web apps, ERP systems, mobile apps, and automation platforms.', 13.5, c['sub'], 500)
    b += (f'<text x="32" y="146" font-family="{SANS}" font-size="12.5" font-weight="500" fill="{c["muted"]}">Executive Role: '
          f'<tspan fill="{c["em"]}" font-weight="800">CFO, CRO &amp; Security Lead</tspan> — Threat Hardening, Financial Governance &amp; Scale.</text>')
    for i, (v, k, col) in enumerate((('06+', 'ENGINEERS', c['em']), ('100%', 'INDEPENDENT', c['cy']))):
        x = 760 + i * 106
        b += (f'<g class="fi" style="animation-delay:{.3 + i * .1:.2f}s"><rect x="{x}" y="26" width="96" height="62" rx="12" fill="{c["panel"]}" stroke="{col}" stroke-opacity=".45"/>'
              + t(x + 48, 60, v, 22, col, 900, anchor='middle') + mono(x + 48, 77, k, 8.5, c['muted'], 800, 'middle', 1.4) + '</g>')
    b += (f'<defs><linearGradient id="cta" x1="0" x2="1"><stop offset="0" stop-color="#F59E0B"/><stop offset="1" stop-color="#FBBF24"/></linearGradient></defs>'
          f'<g class="fi" style="animation-delay:.5s"><rect x="760" y="104" width="202" height="44" rx="12" fill="url(#cta)"/>'
          + mono(861, 131, 'VISIT VOVALYX.IN ↗', 12, '#1C1203', 900, 'middle', 1.8) + '</g>')
    b += mono(32, 178, 'WEB APPS  ·  ERP SYSTEMS  ·  MOBILE APPS  ·  AUTOMATION', 9.5, c['dim'], 700, ls=2.2)
    return svg(W, H, 'Vovalyx — Engineer Your Vision. Custom software development studio.', b)


# ───────────────────────────── manifest ─────────────────────────────

MANIFEST = [
    ('UNICONV', 'SAAS FILE CONVERTER', 'Universal browser-based file conversion platform with client-side WebAssembly processing.',
     'Eliminates cloud data leakage with zero server telemetry and 256-bit AES encryption.',
     ['NEXT.JS 14', 'TYPESCRIPT', 'TAILWIND CSS', 'WASM'], 'PRODUCTION', 'em', 'bolt'),
    ('NOC CLEARANCE PORTAL', '', 'Student NOC clearance and workflow automation system with multi-department sign-offs.',
     'Eliminates campus administrative delays with role-based authorization and cryptographic audit logs.',
     ['REACT', 'NODE.JS', 'FIREBASE', 'RBAC'], 'DEPLOYED CAMPUS-WIDE', 'cy', 'shield'),
    ('ACADOPS ERP CLIENT', '', 'Governance-first academic management and examination control system.',
     'Designed with a 10-role permission hierarchy, separation of duties, and audit logging.',
     ['REACT 18', 'TAILWIND', 'VITE', 'SUPABASE'], 'PRODUCTION', 'vi', 'landmark'),
    ('MITM PLACEPRO', '', 'Autonomous campus placement management and recruitment workflow automation.',
     'Automates company drives, student eligibility filtering, and real-time interview telemetry.',
     ['TYPESCRIPT', 'REACT', 'POSTGRESQL', 'TAILWIND'], 'DEPLOYED', 'am', 'brief'),
    ('ROUTE RESILIENCE', 'ISRO BAH 2026', 'Critical infrastructure network resilience modeling using satellite & geospatial data.',
     'Calculates road network vulnerability and suggests resilient routing during extreme weather disruptions.',
     ['PYTHON', 'OSMNX', 'NETWORKX', 'GEOPANDAS'], 'COMPETITION FINALIST', 'ro', 'satellite'),
]


def manifest(c, theme):
    W, row = 1000, 116
    H = 64 + row * len(MANIFEST) + 10
    b = shell(c, W, H, 18, glows=(('ge', 80, 40, 260), ('gv', 920, H, 300)))
    b += icon('terminal', 30, 22, 20, c['em'], 2) + mono(60, 37, 'FEATURED PROJECTS MANIFEST', 11, c['em'], 800, ls=2.6)
    b += mono(970, 37, f'{len(MANIFEST):02d} SYSTEMS // SHIPPED', 10, c['muted'], 800, 'end', 1.6)
    for i, (name, tag, d1, d2, tech, status, ck, ic) in enumerate(MANIFEST):
        col = c[ck]
        y = 58 + i * row
        b += f'<g class="fi" style="animation-delay:{.1 + i * .12:.2f}s">'
        b += f'<rect x="18" y="{y}" width="{W - 36}" height="{row - 10}" rx="14" fill="{c["panel"]}" fill-opacity=".75" stroke="{c["line"]}"/>'
        b += f'<rect x="18" y="{y + 16}" width="3" height="{row - 42}" rx="1.5" fill="{col}"/>'
        b += (f'<text x="40" y="{y + 56}" font-family="{SANS}" font-size="34" font-weight="900" fill="none" stroke="{col}" '
              f'stroke-opacity=".8" stroke-width="1.2">{i + 1:02d}</text>')
        b += icon_tile(ic, 96, y + 16, 30, col, c)
        b += t(138, y + 37, name, 15, c['ink'], 800, extra='letter-spacing="1.2"')
        if tag:
            g, _ = chip(138 + len(name) * 12.4 + 10, y + 23, tag, col, c, 20, 9, 8)
            b += g
        b += t(138, y + 59, d1, 12, c['sub'], 500)
        b += t(138, y + 76, d2, 12, c['muted'], 500)
        sw = len(status) * (9 * .6 + 1) + 20
        g, _ = chip(W - 34 - sw, y + 20, status, col, c, 22, 9, 10)
        b += g
        b += mono(138, y + 96, '  ·  '.join(tech), 9, col, 800, ls=1.4)
        b += '</g>'
    return svg(W, H, 'Featured projects manifest', b)


# ───────────────────────────── project cards with screenshots ─────────────────────────────

PROJECTS = [
    ('uniconv', 'uniconv.png', 'UniConv', 'SAAS // PRODUCTION', 'uniconv-psi.vercel.app', 'bolt', 'em',
     'Universal browser-based file conversion platform.', 'AI watermark removal, PDF table extraction & 256-bit AES encryption.',
     [('REACT', 'em'), ('SUPABASE', 'cy'), ('AI TOOLS', 'vi'), ('256-BIT AES', 'am')], 'LIVE DEMO'),
    ('nodue-portal', 'noc-portal.png', 'NOC Portal', 'EDTECH // INSTITUTION-WIDE', 'noc-portal-self.vercel.app', 'shield', 'cy',
     'Student No-Due Clearance Management System.', '6-stage clearance workflow, HDFC SmartGateway payments, adopted at MIT Mysore.',
     [('NEXT.JS', 'cy'), ('POSTGRESQL', 'em'), ('HDFC GATEWAY', 'am'), ('12+ ROLES', 'vi')], 'LIVE DEMO'),
    ('erp-client', 'acadops.png', 'AcadOps // ERP Client', 'GOVERNANCE // ENTERPRISE', 'erp-client-9lbk.vercel.app', 'landmark', 'vi',
     'Governance-first academic operations and examinations platform.', '10-role RBAC hierarchy, separation-of-duties & immutable audit logging.',
     [('NEXT.JS 16', 'cy'), ('EXPRESS 5', 'em'), ('POSTGRESQL', 'vi'), ('ZERO-TRUST', 'am')], 'LIVE DEMO'),
    ('placepro', 'placepro.png', 'MITM PlacePro', 'EDTECH // CAREERS', 'mitm-placepro.vercel.app', 'brief', 'am',
     'Intelligent Campus Placement Management System.', 'Triple portal (Admin, Student, Company) with automated drive scheduling.',
     [('NEXT.JS 16', 'cy'), ('NESTJS', 'ro'), ('NEON POSTGRES', 'em'), ('JWT', 'vi')], 'LIVE DEMO'),
    ('jnanashodha', 'mrf-rd.png', 'Jnanashodha (ಜ್ಞಾನಶೋಧ)', 'RESEARCH // VTU COMPLIANT', 'mitm-rd.vercel.app', 'flask', 'em',
     'Ph.D Research Admissions & Lifecycle Management Portal.', '8-stage candidate application wizard with 5 tailored governance dashboards.',
     [('REACT', 'cy'), ('TAILWIND CSS', 'em'), ('VTU COMPLIANCE', 'am'), ('5 ROLES', 'vi')], 'LIVE DEMO'),
    ('petcommunity', 'petcommunity.png', 'PetCommunity', 'CONSUMER // PLATFORM', 'vovalyx.in/products.html', 'paw', 'ro',
     'Connect, match & care — one home for pet parents.', 'Intelligent matchmaking, verified vet network & Breed Lab encyclopedia.',
     [('MATCH', 'em'), ('VET NET', 'cy'), ('BREED LAB', 'vi'), ('VOVALYX', 'am')], 'VIEW PRODUCT'),
]


def project_card(c, theme, p, shot):
    slug, _, name, cat, url, ic, ck, d1, d2, tags, cta = p
    col = c[ck]
    W, H = 560, 420
    b = shell(c, W, H, 20, grid='dots', glows=(('ge' if ck in ('em',) else 'gc', 80, 300, 220),), sweep=True, uid='p')
    # browser frame
    fx, fy, fw, fh = 16, 16, W - 32, 236
    b += f'<clipPath id="win"><rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" rx="12"/></clipPath>'
    b += f'<g clip-path="url(#win)"><rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" fill="{c["panel2"]}"/>'
    b += f'<image href="{shot}" x="{fx}" y="{fy + 30}" width="{fw}" height="{fh - 30}" preserveAspectRatio="xMidYMin slice"/>'
    b += (f'<defs><linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset=".68" stop-color="{c["shade"]}" stop-opacity="0"/>'
          f'<stop offset="1" stop-color="{c["shade"]}" stop-opacity=".85"/></linearGradient></defs>'
          f'<rect x="{fx}" y="{fy + 30}" width="{fw}" height="{fh - 30}" fill="url(#fade)"/>')
    bar = '#0E1822' if theme == 'dark' else '#EEF2F6'
    b += f'<rect x="{fx}" y="{fy}" width="{fw}" height="30" fill="{bar}"/><line x1="{fx}" y1="{fy + 30}" x2="{fx + fw}" y2="{fy + 30}" stroke="{c["line"]}"/>'
    for i, dc in enumerate(('#FF5F57', '#FEBC2E', '#28C840')):
        b += f'<circle cx="{fx + 16 + i * 14}" cy="{fy + 15}" r="4.5" fill="{dc}"/>'
    b += (f'<rect x="{fx + 70}" y="{fy + 6}" width="{fw - 140}" height="18" rx="9" fill="{c["bg0"]}" stroke="{c["line"]}"/>'
          + icon('lock', fx + 80, fy + 9.5, 11, c['em'], 2.2) + t(fx + 96, fy + 19, url, 10.5, c['muted'], 600, MONO))
    b += '</g>'
    b += f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" rx="12" fill="none" stroke="{c["line2"]}"/>'
    # live badge on screenshot
    b += (f'<g><rect x="{fx + fw - 74}" y="{fy + 42}" width="62" height="22" rx="11" fill="{c["bg0"]}" fill-opacity=".85" stroke="{c["em"]}" stroke-opacity=".6"/>'
          f'<circle class="pulse" cx="{fx + fw - 61}" cy="{fy + 53}" r="3.5" fill="{c["em"]}"/>' + mono(fx + fw - 52, fy + 57, 'LIVE', 9.5, c['em'], 900, ls=1.6) + '</g>')
    # body
    y = 274
    b += icon_tile(ic, 22, y, 44, col, c)
    b += mono(78, y + 15, cat, 10, col, 800, ls=2)
    b += t(78, y + 39, name, 22, c['ink'], 800, extra='letter-spacing="-.3"')
    b += f'<g transform="translate({W - 50},{y + 4})">' + icon('arrow', 0, 0, 26, col, 2.4) + '</g>'
    b += t(24, y + 70, d1, 13, c['muted'], 500)
    b += t(24, y + 89, d2, 12.5 if len(d2) < 76 else 11.6, c['sub'], 600)
    x = 24
    for label, tk in tags:
        g, w = chip(x, H - 38, label, c[tk], c, 22, 9.5, 9)
        b += g
        x += w + 7
    b += mono(W - 24, H - 22, f'{cta} ↗', 10.5, col, 900, 'end', 1.6)
    return svg(W, H, f'{name} — {d1}', b)


# ───────────────────────────── repository cards ─────────────────────────────

REPOS = [
    ('Route Resilience', 'Satellite Analytics / GIS', 'Satellite road network flood vulnerability modeling, topological graph analysis & dynamic evacuation routing.',
     ['Python', 'GeoPandas', 'NetworkX'], 'ISRO BAH 2026 FINALIST', 'am', 'satellite'),
    ('Claim_Ai', 'InsurTech / AI Engine', 'Intelligent insurance claim triage, OCR document validation & automated policy anomaly detection.',
     ['TypeScript', 'Next.js', 'AI APIs'], 'ACTIVE REPOSITORY', 'cy', 'bolt'),
    ('LeafCure', 'AgriTech / Computer Vision', 'Computer vision plant pathology diagnostic system identifying crop diseases with treatment recommendations.',
     ['JavaScript', 'Python', 'TensorFlow'], 'ACTIVE REPOSITORY', 'em', 'flask'),
    ('Liltwise', 'AI Media Utility', 'Multi-modal text and audio synthesis engine designed for rapid content workflow automation.',
     ['TypeScript', 'React', 'AI APIs'], 'ACTIVE REPOSITORY', 'vi', 'layers'),
    ('Inklly', 'Dev Publishing / CMS', 'High-speed technical blogging and markdown documentation platform.',
     ['TypeScript', 'Tailwind CSS', 'Next.js'], 'ACTIVE REPOSITORY', 'cy', 'doc'),
    ('Budget Allocator', 'FinTech / Analytics', 'Strategic financial modeling and resource allocation engine supporting zero-based budgeting simulations.',
     ['TypeScript', 'React'], 'ACTIVE REPOSITORY', 'am', 'trophy'),
    ('Paws & Polish', 'Booking & Operations SaaS', 'Professional pet grooming management platform with automated booking, service schedules & notifications.',
     ['TypeScript', 'Tailwind CSS'], 'ACTIVE REPOSITORY', 'ro', 'paw'),
    ('SIEM Threat Defense', 'Offensive & SOC Security', 'Syslog correlation rules, alert threshold tuning, automated attack simulation, and incident triage.',
     ['Splunk', 'ELK', 'Python', 'Bash'], 'SECURITY CORE', 'em', 'shield'),
    ('Pentest Toolkit', 'Security Automation', 'Automated vulnerability scanning, network reconnaissance, port enumeration, and payload verification suite.',
     ['Python', 'Nmap', 'Burp Suite'], 'SECURITY CORE', 'ro', 'radar'),
    ('Bhavish-S Portfolio', 'Web Architecture', 'Production codebase for the official interactive portfolio web app (iambhavishs.vercel.app).',
     ['React 19', 'Vite 8', 'Tailwind CSS v4'], 'LIVE PRODUCTION', 'em', 'globe'),
]


def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


def repo_card(c, theme, r):
    name, domain, desc, tech, status, ck, ic = r
    col = c[ck]
    W, H = 480, 174
    b = shell(c, W, H, 16, grid='dots', glows=((('ge' if ck == 'em' else 'gc'), W, 0, 200),), sweep=False, uid='r')
    b += f'<rect x="0" y="22" width="3" height="40" rx="1.5" fill="{col}"/>'
    b += icon_tile(ic, 20, 20, 42, col, c)
    b += t(76, 40, name, 18, c['ink'], 800)
    b += mono(77, 58, domain.upper(), 9, col, 800, ls=1.4)
    b += icon('repo', W - 44, 22, 20, c['dim'], 1.8)
    for i, line in enumerate(textwrap.wrap(desc, 66)[:3]):
        b += t(22, 92 + i * 18, line, 12.5, c['sub'], 500)
    x = 22
    for label in tech:
        g, w = chip(x, H - 40, label.upper(), c['muted'] if theme == 'light' else c['sub'], c, 22, 9, 9, fill=c['chip'])
        b += g
        x += w + 6
    sw = len(status) * (8.5 * .6 + 1) + 18
    g, _ = chip(W - 20 - sw, H - 40, status, col, c, 22, 8.5, 9)
    b += g
    return svg(W, H, f'{name} — {domain}', b)


# ───────────────────────────── arsenal ─────────────────────────────

ARSENAL = [
    ('OFFENSIVE SECURITY & SOC DEFENSE', 'shield', 'ro', ['burp-suite', 'metasploit', 'wireshark', 'kalilinux', 'splunk', 'nmap']),
    ('FULL-STACK SYSTEMS & FRAMEWORKS', 'layers', 'cy', ['react', 'next-js', 'express', 'tailwind', 'vite']),
    ('CORE LANGUAGES & SYSTEMS', 'code', 'em', ['python', 'go', 'typescript', 'javascript', 'bash', 'linux']),
    ('CLOUD, DATABASES & DEVOPS', 'cloud', 'vi', ['postgresql', 'supabase', 'vercel', 'docker', 'git', 'github-actions']),
]


def badge_icon(slug_, theme):
    s = (ROOT / 'assets' / 'badges' / f'{slug_}.{theme}.svg').read_text()
    label = re.search(r'<title>(.*?)</title>', s).group(1)
    g = re.search(r'<g transform="[^"]*">(.*?)</g>', s, re.S).group(1)
    fills = re.findall(r'fill="(#[0-9a-fA-F]{3,6})"', s)
    color = fills[1] if len(fills) > 1 else '#888'
    rgb = [int(color.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4)]
    lum = (0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]) / 255
    if theme == 'dark' and lum < .42:
        color = '#%02X%02X%02X' % tuple(round(v + (255 - v) * .45) for v in rgb)
    return label, g, color


def arsenal(c, theme):
    W, H = 1000, 400
    b = ''
    cw, ch = 491, 192
    for k, (title, ic, ck, items) in enumerate(ARSENAL):
        col = c[ck]
        x0, y0 = (k % 2) * (cw + 18), (k // 2) * (ch + 16)
        uid = f'k{k}'
        b += f'<g transform="translate({x0},{y0})"><g>{shell(c, cw, ch, 16, "dots", ((("g" + ck[0]) if ck in ("em", "vi") else "gc", 0, 0, 220),), False, False, uid)}</g>'
        b += icon_tile(ic, 18, 16, 36, col, c)
        b += mono(66, 33, title, 10.5, c['ink'], 800, ls=1.6)
        b += mono(66, 48, f'{len(items):02d} TOOLS // PRODUCTION-GRADE', 8.5, col, 800, ls=1.4)
        for i, slug_ in enumerate(items):
            label, paths, icol = badge_icon(slug_, theme)
            cx, cy = 18 + (i % 3) * 153, 70 + (i // 3) * 56
            b += (f'<g class="fi" style="animation-delay:{.1 + k * .1 + i * .05:.2f}s"><rect x="{cx}" y="{cy}" width="145" height="46" rx="11" '
                  f'fill="{c["panel2"]}" stroke="{c["line"]}"/>'
                  f'<rect x="{cx + 8}" y="{cy + 8}" width="30" height="30" rx="8" fill="{icol}" fill-opacity=".12"/>'
                  f'<g transform="translate({cx + 14},{cy + 14}) scale(.75)" fill="{icol}">{paths}</g>'
                  + t(cx + 48, cy + 28.5, label, 13, c['ink'], 700) + '</g>')
        b += '</g>'
    return svg(W, H, 'Technical arsenal: offensive security, full-stack, languages, cloud and DevOps', b)


# ───────────────────────────── metrics bar ─────────────────────────────

def metrics(c, theme):
    W, H = 1000, 118
    b = shell(c, W, H, 18, glows=(('ge', 100, 0, 220), ('gc', 900, 118, 220)), comet=True)
    items = [('repo', '50+', 'Repositories', 'em'), ('trophy', '10+', 'Projects Built', 'am'), ('code', '15K+', 'Lines of Code', 'cy'),
             ('bolt', '20+', 'Contributions (Recent)', 'vi'), ('star', '50+', 'Stars Earned', 'am')]
    w = (W - 40 - 4 * 12) / 5
    for i, (ic, v, k, ck) in enumerate(items):
        x = 20 + i * (w + 12)
        col = c[ck]
        b += (f'<g class="fi" style="animation-delay:{.1 + i * .08:.2f}s"><rect x="{x:.1f}" y="18" width="{w:.1f}" height="82" rx="14" fill="{c["panel"]}" stroke="{c["line"]}"/>'
              + icon_tile(ic, x + 16, 37, 44, col, c)
              + t(x + 72, 64, v, 28, c['ink'], 900, extra='letter-spacing="-.5"') + t(x + 73, 83, k, 11 if len(k) < 16 else 9.8, c['muted'], 600) + '</g>')
    return svg(W, H, 'Quick metrics: 50+ repositories, 10+ projects, 15K+ lines of code, 20+ recent contributions, 50+ stars', b)


# ───────────────────────────── credentials ─────────────────────────────

def credentials(c, theme):
    W, H = 1000, 214
    b = shell(c, W, H, 18, glows=(('ge', 160, 214, 260), ('ga', 860, 0, 260)), comet=True)
    b += icon('award', 26, 20, 20, c['am'], 2) + mono(54, 35, 'VERIFIED CREDENTIALS & INSTITUTIONAL RECOGNITION', 10.5, c['em'], 800, ls=2.2)
    b += mono(974, 35, 'CREDENTIAL ID: I4I0BFTGQ6G2 ↗', 10, c['cy'], 800, 'end', 1.4)
    cards = [('shield', 'Google Cybersecurity Pro', 'COMPLETED FEB 11, 2026', 'Coursera Verified Specialization', 'em'),
             ('landmark', "Principal's Appreciation", 'REF: MITM/2026/128', 'Dr. Murali S., Principal, MIT Mysore', 'cy'),
             ('satellite', 'ISRO BAH 2026 Hackathon', 'BHARATIYA ANTARIKSH', 'Satellite Road Network Resilience', 'am')]
    w = (W - 52 - 2 * 14) / 3
    for i, (ic, head, sub, det, ck) in enumerate(cards):
        col = c[ck]
        x = 26 + i * (w + 14)
        b += f'<g class="fi" style="animation-delay:{.15 + i * .12:.2f}s">'
        b += f'<rect x="{x:.1f}" y="54" width="{w:.1f}" height="136" rx="14" fill="{c["panel"]}" stroke="{col}" stroke-opacity=".5"/>'
        b += f'<rect x="{x + 20:.1f}" y="54" width="{w - 40:.1f}" height="3" rx="1.5" fill="{col}"/>'
        # seal
        sx, sy = x + 46, 104
        b += (f'<circle cx="{sx}" cy="{sy}" r="27" fill="{col}" fill-opacity=".1"/>'
              f'<circle cx="{sx}" cy="{sy}" r="27" fill="none" stroke="{col}" stroke-opacity=".6" stroke-dasharray="3 3"/>'
              f'<circle cx="{sx}" cy="{sy}" r="19" fill="{c["panel2"]}" stroke="{col}"/>' + icon(ic, sx - 11, sy - 11, 22, col, 2))
        b += t(x + 86, 96, head, 15, c['ink'], 800)
        b += mono(x + 86, 115, sub, 9.5, col, 800, ls=1.2)
        b += t(x + 86, 133, det, 11.5, c['muted'], 500)
        g, _ = chip(x + 20, 156, '✓ VERIFIED', col, c, 22, 9, 9)
        b += g + '</g>'
    return svg(W, H, 'Verified credentials: Google Cybersecurity Professional, MIT Mysore Principal Letter, ISRO BAH 2026', b)


# ───────────────────────────── connect + pills + footer ─────────────────────────────

CONNECT = [
    ('portfolio', 'globe', 'Portfolio', 'iambhavishs.vercel.app', 'em'),
    ('linkedin', 'linkedin', 'LinkedIn', '@bhavish-s-', 'cy'),
    ('email', 'mail', 'Email', 'x.bhavish.s@gmail.com', 'vi'),
    ('instagram', 'instagram', 'Instagram', '@bhavish_s_', 'ro'),
    ('vovalyx', 'building', 'Vovalyx', 'vovalyx.in', 'am'),
]


def connect_button(c, theme, item):
    key, ic, label, handle, ck = item
    col = c[ck]
    W, H = 236, 68
    b = shell(c, W, H, 16, grid=None, glows=(('g' + ('e' if ck == 'em' else 'c'), 0, 34, 120),), sweep=True, uid='c')
    b += f'<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="16" fill="none" stroke="{col}" stroke-opacity=".55"/>'
    b += icon_tile(ic, 14, 14, 40, col, c, 12)
    b += t(66, 32, label, 15, c['ink'], 800)
    b += t(66, 50, handle, 11.5 if len(handle) < 20 else 10.5, c['muted'], 600, MONO)
    b += icon('arrow', W - 32, 24, 18, col, 2.2)
    return svg(W, H, f'{label} — {handle}', b)


PILLS = [('portfolio', 'globe', 'PORTFOLIO', 'em'), ('resume', 'doc', 'RESUME', 'cy'), ('vovalyx', 'building', 'VOVALYX.IN', 'am'),
         ('linkedin', 'linkedin', 'LINKEDIN', 'cy'), ('email', 'mail', 'EMAIL', 'vi'), ('instagram', 'instagram', 'INSTAGRAM', 'ro')]


def pill(c, theme, item):
    key, ic, label, ck = item
    col = c[ck]
    W, H = int(len(label) * 7.4 + 58), 34
    b = (f'<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="17" fill="{c["panel"]}" stroke="{col}" stroke-opacity=".55"/>'
         f'<circle cx="18" cy="17" r="11" fill="{col}" fill-opacity=".14"/>' + icon(ic, 11, 10, 14, col, 2)
         + mono(36, 21.5, label, 11, c['ink'], 800, ls=1.4))
    return svg(W, H, label, b)


def footer(c, theme):
    W, H = 1000, 210
    b = shell(c, W, H, 20, glows=(('ge', 500, 210, 380), ('gv', 120, 0, 220), ('gc', 880, 0, 220)), comet=True)
    # waveform
    pts = []
    import math
    for i in range(0, 1001, 10):
        y = 168 + 10 * math.sin(i / 38) * math.sin(i / 140)
        pts.append(f'{i},{y:.1f}')
    b += f'<polyline points="{" ".join(pts)}" fill="none" stroke="url(#acc)" stroke-width="1.6" opacity=".55"/>'
    b += f'<polyline class="flow" points="{" ".join(pts)}" fill="none" stroke="{c["em"]}" stroke-width="1.6" stroke-dasharray="6 18" opacity=".9"/>'
    b += t(500, 66, '“', 72, c['em'], 700, "Georgia,'Times New Roman',serif", 'middle', 'opacity=".5"')
    b += (f'<g class="fi" style="animation-delay:.2s"><text x="500" y="96" font-family="{SANS}" font-size="26" font-weight="800" '
          f'text-anchor="middle" fill="{c["ink"]}">Security is not a product, but a <tspan fill="{c["em"]}">process.</tspan></text></g>')
    b += f'<g class="fi" style="animation-delay:.4s">' + t(500, 122, '— Bruce Schneier', 13, c['muted'], 600, anchor='middle') + '</g>'
    b += mono(500, 196, 'BHAVISH S  //  HACK THE PLANET — LEGALLY', 10, c['dim'], 800, 'middle', 3)
    return svg(W, H, 'Security is not a product, but a process. — Bruce Schneier', b)


# ───────────────────────────── main ─────────────────────────────

def main():
    shots = {p[0]: jpeg_data(SHOTS / p[1], (1056, 520), crop_top=520 / 1056, quality=72) for p in PROJECTS}
    for theme, c in T.items():
        write('masthead', theme, hero(c, theme))
        for s in SECTIONS:
            write(f's{s[0]}', theme, banner(c, theme, *s))
        write('about', theme, about(c, theme))
        write('timeline', theme, timeline(c, theme))
        write('studio', theme, studio(c, theme))
        write('manifest', theme, manifest(c, theme))
        for p in PROJECTS:
            write(f'project-{p[0]}', theme, project_card(c, theme, p, shots[p[0]]))
        for r in REPOS:
            write(f'repo-{slug(r[0])}', theme, repo_card(c, theme, r))
        write('arsenal', theme, arsenal(c, theme))
        write('metrics', theme, metrics(c, theme))
        write('credentials', theme, credentials(c, theme))
        for item in CONNECT:
            write(f'connect-{item[0]}', theme, connect_button(c, theme, item))
        for item in PILLS:
            write(f'pill-{item[0]}', theme, pill(c, theme, item))
        write('footer', theme, footer(c, theme))
    n = len(list(OUT.glob('*.svg')))
    print(f'Wrote {n} SVGs to {OUT.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
