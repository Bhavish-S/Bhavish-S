#!/usr/bin/env python3
"""Build GitHub-safe profile artwork; no external fonts, scripts or image services."""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/design'
THEMES = {
    'dark': dict(bg='#0d1418', panel='#131e23', ink='#f0f6f2', muted='#9bb0ab', line='#294039', accent='#89e9b5', faint='#1b302a'),
    'light': dict(bg='#f4f8f5', panel='#ffffff', ink='#162e26', muted='#516b61', line='#cbded1', accent='#18734d', faint='#e3efe7'),
}

def text(x, y, value, size=14, color=None, weight=400, mono=False, extra=''):
    font = 'ui-monospace,Consolas,monospace' if mono else 'Arial,Helvetica,sans-serif'
    return f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" fill="{color}" {extra}>{escape(value)}</text>'

def svg(width, height, title, body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title"><title id="title">{escape(title)}</title>{body}</svg>\n'

def generate():
    OUT.mkdir(parents=True, exist_ok=True)
    for theme, c in THEMES.items():
        b = f'<rect x=".5" y=".5" width="1119" height="379" rx="16" fill="{c["bg"]}" stroke="{c["line"]}"/>'
        b += f'<path d="M32 62H1088M32 316H1088" stroke="{c["line"]}"/>'
        b += f'<circle cx="37" cy="34" r="4" fill="{c["accent"]}"/>'
        b += text(51, 39, 'BHAVISH-S / THE LEGAL HACKER', 12, c['muted'], mono=True, extra='letter-spacing="1.7"')
        b += text(1084, 39, 'INDIA / B.TECH CSE', 12, c['muted'], mono=True, extra='text-anchor="end"')
        b += text(38, 114, 'CYBERSECURITY · ENGINEERING · AUTOMATION', 13, c['accent'], mono=True, extra='letter-spacing="1.3"')
        b += text(32, 212, 'Bhavish S', 90, c['ink'], 700, extra='letter-spacing="-5"')
        b += text(39, 255, 'Ethical Hacker · Pen Tester · SOC Analyst', 20, c['muted'])
        b += text(39, 284, 'Security Engineer', 20, c['muted'])
        b += text(39, 351, 'Break it to understand it. Then make it unbreakable.', 17, c['ink'])
        b += text(1084, 351, 'OPEN TO COLLABORATION ↗', 12, c['accent'], mono=True, extra='text-anchor="end"')
        # Quiet orbital illustration, with a legible static state and reduced-motion support.
        b += '<style>@media(prefers-reduced-motion:no-preference){.orbit{animation:orbit 36s linear infinite;transform-origin:900px 190px}}@keyframes orbit{to{transform:rotate(360deg)}}</style>'
        b += f'<g fill="none" stroke="{c["line"]}"><circle cx="900" cy="190" r="107"/><circle cx="900" cy="190" r="77"/><circle cx="900" cy="190" r="48"/><path d="M770 190H1030M900 80V300" stroke-dasharray="2 7"/></g>'
        b += f'<g class="orbit"><ellipse cx="900" cy="190" rx="136" ry="49" transform="rotate(-38 900 190)" fill="none" stroke="{c["accent"]}" stroke-opacity=".65"/><circle cx="1007" cy="128" r="5" fill="{c["accent"]}"/></g>'
        b += f'<path d="M900 147L929 159V189Q929 218 900 232Q871 218 871 189V159Z" fill="{c["panel"]}" stroke="{c["accent"]}" stroke-width="1.5"/><path d="M886 188L896 198L916 175" fill="none" stroke="{c["accent"]}" stroke-width="2.5"/>'
        (OUT / f'hero.{theme}.svg').write_text(svg(1120, 380, 'Bhavish S — Ethical Hacker · Pen Tester · SOC Analyst · Security Engineer', b))
        mobile = f'<rect x=".5" y=".5" width="639" height="339" rx="16" fill="{c["bg"]}" stroke="{c["line"]}"/>'
        mobile += text(28, 40, 'BHAVISH-S / THE LEGAL HACKER', 14, c['accent'], mono=True)
        mobile += f'<path d="M28 61H612" stroke="{c["line"]}"/>'
        mobile += text(28, 145, 'Bhavish S', 76, c['ink'], 700, extra='letter-spacing="-4"')
        mobile += text(28, 185, 'Ethical Hacker · Pen Tester · SOC Analyst', 19, c['muted'])
        mobile += text(28, 215, 'Security Engineer', 19, c['muted'])
        mobile += text(28, 270, 'Break it to understand it.', 20, c['ink'])
        mobile += text(28, 299, 'Then make it unbreakable.', 20, c['ink'])
        (OUT / f'hero-mobile.{theme}.svg').write_text(svg(640, 340, 'Bhavish S — The Legal Hacker', mobile))
        b = f'<rect x=".5" y=".5" width="1119" height="139" rx="12" fill="{c["bg"]}" stroke="{c["line"]}"/>'
        b += text(36, 38, 'HACK THE PLANET — LEGALLY', 11, c['accent'], mono=True, extra='letter-spacing="2"')
        b += text(36, 79, 'Security is not a product, but a process.', 27, c['ink'], 700)
        b += text(36, 111, '— Bruce Schneier', 14, c['muted'])
        b += text(1080, 112, 'BHAVISH S / END OF TRANSMISSION', 11, c['muted'], mono=True, extra='text-anchor="end"')
        (OUT / f'footer.{theme}.svg').write_text(svg(1120, 140, 'Security is not a product, but a process. — Bruce Schneier', b))
        for label in ['DEPLOYED', 'IN DEV']:
            color = c['accent'] if label == 'DEPLOYED' else ('#e9c182' if theme == 'dark' else '#805914')
            b = f'<rect x=".5" y=".5" width="99" height="25" rx="13" fill="{c["panel"]}" stroke="{c["line"]}"/><circle cx="14" cy="13" r="3" fill="{color}"/>'
            b += text(25, 17, label, 10, color, 700, mono=True)
            (OUT / f'{label.lower().replace(" ", "-")}.{theme}.svg').write_text(svg(100, 26, label, b))
        for slug, label in [('github', 'GitHub ↗'), ('linkedin', 'LinkedIn ↗'), ('email', 'Email ↗'), ('game', 'Snake & Ladder ↗')]:
            w = 174 if slug == 'game' else 118
            b = f'<rect x=".5" y=".5" width="{w-1}" height="39" rx="8" fill="{c["panel"]}" stroke="{c["line"]}"/>'
            b += text(w/2, 25, label, 14, c['ink'], 600, extra='text-anchor="middle"')
            (OUT / f'{slug}.{theme}.svg').write_text(svg(w, 40, label, b))
    print('Generated light and dark profile artwork.')

if __name__ == '__main__':
    generate()
