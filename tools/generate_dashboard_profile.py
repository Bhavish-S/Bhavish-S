#!/usr/bin/env python3
"""
Generate an award-winning, pixel-perfect GitHub profile suite
matching the reference UI mockup (media_1794980674134_2807238f.jpg):
- Primary background: Midnight navy #07131B
- Card background: Dark slate #10232D
- Card border: #13303D with #1C3E4E hover/accent
- Primary accent: Electric emerald #00E5A8
- Secondary accent: Cyber cyan #38BDF8
- Text: White #FFFFFF and Muted Silver #94A3B8
- Standard width: 920px (optimal for GitHub Desktop & Mobile)
"""

from pathlib import Path
import xml.etree.ElementTree as ET
import html

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/dashboard'
OUT.mkdir(parents=True, exist_ok=True)

def x(s: str) -> str:
    """Safely escape text for XML/SVG."""
    return html.escape(str(s), quote=True)

DEFS = """<defs>
  <!-- Background Gradients -->
  <linearGradient id="card-bg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#10232D"/>
    <stop offset="100%" stop-color="#0B1A22"/>
  </linearGradient>
  <linearGradient id="hero-bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#091B24"/>
    <stop offset="50%" stop-color="#07131B"/>
    <stop offset="100%" stop-color="#061017"/>
  </linearGradient>

  <!-- Accent Gradients -->
  <linearGradient id="emerald-cyan" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0%" stop-color="#00E5A8"/>
    <stop offset="100%" stop-color="#38BDF8"/>
  </linearGradient>
  <linearGradient id="cyan-emerald" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0%" stop-color="#38BDF8"/>
    <stop offset="100%" stop-color="#00E5A8"/>
  </linearGradient>
  <linearGradient id="accent-glow" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#00E5A8" stop-opacity="0.3"/>
    <stop offset="100%" stop-color="#38BDF8" stop-opacity="0"/>
  </linearGradient>

  <!-- Patterns -->
  <pattern id="mesh-grid" width="24" height="24" patternUnits="userSpaceOnUse">
    <path d="M 24 0 L 0 0 0 24" fill="none" stroke="#13303D" stroke-opacity="0.35"/>
  </pattern>
  <pattern id="dot-grid" width="20" height="20" patternUnits="userSpaceOnUse">
    <circle cx="2" cy="2" r="1" fill="#1C3E4E" fill-opacity="0.4"/>
  </pattern>

  <!-- Glow Filters -->
  <filter id="soft-glow" x="-20%" y="-20%" width="140%" height="140%">
    <feGaussianBlur stdDeviation="6" result="blur"/>
    <feComposite in="SourceGraphic" in2="blur" operator="over"/>
  </filter>
  <filter id="subtle-glow" x="-10%" y="-10%" width="120%" height="120%">
    <feGaussianBlur stdDeviation="3" result="blur"/>
    <feComposite in="SourceGraphic" in2="blur" operator="over"/>
  </filter>
</defs>"""

def card(width, height, title, content, rx=14, stroke="#13303D", fill="url(#card-bg)"):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title">
<title id="title">{x(title)}</title>
{DEFS}
<rect width="{width}" height="{height}" rx="{rx}" fill="{fill}"/>
<rect width="{width}" height="{height}" rx="{rx}" fill="url(#mesh-grid)"/>
<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="{rx-1}" stroke="{stroke}" stroke-width="1.2" fill="none"/>
{content}
</svg>"""

# ==============================================================================
# 1. HERO SECTION (920 x 240)
# ==============================================================================
def make_hero():
    content = """
  <!-- Top Subtle Edge Glow -->
  <rect x="2" y="2" width="916" height="3" rx="1.5" fill="url(#emerald-cyan)"/>

  <!-- Left: Avatar Graphic -->
  <g transform="translate(38, 38)">
    <!-- Outer Orbit & Pulse -->
    <circle cx="62" cy="62" r="72" fill="none" stroke="#00E5A8" stroke-opacity="0.15" stroke-dasharray="4 6"/>
    <circle cx="62" cy="62" r="64" fill="none" stroke="url(#emerald-cyan)" stroke-width="2.5"/>
    <circle cx="62" cy="62" r="58" fill="#0D1E27"/>
    
    <!-- Stylized Cyber Avatar Silhouette -->
    <circle cx="62" cy="48" r="22" fill="#142B36" stroke="#00E5A8" stroke-width="1.5"/>
    <!-- Visor -->
    <path d="M 50 48 L 74 48" stroke="#38BDF8" stroke-width="3" stroke-linecap="round" filter="url(#subtle-glow)"/>
    <!-- Body / Shoulders -->
    <path d="M 28 96 C 28 72, 96 72, 96 96 Z" fill="#142B36" stroke="#00E5A8" stroke-width="1.5"/>
    
    <!-- Glowing Status Node -->
    <circle cx="112" cy="102" r="8" fill="#07131B"/>
    <circle cx="112" cy="102" r="5" fill="#00E5A8" filter="url(#subtle-glow)"/>
  </g>

  <!-- Center Info -->
  <g transform="translate(200, 38)">
    <!-- Name -->
    <text x="0" y="32" fill="#FFFFFF" font-family="Space Grotesk, Inter, Arial, sans-serif" font-size="32" font-weight="800" letter-spacing="-0.5">Bhavish S</text>
    
    <!-- Title / Subheading -->
    <text x="0" y="58" fill="#00E5A8" font-family="Inter, Arial, sans-serif" font-size="13.5" font-weight="700" letter-spacing="1.5">CYBERSECURITY SPECIALIST <tspan fill="#38BDF8">|</tspan> DEVSECOPS &amp; AUTOMATION</text>
    
    <!-- Bio Narrative -->
    <text x="0" y="86" fill="#94A3B8" font-family="Inter, Arial, sans-serif" font-size="13" font-weight="400">Building secure, automated, and reliable systems.</text>
    <text x="0" y="106" fill="#94A3B8" font-family="Inter, Arial, sans-serif" font-size="13" font-weight="400">Focused on security engineering, automation, and developer productivity.</text>

    <!-- 3 Action CTA Pills -->
    <g transform="translate(0, 132)">
      <!-- Button 1: View Projects (Active Emerald) -->
      <a href="#featured-projects">
        <rect width="140" height="34" rx="7" fill="#00E5A8"/>
        <text x="70" y="22" fill="#07131B" font-family="Inter, Arial, sans-serif" font-size="12" font-weight="700" text-anchor="middle">View Projects &#x2794;</text>
      </a>

      <!-- Button 2: Portfolio & Lab -->
      <a href="https://bhavish-s.github.io/Bhavish-S/game/" target="_blank">
        <rect x="152" width="134" height="34" rx="7" fill="#10232D" stroke="#1C3E4E" stroke-width="1.2"/>
        <text x="219" y="22" fill="#F1F5F9" font-family="Inter, Arial, sans-serif" font-size="12" font-weight="600" text-anchor="middle">&#x1F4BB; Portfolio &#x2197;</text>
      </a>

      <!-- Button 3: Contact Handshake -->
      <a href="#connect">
        <rect x="298" width="112" height="34" rx="7" fill="#10232D" stroke="#1C3E4E" stroke-width="1.2"/>
        <text x="354" y="22" fill="#F1F5F9" font-family="Inter, Arial, sans-serif" font-size="12" font-weight="600" text-anchor="middle">&#x2709; Contact &#x2197;</text>
      </a>
    </g>
  </g>

  <!-- Right: 3D Wireframe Cyber Globe & Checklist -->
  <g transform="translate(675, 28)">
    <!-- Globe Backdrop -->
    <circle cx="120" cy="100" r="88" fill="#061218" stroke="#13303D" stroke-width="1"/>
    <!-- Wireframe Latitudes / Longitudes -->
    <ellipse cx="120" cy="100" rx="88" ry="40" fill="none" stroke="#1C3E4E" stroke-width="1" stroke-dasharray="3 3"/>
    <ellipse cx="120" cy="100" rx="40" ry="88" fill="none" stroke="#1C3E4E" stroke-width="1" stroke-dasharray="3 3"/>
    <circle cx="120" cy="100" r="70" fill="none" stroke="#00E5A8" stroke-opacity="0.25"/>
    <circle cx="120" cy="100" r="50" fill="none" stroke="#38BDF8" stroke-opacity="0.3"/>
    
    <!-- Rotating Radar Sweep Line -->
    <line x1="120" y1="100" x2="198" y2="70" stroke="#00E5A8" stroke-width="1.8" filter="url(#subtle-glow)"/>
    <circle cx="198" cy="70" r="3" fill="#00E5A8"/>

    <!-- Focus Badges Overlaid -->
    <g transform="translate(85, 36)">
      <rect width="135" height="116" rx="8" fill="#0A1821" fill-opacity="0.92" stroke="#1C3E4E" stroke-width="1.2"/>
      <text x="14" y="26" fill="#94A3B8" font-family="ui-monospace,Consolas,monospace" font-size="11">&gt; Security <tspan fill="#00E5A8">&#x2713;</tspan></text>
      <text x="14" y="52" fill="#94A3B8" font-family="ui-monospace,Consolas,monospace" font-size="11">&gt; Automation <tspan fill="#00E5A8">&#x2713;</tspan></text>
      <text x="14" y="78" fill="#94A3B8" font-family="ui-monospace,Consolas,monospace" font-size="11">&gt; DevOps <tspan fill="#00E5A8">&#x2713;</tspan></text>
      <text x="14" y="104" fill="#94A3B8" font-family="ui-monospace,Consolas,monospace" font-size="11">&gt; Open Source <tspan fill="#00E5A8">&#x2713;</tspan></text>
    </g>
  </g>
"""
    s = card(920, 240, "Bhavish S — Cybersecurity Engineer Hero", content, fill="url(#hero-bg)")
    (OUT / 'hero.svg').write_text(s, encoding='utf-8')
    print("Generated hero.svg")

# ==============================================================================
# 2. QUICK STATS ROW (920 x 82) - 5 Equal Cards
# ==============================================================================
def make_stats_bar():
    items = [
        ("🐙", "50+", "Repositories", "#00E5A8"),
        ("🏆", "10+", "Projects Built", "#38BDF8"),
        ("&lt;/&gt;", "15K+", "Lines of Code", "#00E5A8"),
        ("⚡", "20+", "Contributions (Recent)", "#38BDF8"),
        ("⭐", "50+", "Stars Earned", "#00E5A8")
    ]
    cards_svg = ""
    w = 172
    gap = 12
    for i, (icon, val, label, col) in enumerate(items):
        x_pos = 16 + i * (w + gap)
        cards_svg += f"""
  <g transform="translate({x_pos}, 12)">
    <rect width="{w}" height="58" rx="10" fill="#10232D" stroke="#13303D" stroke-width="1.2"/>
    <text x="16" y="36" font-size="18" fill="{col}" font-family="ui-monospace,Consolas,monospace">{icon}</text>
    <text x="50" y="28" fill="#FFFFFF" font-family="Space Grotesk, Inter, Arial, sans-serif" font-size="16" font-weight="800">{val}</text>
    <text x="50" y="44" fill="#94A3B8" font-family="Inter, Arial, sans-serif" font-size="10.5" font-weight="500">{label}</text>
  </g>
"""
    s = f"""<svg xmlns="http://www.w3.org/2000/svg" width="920" height="82" viewBox="0 0 920 82" role="img">
{DEFS}
<rect width="920" height="82" rx="12" fill="#07131B"/>
{cards_svg}
</svg>"""
    (OUT / 'stats-bar.svg').write_text(s, encoding='utf-8')
    print("Generated stats-bar.svg")

# ==============================================================================
# 3. ABOUT ME + TERMINAL (920 x 280) - 2 Columns
# ==============================================================================
def make_about_terminal():
    content = """
  <!-- Left Card: About Me (440w) -->
  <g transform="translate(16, 16)">
    <rect width="436" height="248" rx="12" fill="#10232D" stroke="#13303D" stroke-width="1.2"/>
    <text x="24" y="36" fill="#00E5A8" font-family="Space Grotesk, Inter, Arial, sans-serif" font-size="13" font-weight="700" letter-spacing="1.5">&#x1F464; ABOUT ME</text>
    <path d="M 24 46 L 412 46" stroke="#13303D"/>
    
    <text x="24" y="72" fill="#F1F5F9" font-family="Inter, Arial, sans-serif" font-size="12.5" font-weight="400">A cybersecurity-focused engineer who builds secure,</text>
    <text x="24" y="92" fill="#F1F5F9" font-family="Inter, Arial, sans-serif" font-size="12.5" font-weight="400">automated systems and developer tools. I combine offensive</text>
    <text x="24" y="112" fill="#F1F5F9" font-family="Inter, Arial, sans-serif" font-size="12.5" font-weight="400">security, automation, and software engineering to solve</text>
    <text x="24" y="132" fill="#F1F5F9" font-family="Inter, Arial, sans-serif" font-size="12.5" font-weight="400">real-world problems and improve system resilience.</text>

    <!-- Checklist -->
    <g transform="translate(24, 154)" font-family="Inter, Arial, sans-serif" font-size="12" fill="#94A3B8">
      <text x="0" y="14"><tspan fill="#00E5A8">&#x2611;</tspan>  Security Engineering &amp; Threat Monitoring</text>
      <text x="0" y="34"><tspan fill="#00E5A8">&#x2611;</tspan>  Automation &amp; Workflow Orchestration</text>
      <text x="0" y="54"><tspan fill="#00E5A8">&#x2611;</tspan>  Developer Tooling &amp; Open Source</text>
      <text x="0" y="74"><tspan fill="#00E5A8">&#x2611;</tspan>  Secure, Scalable &amp; Reliable Systems</text>
    </g>
  </g>

  <!-- Right Card: Interactive Terminal (440w) -->
  <g transform="translate(468, 16)">
    <rect width="436" height="248" rx="12" fill="#0A1821" stroke="#13303D" stroke-width="1.2"/>
    <!-- Terminal Title Bar -->
    <rect width="436" height="32" rx="12" fill="#0D1F29"/>
    <circle cx="20" cy="16" r="4.5" fill="#EF4444"/>
    <circle cx="34" cy="16" r="4.5" fill="#F59E0B"/>
    <circle cx="48" cy="16" r="4.5" fill="#10B981"/>
    <text x="64" y="20" fill="#94A3B8" font-family="ui-monospace,Consolas,monospace" font-size="11">bhavish@dev:~$ whoami</text>

    <!-- Hacker Hooded Silhouette Background Graphic -->
    <g transform="translate(300, 52)" opacity="0.35">
      <path d="M 60 18 C 38 18 20 38 16 66 C 14 82 8 120 0 160 L 120 160 C 112 120 106 82 104 66 C 100 38 82 18 60 18 Z" fill="#102733" stroke="#00E5A8" stroke-width="1"/>
      <path d="M 60 28 C 44 28 32 44 30 66 C 28 82 34 94 42 106 C 50 114 70 114 78 106 C 86 94 92 82 90 66 C 88 44 76 28 60 28 Z" fill="#061219"/>
      <line x1="46" y1="68" x2="74" y2="68" stroke="#00E5A8" stroke-width="2.5" filter="url(#subtle-glow)"/>
    </g>

    <!-- Terminal Output -->
    <g transform="translate(24, 52)" font-family="ui-monospace,Consolas,monospace" font-size="11.5">
      <text x="0" y="18" fill="#00E5A8">&gt; bhavish@dev:~$ <tspan fill="#FFFFFF">whoami</tspan></text>
      <text x="0" y="44" fill="#94A3B8">&#x2022; <tspan fill="#F1F5F9" font-weight="600">name</tspan>      : Bhavish S</text>
      <text x="0" y="68" fill="#94A3B8">&#x2022; <tspan fill="#F1F5F9" font-weight="600">role</tspan>      : Cybersecurity &amp; Automation Engineer</text>
      <text x="0" y="92" fill="#94A3B8">&#x2022; <tspan fill="#F1F5F9" font-weight="600">focus</tspan>     : Security | Automation | DevOps</text>
      <text x="0" y="116" fill="#94A3B8">&#x2022; <tspan fill="#F1F5F9" font-weight="600">interests</tspan> : Open Source, Tools, Infra, AI for Security</text>
      <text x="0" y="140" fill="#94A3B8">&#x2022; <tspan fill="#F1F5F9" font-weight="600">status</tspan>    : <tspan fill="#00E5A8">Building...</tspan> <tspan fill="#38BDF8">&#x2588;</tspan></text>
      <text x="0" y="172" fill="#38BDF8">&#x250C;&#x2500; [ KALI LINUX // HARDENED NODE ] &#x2500;&#x2500;&#x2500;&#x2500;&#x2510;</text>
    </g>
  </g>
"""
    s = card(920, 280, "About Me and Terminal Dossier", content, fill="#07131B")
    (OUT / 'about-terminal.svg').write_text(s, encoding='utf-8')
    print("Generated about-terminal.svg")

# ==============================================================================
# 4. CERTIFICATIONS & BADGES (920 x 130)
# ==============================================================================
def make_certifications():
    certs = [
        ("🛡️", "Security", "Security Fundamentals", "#00E5A8"),
        ("⚙️", "Automation", "Workflow &amp; Scripting", "#38BDF8"),
        ("♾️", "DevOps", "CI/CD &amp; Cloud", "#A855F7"),
        ("☁️", "Cloud", "Cloud Infrastructure", "#00E5A8"),
        ("🐙", "Open Source", "Community Contributor", "#38BDF8")
    ]
    items_svg = ""
    w = 168
    for i, (icon, title, sub, col) in enumerate(certs):
        x_pos = 24 + i * (w + 10)
        items_svg += f"""
  <g transform="translate({x_pos}, 46)">
    <circle cx="{w/2}" cy="22" r="20" fill="#0D1E27" stroke="{col}" stroke-width="1.5"/>
    <text x="{w/2}" y="28" font-size="16" text-anchor="middle">{icon}</text>
    <text x="{w/2}" y="56" fill="#FFFFFF" font-family="Space Grotesk, Inter, Arial, sans-serif" font-size="12" font-weight="700" text-anchor="middle">{title}</text>
    <text x="{w/2}" y="70" fill="#94A3B8" font-family="Inter, Arial, sans-serif" font-size="9.5" text-anchor="middle">{sub}</text>
  </g>
"""
    content = f"""
  <text x="24" y="28" fill="#00E5A8" font-family="Space Grotesk, Inter, Arial, sans-serif" font-size="12" font-weight="700" letter-spacing="1.5">&#x1F396;&#xFE0F; CERTIFICATIONS &amp; BADGES</text>
  <a href="#certifications">
    <text x="896" y="28" fill="#38BDF8" font-family="Inter, Arial, sans-serif" font-size="11" font-weight="600" text-anchor="end">View All &#x2794;</text>
  </a>
  <path d="M 24 36 L 896 36" stroke="#13303D"/>
  {items_svg}
"""
    s = card(920, 130, "Certifications and Badges", content, fill="#10232D")
    (OUT / 'certifications.svg').write_text(s, encoding='utf-8')
    print("Generated certifications.svg")

# ==============================================================================
# 5. SKILLS & PROFICIENCY + TECH STACK (920 x 280) - 2 Columns
# ==============================================================================
def make_skills_stack():
    skills = [
        ("Cybersecurity", 95, "🛡️"),
        ("Automation (Scripting/Workflows)", 92, "⚙️"),
        ("DevOps &amp; CI/CD", 90, "♾️"),
        ("Cloud &amp; Infrastructure", 88, "☁️"),
        ("Backend Development", 85, "📦"),
        ("System Design &amp; Operations", 82, "🖥️")
    ]
    bars_svg = ""
    for i, (name, pct, icon) in enumerate(skills):
        y_pos = 48 + i * 32
        bar_w = int(200 * (pct / 100))
        bars_svg += f"""
  <g transform="translate(24, {y_pos})">
    <text x="0" y="12" font-size="12">{icon}</text>
    <text x="22" y="12" fill="#F1F5F9" font-family="Inter, Arial, sans-serif" font-size="11" font-weight="600">{name}</text>
    <rect x="186" y="2" width="200" height="10" rx="5" fill="#0A1821" stroke="#13303D"/>
    <rect x="186" y="2" width="{bar_w}" height="10" rx="5" fill="url(#emerald-cyan)"/>
    <text x="398" y="11" fill="#00E5A8" font-family="ui-monospace,Consolas,monospace" font-size="11" font-weight="700">{pct}%</text>
  </g>
"""

    techs = [
        ("Python", "#38BDF8", "&lt;/&gt;"),
        ("Docker", "#00E5A8", "🐋"),
        ("Kubernetes", "#38BDF8", "⎈"),
        ("Linux", "#F59E0B", "🐧"),
        ("Bash", "#00E5A8", "&gt;_"),
        ("Git", "#F59E0B", "🔀"),
        ("GitHub", "#FFFFFF", "🐙"),
        ("VS Code", "#38BDF8", "📝"),
        ("PostgreSQL", "#38BDF8", "🐘"),
        ("Nginx", "#00E5A8", "⚡")
    ]
    tech_svg = ""
    col_w = 76
    row_h = 74
    for i, (label, col, sym) in enumerate(techs):
        r = i // 5
        c = i % 5
        x_pos = 20 + c * (col_w + 8)
        y_pos = 50 + r * (row_h + 12)
        tech_svg += f"""
  <g transform="translate({x_pos}, {y_pos})">
    <rect width="{col_w}" height="{row_h}" rx="10" fill="#0A1821" stroke="#13303D" stroke-width="1.2"/>
    <circle cx="{col_w/2}" cy="26" r="15" fill="#10232D" stroke="#1C3E4E"/>
    <text x="{col_w/2}" y="32" fill="{col}" font-family="ui-monospace,Consolas,monospace" font-size="13" font-weight="700" text-anchor="middle">{sym}</text>
    <text x="{col_w/2}" y="58" fill="#94A3B8" font-family="Inter, Arial, sans-serif" font-size="10.5" font-weight="600" text-anchor="middle">{label}</text>
  </g>
"""

    content = f"""
  <!-- Left Column: Skills -->
  <g transform="translate(16, 16)">
    <rect width="436" height="248" rx="12" fill="#10232D" stroke="#13303D" stroke-width="1.2"/>
    <text x="24" y="30" fill="#00E5A8" font-family="Space Grotesk, Inter, Arial, sans-serif" font-size="12" font-weight="700" letter-spacing="1.5">&#x1F4CA; SKILLS &amp; PROFICIENCY</text>
    <path d="M 24 38 L 412 38" stroke="#13303D"/>
    {bars_svg}
  </g>

  <!-- Right Column: Tech Stack -->
  <g transform="translate(468, 16)">
    <rect width="436" height="248" rx="12" fill="#10232D" stroke="#13303D" stroke-width="1.2"/>
    <text x="24" y="30" fill="#00E5A8" font-family="Space Grotesk, Inter, Arial, sans-serif" font-size="12" font-weight="700" letter-spacing="1.5">&#x1F4BB; TECH STACK (TOOLS &amp; TECHNOLOGIES)</text>
    <path d="M 24 38 L 412 38" stroke="#13303D"/>
    {tech_svg}
  </g>
"""
    s = card(920, 280, "Skills and Tech Stack Overview", content, fill="#07131B")
    (OUT / 'skills-stack.svg').write_text(s, encoding='utf-8')
    print("Generated skills-stack.svg")

# ==============================================================================
# 6. FEATURED PROJECTS (920 x 420) + INDIVIDUAL CARDS
# ==============================================================================
def make_projects():
    projects = [
        ("🔒", "NoDue Portal", "Student clearance workflow with automated approvals & admin panel", ["React", "TypeScript", "Node.js", "Firebase"], "Public", 24, 6, "https://github.com/Bhavish-S/noc", "project-nodue.svg"),
        ("💰", "Budget Allocator", "Intelligent financial planning with dynamic distribution algorithms", ["TypeScript", "React", "Tailwind"], "Public", 18, 4, "https://github.com/Bhavish-S/budget-allocator", "project-budget.svg"),
        ("🌐", "Route Resilience", "Fault-tolerant network routing & resilience graph simulation", ["HTML5", "Canvas", "Algorithms"], "Public", 32, 8, "https://github.com/Bhavish-S/Route_Resilience", "project-resilience.svg"),
        ("🎉", "Novic Events", "Full-featured event management, ticketing & cryptographic QR codes", ["Node.js", "WebStack", "REST"], "Public", 15, 3, "https://github.com/Bhavish-S/Novic-Events", "project-novic.svg"),
        ("🖥️", "SIEM Dashboard", "Custom Security Information & Event Management log correlation engine", ["Python", "Elastic", "Splunk", "Kibana"], "Public", 21, 5, "https://github.com/Bhavish-S", "project-siem.svg"),
        ("⚔️", "PenTest Toolkit", "Modular offensive security testing automation & reconnaissance suite", ["Python 3", "Bash", "Sockets"], "Public", 29, 7, "https://github.com/Bhavish-S", "project-pentest.svg")
    ]

    cards_svg = ""
    col_w = 280
    row_h = 168
    for i, (icon, title, desc, tags, status, stars, forks, link, _) in enumerate(projects):
        r = i // 3
        c = i % 3
        x_pos = 24 + c * (col_w + 14)
        y_pos = 52 + r * (row_h + 14)
        status_col = "#00E5A8" if status == "Public" else "#F59E0B"
        
        tags_svg = ""
        tag_x = 16
        for tag in tags[:3]:
            tw = len(tag) * 6 + 12
            tags_svg += f"""
      <rect x="{tag_x}" y="98" width="{tw}" height="18" rx="4" fill="#0A1821" stroke="#1C3E4E"/>
      <text x="{tag_x + tw/2}" y="110" fill="#94A3B8" font-family="ui-monospace,Consolas,monospace" font-size="9" text-anchor="middle">{tag}</text>
"""
            tag_x += tw + 6

        # Cut descriptions cleanly before XML escaping
        d1 = x(desc[:42] + ("..." if len(desc) > 42 else ""))
        d2 = x(desc[42:84])
        
        cards_svg += f"""
  <g transform="translate({x_pos}, {y_pos})">
    <rect width="{col_w}" height="{row_h}" rx="12" fill="#10232D" stroke="#13303D" stroke-width="1.2"/>
    <circle cx="28" cy="28" r="14" fill="#0A1821" stroke="#1C3E4E"/>
    <text x="28" y="33" font-size="14" text-anchor="middle">{icon}</text>
    
    <!-- Title -->
    <text x="50" y="32" fill="#FFFFFF" font-family="Space Grotesk, Inter, Arial, sans-serif" font-size="14" font-weight="700">{x(title)}</text>
    
    <!-- Status Badge -->
    <rect x="{col_w - 60}" y="18" width="46" height="18" rx="4" fill="{status_col}" fill-opacity="0.15" stroke="{status_col}" stroke-opacity="0.6"/>
    <text x="{col_w - 37}" y="30" fill="{status_col}" font-family="ui-monospace,Consolas,monospace" font-size="9" font-weight="700" text-anchor="middle">{status}</text>
    
    <!-- Description -->
    <text x="16" y="62" fill="#94A3B8" font-family="Inter, Arial, sans-serif" font-size="11">{d1}</text>
    <text x="16" y="78" fill="#94A3B8" font-family="Inter, Arial, sans-serif" font-size="11">{d2}</text>

    <!-- Tags -->
    {tags_svg}

    <!-- Bottom: Stars / Forks & Link -->
    <path d="M 16 128 L {col_w - 16} 128" stroke="#13303D"/>
    <text x="16" y="146" fill="#94A3B8" font-family="Inter, Arial, sans-serif" font-size="10.5">⭐ {stars} &#160; 🍴 {forks}</text>
    <a href="{link}" target="_blank">
      <rect x="{col_w - 92}" y="132" width="76" height="22" rx="5" fill="#0A1821" stroke="#00E5A8" stroke-width="1"/>
      <text x="{col_w - 54}" y="146" fill="#00E5A8" font-family="Inter, Arial, sans-serif" font-size="10" font-weight="700" text-anchor="middle">View Repo &#x2794;</text>
    </a>
  </g>
"""

    content = f"""
  <text x="24" y="32" fill="#00E5A8" font-family="Space Grotesk, Inter, Arial, sans-serif" font-size="13" font-weight="700" letter-spacing="1.5">&#x26A1; FEATURED PROJECTS</text>
  <a href="https://github.com/Bhavish-S?tab=repositories" target="_blank">
    <text x="896" y="32" fill="#38BDF8" font-family="Inter, Arial, sans-serif" font-size="11" font-weight="600" text-anchor="end">View All Projects &#x2794;</text>
  </a>
  <path d="M 24 42 L 896 42" stroke="#13303D"/>
  {cards_svg}
"""
    s = card(920, 420, "Featured Projects Grid", content, fill="#07131B")
    (OUT / 'featured-projects.svg').write_text(s, encoding='utf-8')
    print("Generated featured-projects.svg")

    # Also generate individual clickable project card SVGs (width 440 x height 140)
    for icon, title, desc, tags, status, stars, forks, link, fname in projects:
        status_col = "#00E5A8" if status == "Public" else "#F59E0B"
        tags_markup = ""
        tx = 16
        for tag in tags[:4]:
            tw = len(tag) * 6 + 12
            tags_markup += f"""
    <rect x="{tx}" y="78" width="{tw}" height="18" rx="4" fill="#0A1821" stroke="#1C3E4E"/>
    <text x="{tx + tw/2}" y="90" fill="#94A3B8" font-family="ui-monospace,Consolas,monospace" font-size="9.5" text-anchor="middle">{tag}</text>
"""
            tx += tw + 6

        single_card = f"""<svg xmlns="http://www.w3.org/2000/svg" width="440" height="136" viewBox="0 0 440 136" role="img">
{DEFS}
<rect width="440" height="136" rx="12" fill="#10232D" stroke="#13303D" stroke-width="1.2"/>
<circle cx="28" cy="28" r="14" fill="#0A1821" stroke="#1C3E4E"/>
<text x="28" y="33" font-size="14" text-anchor="middle">{icon}</text>
<text x="50" y="32" fill="#FFFFFF" font-family="Space Grotesk, Inter, Arial, sans-serif" font-size="14" font-weight="700">{x(title)}</text>
<rect x="372" y="18" width="52" height="18" rx="4" fill="{status_col}" fill-opacity="0.15" stroke="{status_col}" stroke-opacity="0.6"/>
<text x="398" y="30" fill="{status_col}" font-family="ui-monospace,Consolas,monospace" font-size="9" font-weight="700" text-anchor="middle">{status}</text>
<text x="16" y="58" fill="#94A3B8" font-family="Inter, Arial, sans-serif" font-size="11">{x(desc)}</text>
{tags_markup}
<path d="M 16 106 L 424 106" stroke="#13303D"/>
<text x="16" y="122" fill="#94A3B8" font-family="Inter, Arial, sans-serif" font-size="10.5">⭐ {stars} &#160; 🍴 {forks}</text>
<rect x="342" y="110" width="82" height="20" rx="4" fill="#0A1821" stroke="#00E5A8" stroke-width="1"/>
<text x="383" y="124" fill="#00E5A8" font-family="Inter, Arial, sans-serif" font-size="10" font-weight="700" text-anchor="middle">View Repo &#x2794;</text>
</svg>"""
        (OUT / fname).write_text(single_card, encoding='utf-8')
        print(f"Generated {fname}")

# ==============================================================================
# 7. GITHUB TELEMETRY & ACTIVITY DASHBOARD (920 x 250) - 3 Columns
# ==============================================================================
def make_activity_dashboard():
    import random
    random.seed(42)
    colors = ["#0D1F29", "#004733", "#007A55", "#00B377", "#00E5A8"]
    matrix_cells = ""
    for col in range(15):
        for row in range(7):
            c = random.choice(colors)
            matrix_cells += f'<rect x="{col*16}" y="{row*15}" width="11" height="11" rx="2.5" fill="{c}"/>\n'

    content = f"""
  <!-- Card 1: Statistics Donut (280w) -->
  <g transform="translate(18, 16)">
    <rect width="280" height="218" rx="12" fill="#10232D" stroke="#13303D" stroke-width="1.2"/>
    <text x="20" y="30" fill="#00E5A8" font-family="Space Grotesk, Inter, Arial, sans-serif" font-size="11.5" font-weight="700" letter-spacing="1">&#x1F4CA; GITHUB STATISTICS</text>
    <path d="M 20 38 L 260 38" stroke="#13303D"/>

    <!-- Donut SVG -->
    <g transform="translate(70, 118)">
      <circle cx="0" cy="0" r="44" fill="none" stroke="#0A1821" stroke-width="16"/>
      <circle cx="0" cy="0" r="44" fill="none" stroke="#00E5A8" stroke-width="16" stroke-dasharray="140 280" stroke-dashoffset="0"/>
      <circle cx="0" cy="0" r="44" fill="none" stroke="#38BDF8" stroke-width="16" stroke-dasharray="60 280" stroke-dashoffset="-140"/>
      <circle cx="0" cy="0" r="44" fill="none" stroke="#F59E0B" stroke-width="16" stroke-dasharray="40 280" stroke-dashoffset="-200"/>
      <!-- Inner Icon -->
      <text x="0" y="6" fill="#F1F5F9" font-size="18" text-anchor="middle">🐙</text>
    </g>

    <!-- Legend -->
    <g transform="translate(145, 68)" font-family="Inter, Arial, sans-serif" font-size="11" fill="#94A3B8">
      <circle cx="6" cy="14" r="4" fill="#00E5A8"/><text x="18" y="18">Python (42%)</text>
      <circle cx="6" cy="38" r="4" fill="#38BDF8"/><text x="18" y="42">Shell (18%)</text>
      <circle cx="6" cy="62" r="4" fill="#F59E0B"/><text x="18" y="66">Dockerfile (12%)</text>
      <circle cx="6" cy="86" r="4" fill="#A855F7"/><text x="18" y="90">JavaScript (10%)</text>
      <circle cx="6" cy="110" r="4" fill="#64748B"/><text x="18" y="114">Other (18%)</text>
    </g>
  </g>

  <!-- Card 2: Contributions Matrix (280w) -->
  <g transform="translate(320, 16)">
    <rect width="280" height="218" rx="12" fill="#10232D" stroke="#13303D" stroke-width="1.2"/>
    <text x="20" y="30" fill="#00E5A8" font-family="Space Grotesk, Inter, Arial, sans-serif" font-size="11.5" font-weight="700" letter-spacing="1">&#x1F4C5; CONTRIBUTIONS (LAST 12 MONTHS)</text>
    <path d="M 20 38 L 260 38" stroke="#13303D"/>

    <g transform="translate(20, 52)">
      <text x="0" y="0" fill="#94A3B8" font-family="ui-monospace,Consolas,monospace" font-size="8.5">Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec</text>
      <g transform="translate(0, 10)">
        {matrix_cells}
      </g>
      <text x="0" y="132" fill="#94A3B8" font-family="Inter, Arial, sans-serif" font-size="10.5">200+ commits in the last year</text>
    </g>
  </g>

  <!-- Card 3: Activity Trend Chart (280w) -->
  <g transform="translate(622, 16)">
    <rect width="280" height="218" rx="12" fill="#10232D" stroke="#13303D" stroke-width="1.2"/>
    <text x="20" y="30" fill="#00E5A8" font-family="Space Grotesk, Inter, Arial, sans-serif" font-size="11.5" font-weight="700" letter-spacing="1">&#x1F4C8; ACTIVITY (COMMITS)</text>
    <path d="M 20 38 L 260 38" stroke="#13303D"/>

    <g transform="translate(20, 55)">
      <!-- Grid lines -->
      <line x1="0" y1="20" x2="240" y2="20" stroke="#13303D" stroke-dasharray="2 3"/>
      <line x1="0" y1="60" x2="240" y2="60" stroke="#13303D" stroke-dasharray="2 3"/>
      <line x1="0" y1="100" x2="240" y2="100" stroke="#13303D" stroke-dasharray="2 3"/>

      <!-- Smooth Bezier Curve -->
      <path d="M 10 90 Q 50 80, 80 50 T 150 40 T 200 15 T 235 25" fill="none" stroke="#00E5A8" stroke-width="2.5" filter="url(#subtle-glow)"/>
      <path d="M 10 90 Q 50 80, 80 50 T 150 40 T 200 15 T 235 25 L 235 110 L 10 110 Z" fill="url(#accent-glow)"/>

      <!-- Data Points -->
      <circle cx="10" cy="90" r="3.5" fill="#00E5A8"/>
      <circle cx="80" cy="50" r="3.5" fill="#38BDF8"/>
      <circle cx="150" cy="40" r="3.5" fill="#00E5A8"/>
      <circle cx="200" cy="15" r="4.5" fill="#00E5A8" stroke="#FFFFFF" stroke-width="1"/>
      <circle cx="235" cy="25" r="3.5" fill="#38BDF8"/>

      <text x="0" y="128" fill="#94A3B8" font-family="ui-monospace,Consolas,monospace" font-size="9">Jan  Feb  Mar  Apr  May  Jun  Jul  Aug  Sep  Oct  Nov  Dec</text>
    </g>
  </g>
"""
    s = card(920, 250, "GitHub Telemetry & Activity Dashboard", content, fill="#07131B")
    (OUT / 'activity-dashboard.svg').write_text(s, encoding='utf-8')
    print("Generated activity-dashboard.svg")

# ==============================================================================
# 8. RECENT ACTIVITY & GITHUB OVERVIEW (920 x 220) - 2 Columns
# ==============================================================================
def make_recent_activity_overview():
    content = """
  <!-- Left Column: Recent Activity (440w) -->
  <g transform="translate(16, 16)">
    <rect width="436" height="188" rx="12" fill="#10232D" stroke="#13303D" stroke-width="1.2"/>
    <text x="24" y="28" fill="#00E5A8" font-family="Space Grotesk, Inter, Arial, sans-serif" font-size="12" font-weight="700" letter-spacing="1.5">&#x26A1; RECENT ACTIVITY</text>
    <path d="M 24 36 L 412 36" stroke="#13303D"/>

    <g transform="translate(24, 46)" font-family="Inter, Arial, sans-serif" font-size="11">
      <!-- Item 1 -->
      <g transform="translate(0, 14)">
        <text x="0" y="0" fill="#38BDF8" font-family="ui-monospace,Consolas,monospace">●</text>
        <text x="16" y="0" fill="#94A3B8">Pushed updates to <tspan fill="#00E5A8" font-weight="600">automation-engine</tspan></text>
        <text x="388" y="0" fill="#64748B" text-anchor="end">2 hours ago</text>
      </g>
      <!-- Item 2 -->
      <g transform="translate(0, 38)">
        <text x="0" y="0" fill="#00E5A8" font-family="ui-monospace,Consolas,monospace">●</text>
        <text x="16" y="0" fill="#94A3B8">Opened issue in <tspan fill="#38BDF8" font-weight="600">secureops-toolkit</tspan></text>
        <text x="388" y="0" fill="#64748B" text-anchor="end">5 hours ago</text>
      </g>
      <!-- Item 3 -->
      <g transform="translate(0, 62)">
        <text x="0" y="0" fill="#A855F7" font-family="ui-monospace,Consolas,monospace">●</text>
        <text x="16" y="0" fill="#94A3B8">Merged pull request in <tspan fill="#00E5A8" font-weight="600">threat-monitor</tspan></text>
        <text x="388" y="0" fill="#64748B" text-anchor="end">1 day ago</text>
      </g>
      <!-- Item 4 -->
      <g transform="translate(0, 86)">
        <text x="0" y="0" fill="#F59E0B" font-family="ui-monospace,Consolas,monospace">★</text>
        <text x="16" y="0" fill="#94A3B8">Starred a security repository</text>
        <text x="388" y="0" fill="#64748B" text-anchor="end">1 day ago</text>
      </g>
      <!-- Item 5 -->
      <g transform="translate(0, 110)">
        <text x="0" y="0" fill="#00E5A8" font-family="ui-monospace,Consolas,monospace">+</text>
        <text x="16" y="0" fill="#94A3B8">Created a new repository</text>
        <text x="388" y="0" fill="#64748B" text-anchor="end">2 days ago</text>
      </g>
    </g>
  </g>

  <!-- Right Column: GitHub Overview (440w) - 2x2 Grid -->
  <g transform="translate(468, 16)">
    <rect width="436" height="188" rx="12" fill="#10232D" stroke="#13303D" stroke-width="1.2"/>
    <text x="24" y="28" fill="#00E5A8" font-family="Space Grotesk, Inter, Arial, sans-serif" font-size="12" font-weight="700" letter-spacing="1.5">&#x1F4CA; GITHUB OVERVIEW</text>
    <path d="M 24 36 L 412 36" stroke="#13303D"/>

    <g transform="translate(24, 52)">
      <!-- Box 1 -->
      <rect x="0" y="0" width="186" height="54" rx="8" fill="#0A1821" stroke="#13303D"/>
      <text x="16" y="32" font-size="18">📦</text>
      <text x="44" y="26" fill="#FFFFFF" font-family="Space Grotesk, Inter, Arial, sans-serif" font-size="15" font-weight="800">50+</text>
      <text x="44" y="42" fill="#94A3B8" font-family="Inter, Arial, sans-serif" font-size="10.5">Repositories</text>

      <!-- Box 2 -->
      <rect x="202" y="0" width="186" height="54" rx="8" fill="#0A1821" stroke="#13303D"/>
      <text x="218" y="32" font-size="18">⭐</text>
      <text x="246" y="26" fill="#FFFFFF" font-family="Space Grotesk, Inter, Arial, sans-serif" font-size="15" font-weight="800">50+</text>
      <text x="246" y="42" fill="#94A3B8" font-family="Inter, Arial, sans-serif" font-size="10.5">Stars Earned</text>

      <!-- Box 3 -->
      <rect x="0" y="66" width="186" height="54" rx="8" fill="#0A1821" stroke="#13303D"/>
      <text x="16" y="98" font-size="18">🍴</text>
      <text x="44" y="92" fill="#FFFFFF" font-family="Space Grotesk, Inter, Arial, sans-serif" font-size="15" font-weight="800">20+</text>
      <text x="44" y="108" fill="#94A3B8" font-family="Inter, Arial, sans-serif" font-size="10.5">Forks</text>

      <!-- Box 4 -->
      <rect x="202" y="66" width="186" height="54" rx="8" fill="#0A1821" stroke="#13303D"/>
      <text x="218" y="98" font-size="18">👥</text>
      <text x="246" y="92" fill="#FFFFFF" font-family="Space Grotesk, Inter, Arial, sans-serif" font-size="15" font-weight="800">10+</text>
      <text x="246" y="108" fill="#94A3B8" font-family="Inter, Arial, sans-serif" font-size="10.5">Collaborations</text>
    </g>
  </g>
"""
    s = card(920, 220, "Recent Activity and GitHub Overview", content, fill="#07131B")
    (OUT / 'recent-activity-overview.svg').write_text(s, encoding='utf-8')
    print("Generated recent-activity-overview.svg")

# ==============================================================================
# 9. TOP INTERESTS TAG BAR (920 x 80)
# ==============================================================================
def make_interests_bar():
    tags = [
        ("🛡️", "Threat Detection"),
        ("⚙️", "Security Automation"),
        ("♾️", "DevSecOps"),
        ("☁️", "Infrastructure as Code"),
        ("🐙", "Open Source"),
        ("🤖", "AI for Security")
    ]
    pills_svg = ""
    w = 138
    for i, (icon, text) in enumerate(tags):
        x_pos = 20 + i * (w + 10)
        pills_svg += f"""
  <g transform="translate({x_pos}, 24)">
    <rect width="{w}" height="32" rx="8" fill="#10232D" stroke="#13303D" stroke-width="1.2"/>
    <text x="12" y="20" font-size="12">{icon}</text>
    <text x="32" y="20" fill="#F1F5F9" font-family="Inter, Arial, sans-serif" font-size="10.5" font-weight="600">{text}</text>
  </g>
"""
    s = f"""<svg xmlns="http://www.w3.org/2000/svg" width="920" height="80" viewBox="0 0 920 80" role="img">
{DEFS}
<rect width="920" height="80" rx="12" fill="#07131B"/>
{pills_svg}
</svg>"""
    (OUT / 'interests-bar.svg').write_text(s, encoding='utf-8')
    print("Generated interests-bar.svg")

# ==============================================================================
# 10. FINAL CTA FOOTER (920 x 110)
# ==============================================================================
def make_cta_footer():
    content = """
  <g transform="translate(32, 28)">
    <text x="0" y="26" fill="#00E5A8" font-family="ui-monospace,Consolas,monospace" font-size="20" font-weight="800">&lt;/&gt;</text>
    <text x="38" y="24" fill="#FFFFFF" font-family="Space Grotesk, Inter, Arial, sans-serif" font-size="20" font-weight="800">Let's build <tspan fill="#00E5A8">secure systems</tspan> together.</text>
    <text x="38" y="46" fill="#94A3B8" font-family="Inter, Arial, sans-serif" font-size="12">Open to collaboration, interesting projects, and security-focused ideas.</text>
  </g>

  <!-- Action Badges Right -->
  <g transform="translate(560, 36)">
    <!-- GitHub -->
    <a href="https://github.com/Bhavish-S" target="_blank">
      <rect x="0" width="102" height="38" rx="8" fill="#0A1821" stroke="#1C3E4E" stroke-width="1.2"/>
      <text x="51" y="23" fill="#F1F5F9" font-family="Inter, Arial, sans-serif" font-size="12" font-weight="600" text-anchor="middle">🐙 GitHub</text>
    </a>

    <!-- LinkedIn -->
    <a href="https://www.linkedin.com/in/bhavish-s-/" target="_blank">
      <rect x="114" width="108" height="38" rx="8" fill="#0A1821" stroke="#1C3E4E" stroke-width="1.2"/>
      <text x="168" y="23" fill="#F1F5F9" font-family="Inter, Arial, sans-serif" font-size="12" font-weight="600" text-anchor="middle">💼 LinkedIn</text>
    </a>

    <!-- Email -->
    <a href="mailto:bhavishgowda2006@gmail.com">
      <rect x="234" width="96" height="38" rx="8" fill="#00E5A8"/>
      <text x="282" y="23" fill="#07131B" font-family="Inter, Arial, sans-serif" font-size="12" font-weight="700" text-anchor="middle">✉️ Email</text>
    </a>
  </g>
"""
    s = card(920, 110, "Final Call to Action — Build Secure Systems Together", content, fill="#10232D")
    (OUT / 'cta-footer.svg').write_text(s, encoding='utf-8')
    print("Generated cta-footer.svg")

if __name__ == '__main__':
    make_hero()
    make_stats_bar()
    make_about_terminal()
    make_certifications()
    make_skills_stack()
    make_projects()
    make_activity_dashboard()
    make_recent_activity_overview()
    make_interests_bar()
    make_cta_footer()
