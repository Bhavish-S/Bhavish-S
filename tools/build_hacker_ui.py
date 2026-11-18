#!/usr/bin/env python3
"""Build ultra-polished, cohesive quantum hacker UI components with matching background."""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/quantum'
OUT.mkdir(parents=True, exist_ok=True)

COMMON_DEFS = """<defs>
  <linearGradient id="bg" x2="1" y2="1">
    <stop offset="0%" stop-color="#030d14"/>
    <stop offset="50%" stop-color="#071b24"/>
    <stop offset="100%" stop-color="#050b16"/>
  </linearGradient>
  <linearGradient id="neon" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0%" stop-color="#00f5a0"/>
    <stop offset="50%" stop-color="#75ff9e"/>
    <stop offset="100%" stop-color="#00d9ff"/>
  </linearGradient>
  <linearGradient id="cyan-glow" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0%" stop-color="#00d9ff"/>
    <stop offset="100%" stop-color="#00f5a0"/>
  </linearGradient>
  <radialGradient id="halo">
    <stop offset="0%" stop-color="#00ff9d" stop-opacity="0.22"/>
    <stop offset="100%" stop-color="#00ff9d" stop-opacity="0"/>
  </radialGradient>
  <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse">
    <path d="M 32 0 L 0 0 0 32" fill="none" stroke="#1c5362" stroke-opacity="0.25"/>
  </pattern>
  <filter id="glow">
    <feGaussianBlur stdDeviation="5" result="coloredBlur"/>
    <feMerge>
      <feMergeNode in="coloredBlur"/>
      <feMergeNode in="SourceGraphic"/>
    </feMerge>
  </filter>
</defs>"""

def card_base(width, height, title):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title">
<title id="title">{escape(title)}</title>
{COMMON_DEFS}
<rect width="{width}" height="{height}" rx="20" fill="url(#bg)"/>
<rect width="{width}" height="{height}" rx="20" fill="url(#grid)"/>
<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="19" stroke="#278c85" stroke-opacity="0.5" fill="none"/>
"""

# 1. THREAT DOSSIER & SYSTEM METRICS (width 1200, height 520)
def generate_threat_dossier():
    s = card_base(1200, 520, "Threat Dossier — Target Profile & System Status")
    # Window Header
    s += """
  <!-- Terminal Header Bar -->
  <rect x="25" y="20" width="1150" height="36" rx="8" fill="#091b24" stroke="#1c5362" stroke-opacity="0.6"/>
  <circle cx="48" cy="38" r="6" fill="#ff5f56"/>
  <circle cx="68" cy="38" r="6" fill="#ffbd2e"/>
  <circle cx="88" cy="38" r="6" fill="#27c93f"/>
  <text x="110" y="43" fill="#65dcb3" font-family="ui-monospace,Consolas,monospace" font-size="13" letter-spacing="1">root@kali: ~ (CLASSIFIED THREAT DOSSIER // OPERATOR INTEL)</text>
  <text x="1150" y="43" fill="#00d9ff" font-family="ui-monospace,Consolas,monospace" font-size="12" text-anchor="end" letter-spacing="1">[STATUS: SECURE // ONLINE]</text>

  <!-- Left: Terminal Details -->
  <rect x="25" y="68" width="670" height="430" rx="12" fill="#040b10" stroke="#16382c"/>
  <g font-family="ui-monospace,Consolas,monospace" font-size="13" xml:space="preserve">
    <text x="45" y="100" fill="#00d9ff" font-weight="700">bhavish@kali:~$ <tspan fill="#f1fff9">whoami --profile</tspan></text>
    <text x="45" y="128" fill="#65dcb3">┌─ IDENTITY ────────────────────────────────────────────────┐</text>
    <text x="45" y="148" fill="#c7e8df">│  codename    : <tspan fill="#00f5a0" font-weight="700">Bhavish S</tspan></text>
    <text x="45" y="168" fill="#c7e8df">│  alias       : <tspan fill="#00d9ff">"The Legal Hacker"</tspan></text>
    <text x="45" y="188" fill="#c7e8df">│  system_os   : Kali Linux · Arch · Debian · macOS</text>
    <text x="45" y="208" fill="#c7e8df">│  location    : India 🇮🇳  |  degree: B.Tech Computer Science</text>
    <text x="45" y="228" fill="#c7e8df">│  clearance   : <tspan fill="#00f5a0">Ethical Hacker Level 5 (Google CyberSec ✅)</tspan></text>
    <text x="45" y="248" fill="#65dcb3">└───────────────────────────────────────────────────────────┘</text>

    <text x="45" y="278" fill="#00d9ff" font-weight="700">bhavish@kali:~$ <tspan fill="#f1fff9">cat /etc/security_capabilities</tspan></text>
    <text x="45" y="306" fill="#c7e8df">[✓] <tspan fill="#00f5a0">OFFENSIVE</tspan> : Web App PenTest · OWASP Top 10 · Network Recon · Brute Force</text>
    <text x="45" y="328" fill="#c7e8df">[✓] <tspan fill="#00d9ff">DEFENSIVE</tspan> : SOC Operations · SIEM (Splunk/Elastic) · MITRE ATT&amp;CK Mapping</text>
    <text x="45" y="350" fill="#c7e8df">[✓] <tspan fill="#75ff9e">DEVSECOPS</tspan> : Python Automation · CI/CD Security · Container CVE Scanning</text>
    <text x="45" y="372" fill="#c7e8df">[✓] <tspan fill="#c7e8df">FULL-STACK</tspan>: React · TypeScript · Node.js · Express · REST &amp; WebSockets</text>

    <text x="45" y="408" fill="#00d9ff" font-weight="700">bhavish@kali:~$ <tspan fill="#f1fff9">systemctl status bhavish-defense-engine</tspan></text>
    <text x="45" y="434" fill="#00f5a0">● Active: running (high-performance) since boot</text>
    <text x="45" y="456" fill="#8baea6">  Missions: NoDue Portal [DEPLOYED] · SIEM &amp; PenTest Toolkits [IN BUILD]</text>
    <text x="45" y="478" fill="#65dcb3">  Philosophy: "Break it to understand it. Then make it unbreakable."</text>
  </g>

  <!-- Right: 3 Metric Focus Panels -->
  <!-- Panel 1: Offensive Core -->
  <rect x="710" y="68" width="465" height="134" rx="12" fill="#081820" stroke="#1c5362"/>
  <rect x="710" y="68" width="465" height="4" rx="2" fill="url(#neon)"/>
  <text x="730" y="98" fill="#00f5a0" font-family="Arial,Helvetica,sans-serif" font-size="14" font-weight="700" letter-spacing="1">01 // OFFENSIVE TACTICS</text>
  <text x="730" y="125" fill="#f1fff9" font-family="Arial,Helvetica,sans-serif" font-size="18" font-weight="800">Penetration Testing &amp; Red Teaming</text>
  <text x="730" y="150" fill="#9dbcc8" font-family="Arial,Helvetica,sans-serif" font-size="13">Burp Suite Professional · Nmap · Metasploit · SQLMap · Hydra</text>
  <text x="730" y="175" fill="#65dcb3" font-family="ui-monospace,Consolas,monospace" font-size="12">[ 50+ VULNERABILITY LABS SOLVED ON HTB &amp; TRYHACKME ]</text>

  <!-- Panel 2: Defensive Operations -->
  <rect x="710" y="216" width="465" height="134" rx="12" fill="#081820" stroke="#1c5362"/>
  <rect x="710" y="216" width="465" height="4" rx="2" fill="url(#cyan-glow)"/>
  <text x="730" y="246" fill="#00d9ff" font-family="Arial,Helvetica,sans-serif" font-size="14" font-weight="700" letter-spacing="1">02 // DEFENSIVE TELEMETRY</text>
  <text x="730" y="273" fill="#f1fff9" font-family="Arial,Helvetica,sans-serif" font-size="18" font-weight="800">SOC Operations &amp; SIEM Engineering</text>
  <text x="730" y="298" fill="#9dbcc8" font-family="Arial,Helvetica,sans-serif" font-size="13">Splunk Enterprise · ELK Stack · Kibana · Wireshark · Packet Forensics</text>
  <text x="730" y="323" fill="#65dcb3" font-family="ui-monospace,Consolas,monospace" font-size="12">[ LOG CORRELATION · INCIDENT RESPONSE · THREAT HUNTING ]</text>

  <!-- Panel 3: Certifications & Goals -->
  <rect x="710" y="364" width="465" height="134" rx="12" fill="#081820" stroke="#1c5362"/>
  <rect x="710" y="364" width="465" height="4" rx="2" fill="url(#neon)"/>
  <text x="730" y="394" fill="#75ff9e" font-family="Arial,Helvetica,sans-serif" font-size="14" font-weight="700" letter-spacing="1">03 // CERTIFICATION KILL-CHAIN</text>
  <text x="730" y="421" fill="#f1fff9" font-family="Arial,Helvetica,sans-serif" font-size="18" font-weight="800">Google Cybersecurity Professional ✅</text>
  <text x="730" y="446" fill="#9dbcc8" font-family="Arial,Helvetica,sans-serif" font-size="13">TryHackMe Jr. PenTester [ACTIVE]  •  HackTheBox Starting Point [ACTIVE]</text>
  <text x="730" y="471" fill="#00f5a0" font-family="ui-monospace,Consolas,monospace" font-size="12" font-weight="700">NEXT MILESTONES ➔ eJPT → CEH → OSCP (Offensive Security Pro)</text>
</svg>"""
    (OUT / 'threat-dossier.svg').write_text(s, encoding='utf-8')
    print("Generated threat-dossier.svg")

# 2. DEVSECOPS PIPELINE (width 1200, height 260)
def generate_pipeline():
    s = card_base(1200, 260, "Secure SDLC & DevSecOps Pipeline")
    s += """
  <!-- Header -->
  <text x="40" y="44" fill="#00f5a0" font-family="ui-monospace,Consolas,monospace" font-size="14" font-weight="700" letter-spacing="2">// SECURE SDLC &amp; DEVSECOPS PIPELINE — SHIFT-LEFT DEFENSE</text>
  <text x="1160" y="44" fill="#65dcb3" font-family="ui-monospace,Consolas,monospace" font-size="12" text-anchor="end">[ CONTINUOUS AUTOMATED COMPLIANCE ]</text>
  <path d="M 40 60 L 1160 60" stroke="#1c5362" stroke-opacity="0.6"/>

  <!-- 5 Pipeline Nodes -->
"""
    nodes = [
        ("01", "CODE PUSH", "Git PR / Commits", "Branch protection", 40),
        ("02", "SAST & SECRETS", "Semgrep · TruffleHog", "AST & Leak Audits", 270),
        ("03", "BUILD & LINT", "Docker Container", "Isolated Sandbox", 500),
        ("04", "IMAGE CVE SCAN", "Trivy Vulnerability Scan", "Zero High/Crit CVEs", 730),
        ("05", "DAST & STAGING", "OWASP ZAP Dynamic", "Production Hardened", 960)
    ]
    for num, title, tool, desc, x in nodes:
        s += f"""
  <g transform="translate({x}, 82)">
    <rect width="200" height="142" rx="12" fill="#081820" stroke="#1c5362" stroke-width="1.5"/>
    <rect width="200" height="4" rx="2" fill="url(#neon)"/>
    <text x="16" y="28" fill="#00d9ff" font-family="ui-monospace,Consolas,monospace" font-size="12" font-weight="700">{num}</text>
    <text x="16" y="54" fill="#f1fff9" font-family="Arial,Helvetica,sans-serif" font-size="16" font-weight="800">{title}</text>
    <text x="16" y="80" fill="#00f5a0" font-family="ui-monospace,Consolas,monospace" font-size="12">{tool}</text>
    <text x="16" y="112" fill="#8baea6" font-family="Arial,Helvetica,sans-serif" font-size="12">{desc}</text>
  </g>
"""
    # Connectors
    for x in [245, 475, 705, 935]:
        s += f"""
  <g transform="translate({x}, 150)">
    <path d="M 0 0 L 20 0" stroke="#00f5a0" stroke-width="2" stroke-dasharray="3 3"/>
    <path d="M 14 -5 L 22 0 L 14 5" fill="#00f5a0"/>
  </g>
"""
    s += "</svg>"
    (OUT / 'devsecops-pipeline.svg').write_text(s, encoding='utf-8')
    print("Generated devsecops-pipeline.svg")

# 3. ACTIVE OPERATIONS BOARD (width 1200, height 390)
def generate_active_missions():
    s = card_base(1200, 390, "Active Operations — Mission Status Board")
    s += """
  <!-- Header -->
  <text x="40" y="44" fill="#00f5a0" font-family="ui-monospace,Consolas,monospace" font-size="14" font-weight="700" letter-spacing="2">// ACTIVE MISSIONS — CURRENT OPERATION LOG</text>
  <text x="1160" y="44" fill="#00d9ff" font-family="ui-monospace,Consolas,monospace" font-size="12" text-anchor="end">cat ~/ops/active_missions.log</text>
  <path d="M 40 60 L 1160 60" stroke="#1c5362" stroke-opacity="0.6"/>
"""
    missions = [
        ("🔴 LIVE", "#ff5555", "NODUE PORTAL PRODUCTION", "Student NOC & Clearance Automation System", "React · TypeScript · Node.js · Firebase", "DEPLOYED", 75),
        ("🟡 DEV", "#f6c76a", "SIEM DASHBOARD & LOG INGEST", "Security event monitoring & threat detection engine", "Python · Elasticsearch · Splunk · Kibana", "IN BUILD", 125),
        ("🟡 DEV", "#f6c76a", "MODULAR PENTEST TOOLKIT", "Automated multi-threaded recon, port probe & exploits", "Python 3 · Bash · Raw Sockets · Asyncio", "IN BUILD", 175),
        ("🔵 LEARN", "#00d9ff", "ADVANCED PENETRATION TESTING", "Active Directory exploitation, Web PenTesting & Buffer Overflows", "HackTheBox · TryHackMe · OWASP", "ACTIVE", 225),
        ("🟢 OPEN", "#00f5a0", "OPEN-SOURCE COLLABORATIONS", "Open to collaborative security tooling, CTF teams & research", "GitHub · Discord · Remote Pair", "OPEN", 275),
        ("🎯 TARGET", "#bb86fc", "OSCP CERTIFICATION KILL-CHAIN", "Offensive Security Certified Professional milestone", "OffSec · 24-Hour Practical Exam", "GOAL 2027", 325)
    ]
    for status, color, title, desc, stack, tag, y in missions:
        s += f"""
  <g transform="translate(40, {y})">
    <rect width="1120" height="42" rx="8" fill="#081820" stroke="#16382c"/>
    <text x="16" y="26" fill="{color}" font-family="ui-monospace,Consolas,monospace" font-size="12" font-weight="700">{status}</text>
    <text x="120" y="26" fill="#f1fff9" font-family="Arial,Helvetica,sans-serif" font-size="14" font-weight="800">{title}</text>
    <text x="440" y="26" fill="#9dbcc8" font-family="Arial,Helvetica,sans-serif" font-size="13">{desc}</text>
    <text x="840" y="26" fill="#65dcb3" font-family="ui-monospace,Consolas,monospace" font-size="12">{stack}</text>
    <rect x="1025" y="10" width="80" height="22" rx="6" fill="{color}" fill-opacity="0.15" stroke="{color}" stroke-opacity="0.6"/>
    <text x="1065" y="25" fill="{color}" font-family="ui-monospace,Consolas,monospace" font-size="10" font-weight="700" text-anchor="middle">{tag}</text>
  </g>
"""
    s += "</svg>"
    (OUT / 'active-missions.svg').write_text(s, encoding='utf-8')
    print("Generated active-missions.svg")

# 4. MITRE ATT&CK MATRIX (width 1200, height 380)
def generate_mitre_matrix():
    s = card_base(1200, 380, "MITRE ATT&CK Framework Coverage")
    s += """
  <!-- Header -->
  <text x="40" y="44" fill="#00f5a0" font-family="ui-monospace,Consolas,monospace" font-size="14" font-weight="700" letter-spacing="2">// MITRE ATT&amp;CK® FRAMEWORK — PERSONAL COVERAGE MATRIX</text>
  <text x="1160" y="44" fill="#00d9ff" font-family="ui-monospace,Consolas,monospace" font-size="12" text-anchor="end">TACTICAL READINESS EVALUATION</text>
  <path d="M 40 60 L 1160 60" stroke="#1c5362" stroke-opacity="0.6"/>
"""
    tactics = [
        # Col 1
        ("Reconnaissance", 80, "Passive DNS, Shodan, Nmap scans", 40, 80),
        ("Initial Access", 70, "Web bugs (SQLi, XSS, SSRF), PoCs", 40, 138),
        ("Execution", 60, "Python/Bash scripts, Command injection", 40, 196),
        ("Persistence", 50, "Cron jobs, Web shells, Backdoors", 40, 254),
        ("Privilege Escalation", 60, "SUID binaries, Sudo misconfigs, Kernel", 40, 312),
        # Col 2
        ("Defense Evasion", 45, "Log tampering analysis, Obfuscation", 620, 80),
        ("Credential Access", 70, "Hashcat, John the Ripper, Shadow dumps", 620, 138),
        ("Discovery", 80, "Subnet scans, Local privilege enum", 620, 196),
        ("Lateral Movement", 50, "SSH pivoting, Port forwarding, SOCKS", 620, 254),
        ("Command & Control", 35, "Reverse shells, Staging listeners", 620, 312)
    ]
    for name, pct, tech, x, y in tactics:
        filled_w = int(140 * (pct / 100))
        s += f"""
  <g transform="translate({x}, {y})">
    <rect width="540" height="48" rx="8" fill="#081820" stroke="#16382c"/>
    <text x="16" y="22" fill="#f1fff9" font-family="Arial,Helvetica,sans-serif" font-size="13" font-weight="700">{name}</text>
    <text x="16" y="38" fill="#8baea6" font-family="ui-monospace,Consolas,monospace" font-size="11">{tech}</text>
    <!-- Progress Bar -->
    <rect x="350" y="16" width="140" height="16" rx="4" fill="#040b10" stroke="#1c5362"/>
    <rect x="350" y="16" width="{filled_w}" height="16" rx="4" fill="url(#neon)"/>
    <text x="502" y="29" fill="#00f5a0" font-family="ui-monospace,Consolas,monospace" font-size="11" font-weight="700">{pct}%</text>
  </g>
"""
    s += "</svg>"
    (OUT / 'mitre-matrix.svg').write_text(s, encoding='utf-8')
    print("Generated mitre-matrix.svg")

# 5. TACTICAL LAB (width 1200, height 210)
def generate_tactical_lab():
    s = card_base(1200, 210, "Tactical Lab — Interactive Snake & Ladder Browser Game")
    s += """
  <!-- Header -->
  <text x="40" y="44" fill="#00f5a0" font-family="ui-monospace,Consolas,monospace" font-size="14" font-weight="700" letter-spacing="2">// TACTICAL LAB — INTERACTIVE BROWSER GAME</text>
  <text x="1160" y="44" fill="#00d9ff" font-family="ui-monospace,Consolas,monospace" font-size="12" text-anchor="end">DEPLOYED ON GITHUB PAGES</text>
  <path d="M 40 60 L 1160 60" stroke="#1c5362" stroke-opacity="0.6"/>

  <g transform="translate(40, 78)">
    <rect width="1120" height="108" rx="12" fill="#081820" stroke="#1c5362"/>
    <text x="30" y="42" fill="#f1fff9" font-family="Arial,Helvetica,sans-serif" font-size="24" font-weight="800">🎲 Snake &amp; Ladder — Cyber Simulation Engine</text>
    <text x="30" y="70" fill="#9dbcc8" font-family="Arial,Helvetica,sans-serif" font-size="14">Built with Modern ES Modules, HTML5 Canvas, and Custom CSS Grid Physics. Test your tactical maneuvers live in browser.</text>
    <text x="30" y="92" fill="#65dcb3" font-family="ui-monospace,Consolas,monospace" font-size="12">https://bhavish-s.github.io/Bhavish-S/game/</text>

    <!-- Play Button -->
    <a href="https://bhavish-s.github.io/Bhavish-S/game/" target="_blank">
      <rect x="910" y="28" width="180" height="52" rx="10" fill="url(#neon)"/>
      <text x="1000" y="60" fill="#030d14" font-family="Arial,Helvetica,sans-serif" font-size="15" font-weight="900" text-anchor="middle" letter-spacing="1">LAUNCH GAME ➔</text>
    </a>
  </g>
</svg>"""
    (OUT / 'tactical-lab.svg').write_text(s, encoding='utf-8')
    print("Generated tactical-lab.svg")

# 6. CONNECT TERMINAL (width 1200, height 330)
def generate_connect_terminal():
    s = card_base(1200, 330, "Establish Secure Channel — Connect & Comms")
    s += """
  <!-- Header Bar -->
  <rect x="25" y="20" width="1150" height="36" rx="8" fill="#091b24" stroke="#1c5362" stroke-opacity="0.6"/>
  <circle cx="48" cy="38" r="6" fill="#ff5f56"/>
  <circle cx="68" cy="38" r="6" fill="#ffbd2e"/>
  <circle cx="88" cy="38" r="6" fill="#27c93f"/>
  <text x="110" y="43" fill="#65dcb3" font-family="ui-monospace,Consolas,monospace" font-size="13" letter-spacing="1">root@kali: ~ (SECURE TRANSMISSION HANDSHAKE // SSH PORT 22)</text>
  <text x="1150" y="43" fill="#00d9ff" font-family="ui-monospace,Consolas,monospace" font-size="12" text-anchor="end">[HANDSHAKE: READY]</text>

  <g transform="translate(40, 75)">
    <!-- Terminal Box -->
    <rect width="1120" height="230" rx="12" fill="#040b10" stroke="#16382c"/>
    <text x="25" y="38" fill="#00d9ff" font-family="ui-monospace,Consolas,monospace" font-size="14" font-weight="700">bhavish@kali:~$ <tspan fill="#f1fff9">ssh -T operator@bhavish-cyber.net</tspan></text>
    <text x="25" y="66" fill="#00f5a0" font-family="ui-monospace,Consolas,monospace" font-size="13">[+] Connection established. Public key accepted.</text>
    <text x="25" y="88" fill="#c7e8df" font-family="ui-monospace,Consolas,monospace" font-size="13">[+] Interactive shell session opened. Awaiting operator handshake...</text>

    <!-- Channels Grid -->
    <path d="M 25 106 L 1095 106" stroke="#1c5362" stroke-opacity="0.4"/>
    <text x="25" y="132" fill="#75ff9e" font-family="ui-monospace,Consolas,monospace" font-size="12" font-weight="700">// TRANSMISSION CHANNELS:</text>
    <text x="25" y="160" fill="#c7e8df" font-family="ui-monospace,Consolas,monospace" font-size="13">📧 Email       : <tspan fill="#00d9ff">bhavishgowda2006@gmail.com</tspan></text>
    <text x="25" y="184" fill="#c7e8df" font-family="ui-monospace,Consolas,monospace" font-size="13">💼 LinkedIn    : <tspan fill="#00d9ff">linkedin.com/in/bhavish-s-/</tspan></text>
    <text x="25" y="208" fill="#c7e8df" font-family="ui-monospace,Consolas,monospace" font-size="13">💬 Discord     : <tspan fill="#00d9ff">discord.gg/QvrjjptH2a</tspan>  |  X: twitter.com/Bhavish-S</text>

    <!-- Right Side: CTF / Battle Platforms -->
    <text x="600" y="132" fill="#00d9ff" font-family="ui-monospace,Consolas,monospace" font-size="12" font-weight="700">// CTF BATTLE STATIONS &amp; PRACTICE:</text>
    <text x="600" y="160" fill="#c7e8df" font-family="ui-monospace,Consolas,monospace" font-size="13">🟩 HackTheBox  : <tspan fill="#00f5a0">Active Operator</tspan> · Box Rooting &amp; CVE PoCs</text>
    <text x="600" y="184" fill="#c7e8df" font-family="ui-monospace,Consolas,monospace" font-size="13">🟧 TryHackMe   : <tspan fill="#00f5a0">Jr. PenTester Path</tspan> · SOC Level 1 Analyst</text>
    <text x="600" y="208" fill="#c7e8df" font-family="ui-monospace,Consolas,monospace" font-size="13">⚡ LeetCode    : <tspan fill="#00f5a0">Algorithms &amp; Problem Solving</tspan> (leetcode.com/u/bhavishs/)</text>
  </g>
</svg>"""
    (OUT / 'connect-terminal.svg').write_text(s, encoding='utf-8')
    print("Generated connect-terminal.svg")

if __name__ == '__main__':
    generate_threat_dossier()
    generate_pipeline()
    generate_active_missions()
    generate_mitre_matrix()
    generate_tactical_lab()
    generate_connect_terminal()

# 7. WEAPON SYSTEMS OVERVIEW (width 1200, height 280)
def generate_weapon_systems():
    s = card_base(1200, 280, "Weapon Systems — Tech & Security Arsenal")
    s += """
  <!-- Header -->
  <text x="40" y="44" fill="#00f5a0" font-family="ui-monospace,Consolas,monospace" font-size="14" font-weight="700" letter-spacing="2">// WEAPON SYSTEMS — TACTICAL ARSENAL OVERVIEW</text>
  <text x="1160" y="44" fill="#00d9ff" font-family="ui-monospace,Consolas,monospace" font-size="12" text-anchor="end">[ HARDENED TOOLING &amp; LANGUAGES ]</text>
  <path d="M 40 60 L 1160 60" stroke="#1c5362" stroke-opacity="0.6"/>

  <!-- 3 Columns -->
  <!-- Col 1: Offensive & Exploits -->
  <g transform="translate(40, 78)">
    <rect width="360" height="175" rx="12" fill="#081820" stroke="#1c5362"/>
    <rect width="360" height="4" rx="2" fill="url(#neon)"/>
    <text x="20" y="32" fill="#00f5a0" font-family="ui-monospace,Consolas,monospace" font-size="12" font-weight="700">01 // OFFENSIVE SECURITY</text>
    <text x="20" y="60" fill="#f1fff9" font-family="Arial,Helvetica,sans-serif" font-size="16" font-weight="800">PenTest &amp; Red Team Tools</text>
    <text x="20" y="88" fill="#c7e8df" font-family="ui-monospace,Consolas,monospace" font-size="12">Burp Suite Pro · Metasploit · Nmap</text>
    <text x="20" y="110" fill="#c7e8df" font-family="ui-monospace,Consolas,monospace" font-size="12">SQLMap · Hydra · John the Ripper</text>
    <text x="20" y="132" fill="#c7e8df" font-family="ui-monospace,Consolas,monospace" font-size="12">Gobuster · Wireshark · Tcpdump</text>
    <text x="20" y="156" fill="#65dcb3" font-family="ui-monospace,Consolas,monospace" font-size="11">[ KALI LINUX &amp; ARCH SUITE ]</text>
  </g>

  <!-- Col 2: Defensive & SIEM -->
  <g transform="translate(420, 78)">
    <rect width="360" height="175" rx="12" fill="#081820" stroke="#1c5362"/>
    <rect width="360" height="4" rx="2" fill="url(#cyan-glow)"/>
    <text x="20" y="32" fill="#00d9ff" font-family="ui-monospace,Consolas,monospace" font-size="12" font-weight="700">02 // DEFENSIVE &amp; SIEM</text>
    <text x="20" y="60" fill="#f1fff9" font-family="Arial,Helvetica,sans-serif" font-size="16" font-weight="800">SOC Operations &amp; IR</text>
    <text x="20" y="88" fill="#c7e8df" font-family="ui-monospace,Consolas,monospace" font-size="12">Splunk Enterprise · ELK Stack</text>
    <text x="20" y="110" fill="#c7e8df" font-family="ui-monospace,Consolas,monospace" font-size="12">Kibana Dashboards · Logstash</text>
    <text x="20" y="132" fill="#c7e8df" font-family="ui-monospace,Consolas,monospace" font-size="12">MITRE ATT&amp;CK · Threat Intel</text>
    <text x="20" y="156" fill="#65dcb3" font-family="ui-monospace,Consolas,monospace" font-size="11">[ SIEM LOG CORRELATION &amp; ALERTING ]</text>
  </g>

  <!-- Col 3: Languages & Automation -->
  <g transform="translate(800, 78)">
    <rect width="360" height="175" rx="12" fill="#081820" stroke="#1c5362"/>
    <rect width="360" height="4" rx="2" fill="url(#neon)"/>
    <text x="20" y="32" fill="#75ff9e" font-family="ui-monospace,Consolas,monospace" font-size="12" font-weight="700">03 // CODE &amp; DEVSECOPS</text>
    <text x="20" y="60" fill="#f1fff9" font-family="Arial,Helvetica,sans-serif" font-size="16" font-weight="800">Scripting &amp; Infrastructure</text>
    <text x="20" y="88" fill="#c7e8df" font-family="ui-monospace,Consolas,monospace" font-size="12">Python 3 · Bash · C / C++ · Rust</text>
    <text x="20" y="110" fill="#c7e8df" font-family="ui-monospace,Consolas,monospace" font-size="12">TypeScript · React · Node.js · Go</text>
    <text x="20" y="132" fill="#c7e8df" font-family="ui-monospace,Consolas,monospace" font-size="12">Docker · GitHub Actions · AWS · GCP</text>
    <text x="20" y="156" fill="#65dcb3" font-family="ui-monospace,Consolas,monospace" font-size="11">[ AUTOMATION &amp; SHIFT-LEFT DEFENSE ]</text>
  </g>
</svg>"""
    (OUT / 'weapon-systems.svg').write_text(s, encoding='utf-8')
    print("Generated weapon-systems.svg")

if __name__ == '__main__':
    generate_weapon_systems()
