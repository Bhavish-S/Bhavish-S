#!/usr/bin/env python3
# Regenerate the locally hosted green technology badges in assets/badges.
from pathlib import Path
import html, re
ROOT = Path(__file__).resolve().parents[1]
BADGES = ROOT / "assets" / "badges"
GROUPS = {
    "languages": ["Python", "JavaScript", "TypeScript", "C", "C++", "Java", "Go", "PHP", "Bash", "Rust", "Kotlin", "Swift"],
    "frontend-mobile": ["React", "Angular", "Vue", "Svelte", "Next.js", "HTML", "CSS", "Tailwind", "Bootstrap", "Flutter", "Android Studio"],
    "backend-databases": ["Node.js", "Express", "Django", "Flask", "FastAPI", "MongoDB", "MySQL", "PostgreSQL", "Redis", "Firebase", "GraphQL", "Supabase"],
    "cloud-devops": ["AWS", "Azure", "GCP", "Docker", "Kubernetes", "Terraform", "Ansible", "GitHub Actions", "Vercel", "Netlify"],
    "tools-platforms": ["Git", "GitHub", "Linux", "Figma", "Postman", "VS Code", "Neovim", "Notion", "Obsidian", "Blender"],
    "security-arsenal": ["Burp Suite", "Metasploit", "Nmap", "SQLMap", "Hydra", "John the Ripper", "Gobuster", "Splunk", "ELK", "Kibana", "SIEM", "MITRE ATT&CK", "Threat Intel", "PowerShell", "DevSecOps", "CTF"],
}
for labels in GROUPS.values():
    for label in labels:
        slug = "cpp" if label == "C++" else re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")
        initials = "".join(x[0] for x in re.findall(r"[A-Za-z0-9]+", label)[:2]).upper()
        for theme in ("dark", "light"):
            bg, fg, edge, chip, accent = (("#0D1510", "#E6EDF3", "#183C29", "#153521", "#B7FFCA") if theme == "dark" else ("#F3FAF5", "#173321", "#B7D8C2", "#DDEFE3", "#087A3C"))
            svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="168" height="38" viewBox="0 0 168 38" role="img" aria-label="{html.escape(label)} badge"><rect x=".7" y=".7" width="166.6" height="36.6" rx="8" fill="{bg}" stroke="{edge}"/><rect x="5" y="5" width="28" height="28" rx="6" fill="{chip}"/><text x="19" y="24" font-family="Arial,Helvetica,sans-serif" font-size="10" font-weight="700" fill="{accent}" text-anchor="middle">{html.escape(initials)}</text><text x="42" y="24" font-family="Arial,Helvetica,sans-serif" font-size="12" font-weight="700" fill="{fg}">{html.escape(label)}</text></svg>'''
            (BADGES / f"{slug}.{theme}.svg").write_text(svg, encoding="utf-8")
if __name__ == "__main__":
    print(f"Generated {sum(len(v) for v in GROUPS.values()) * 2} theme-aware badges in {BADGES}")
