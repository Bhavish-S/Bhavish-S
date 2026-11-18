function Chrome({ title, badge, children }: { title: string; badge?: string; children: React.ReactNode }) {
  return (
    <svg viewBox="0 0 400 240" fill="none" xmlns="http://www.w3.org/2000/svg" className="project-screenshot">
      <rect width="400" height="240" rx="8" fill="#0B0C10" />
      {/* title bar */}
      <rect width="400" height="32" fill="#0F1117" />
      <circle cx="16" cy="16" r="4" fill="#FF5F57" />
      <circle cx="30" cy="16" r="4" fill="#FEBC2E" />
      <circle cx="44" cy="16" r="4" fill="#28C840" />
      <text x="200" y="20" textAnchor="middle" fill="#5A5C6A" fontSize="9" fontFamily="Inter, sans-serif" fontWeight={500}>
        {title}
      </text>
      {badge && (
        <rect x={320} y="8" width={60} height={16} rx="4" fill="rgba(0,229,168,0.12)" />
      )}
      {badge && (
        <text x="350" y="19" textAnchor="middle" fill="#00E5A8" fontSize="8" fontFamily="Inter, sans-serif" fontWeight={700}>
          {badge}
        </text>
      )}
      {/* sidebar */}
      <rect x="0" y="32" width="72" height="208" fill="#0C0D12" />
      {Array.from({ length: 5 }).map((_, i) => (
        <rect key={i} x="8" y={44 + i * 32} width="56" height="20" rx="4" fill={i === 0 ? "rgba(0,229,168,0.12)" : "rgba(255,255,255,0.02)" } />
      ))}
      {/* divider */}
      <line x1="72" y1="32" x2="72" y2="240" stroke="rgba(255,255,255,0.04)" strokeWidth="1" />
      {children}
    </svg>
  );
}

/* ── 01. NoDue Portal ───────────────────────────── */
export function NoDuePortalScreenshot() {
  return (
    <Chrome title="NoDue Portal — Student Clearance" badge="LIVE">
      {/* progress steps */}
      {["Submit Request", "Department Check", "Library", "Accounts", "Approved"].map((step, i) => (
        <g key={i}>
          <circle cx={96 + i * 70} cy="58" r="9" fill={i < 3 ? "#00E5A8" : "rgba(255,255,255,0.04)"} />
          <text x={96 + i * 70} y="61" textAnchor="middle" fill={i < 3 ? "#08090D" : "#3A3C48"} fontSize="8" fontFamily="Inter, sans-serif" fontWeight={700}>{i + 1}</text>
          {i < 4 && <line x1={105 + i * 70} y1="58" x2={127 + i * 70} y2="58" stroke={i < 2 ? "#00E5A8" : "rgba(255,255,255,0.06)"} strokeWidth="1.5" />}
          <text x={96 + i * 70} y="76" textAnchor="middle" fill={i < 3 ? "#8B8D9A" : "#3A3C48"} fontSize="6" fontFamily="Inter, sans-serif">{step}</text>
        </g>
      ))}

      {/* department status cards */}
      {[
        { dept: "Computer Science Dept", status: "Cleared ✓", color: "#10B981" },
        { dept: "Central Library", status: "Cleared ✓", color: "#10B981" },
        { dept: "Student Hostel Facility", status: "Pending", color: "#FBBF24" },
        { dept: "Finance & Accounts", status: "Pending", color: "#FBBF24" },
      ].map((item, i) => (
        <g key={i}>
          <rect x="84" y={96 + i * 28} width="306" height="24" rx="4" fill="rgba(255,255,255,0.02)" />
          <rect x="84" y={96 + i * 28} width="3" height="24" rx="1.5" fill={item.color} />
          <text x="96" y={111 + i * 28} fill="#F0F0F5" fontSize="8.5" fontFamily="Inter, sans-serif" fontWeight={500}>{item.dept}</text>
          <rect x="330" y={100 + i * 28} width="52" height="15" rx="3" fill={item.color === "#10B981" ? "rgba(16,185,129,0.12)" : "rgba(251,191,36,0.12)"} />
          <text x="356" y={111 + i * 28} textAnchor="middle" fill={item.color} fontSize="7" fontFamily="Inter, sans-serif" fontWeight={600}>{item.status}</text>
        </g>
      ))}

      <text x="12" y="80" fill="#3A3C48" fontSize="7" fontFamily="Inter, sans-serif">📋 Clearances</text>
      <text x="12" y="112" fill="#5A5C6A" fontSize="7" fontFamily="Inter, sans-serif">My Dues</text>
      <text x="12" y="144" fill="#5A5C6A" fontSize="7" fontFamily="Inter, sans-serif">Audits</text>
      <text x="12" y="176" fill="#00E5A8" fontSize="7" fontFamily="Inter, sans-serif" fontWeight={600}>VERIFIED</text>
    </Chrome>
  );
}

/* ── 02. Budget Allocator ───────────────────────────── */
export function BudgetAllocatorScreenshot() {
  return (
    <Chrome title="Budget Allocator — Dynamic Distribution" badge="LIVE">
      <rect x="84" y="44" width="140" height="34" rx="6" fill="rgba(255,255,255,0.03)" />
      <text x="94" y="58" fill="#8B8D9A" fontSize="7" fontFamily="Inter, sans-serif">Total Income</text>
      <text x="94" y="72" fill="#F0F0F5" fontSize="12" fontFamily="Inter, sans-serif" fontWeight={700}>$12,500.00</text>

      <rect x="236" y="44" width="154" height="34" rx="6" fill="rgba(0,229,168,0.06)" stroke="rgba(0,229,168,0.2)" />
      <text x="246" y="58" fill="#00E5A8" fontSize="7" fontFamily="Inter, sans-serif">Remaining Available</text>
      <text x="246" y="72" fill="#00E5A8" fontSize="12" fontFamily="Inter, sans-serif" fontWeight={700}>$0.00 (Balanced)</text>

      {/* allocation sliders */}
      {[
        { name: "Fixed Operations & Infrastructure", pct: 45, val: "$5,625", col: "#38BDF8" },
        { name: "Security Hardening & Tooling", pct: 30, val: "$3,750", col: "#00E5A8" },
        { name: "Emergency Reserves & Liquidity", pct: 15, val: "$1,875", col: "#FBBF24" },
        { name: "Growth & Experimentation", pct: 10, val: "$1,250", col: "#A855F7" },
      ].map((item, i) => (
        <g key={i}>
          <text x="84" y={100 + i * 32} fill="#F0F0F5" fontSize="8" fontFamily="Inter, sans-serif">{item.name}</text>
          <text x="388" y={100 + i * 32} textAnchor="end" fill={item.col} fontSize="8" fontFamily="Inter, sans-serif" fontWeight={700}>{item.val} ({item.pct}%)</text>
          <rect x="84" y={106 + i * 32} width="306" height="8" rx="4" fill="rgba(255,255,255,0.04)" />
          <rect x="84" y={106 + i * 32} width={306 * (item.pct / 100)} height="8" rx="4" fill={item.col} />
        </g>
      ))}
    </Chrome>
  );
}

/* ── 03. Route Resilience Simulator ───────────────────────────── */
export function RouteResilienceScreenshot() {
  return (
    <Chrome title="Route Resilience — Network Simulator" badge="LIVE">
      {/* network topology graph */}
      <line x1="120" y1="80" x2="200" y2="70" stroke="#00E5A8" strokeWidth="2" strokeDasharray="3 3" />
      <line x1="200" y1="70" x2="280" y2="90" stroke="#00E5A8" strokeWidth="2" />
      <line x1="280" y1="90" x2="350" y2="140" stroke="#38BDF8" strokeWidth="2" />
      <line x1="120" y1="80" x2="160" y2="160" stroke="#EF4444" strokeWidth="1.5" strokeOpacity="0.4" />
      <line x1="160" y1="160" x2="260" y2="180" stroke="#38BDF8" strokeWidth="2" />
      <line x1="260" y1="180" x2="350" y2="140" stroke="#00E5A8" strokeWidth="2" />

      {/* Nodes */}
      <circle cx="120" cy="80" r="14" fill="#0C1D26" stroke="#00E5A8" strokeWidth="2" />
      <text x="120" y="83" textAnchor="middle" fill="#00E5A8" fontSize="8" fontWeight={700}>SRC</text>

      <circle cx="200" cy="70" r="12" fill="#0C1D26" stroke="#00E5A8" strokeWidth="2" />
      <text x="200" y="73" textAnchor="middle" fill="#FFFFFF" fontSize="7">N1</text>

      <circle cx="280" cy="90" r="12" fill="#0C1D26" stroke="#38BDF8" strokeWidth="2" />
      <text x="280" y="93" textAnchor="middle" fill="#FFFFFF" fontSize="7">N2</text>

      <circle cx="160" cy="160" r="12" fill="#201010" stroke="#EF4444" strokeWidth="2" />
      <text x="160" y="163" textAnchor="middle" fill="#EF4444" fontSize="7">DEAD</text>

      <circle cx="260" cy="180" r="12" fill="#0C1D26" stroke="#38BDF8" strokeWidth="2" />
      <text x="260" y="183" textAnchor="middle" fill="#FFFFFF" fontSize="7">N3</text>

      <circle cx="350" cy="140" r="14" fill="#0C1D26" stroke="#00E5A8" strokeWidth="2" />
      <text x="350" y="143" textAnchor="middle" fill="#00E5A8" fontSize="8" fontWeight={700}>DST</text>

      {/* Telemetry pill */}
      <rect x="84" y="200" width="140" height="24" rx="4" fill="rgba(0,229,168,0.08)" />
      <text x="94" y="215" fill="#00E5A8" fontSize="7.5" fontWeight={600}>Delivery Ratio: 99.4%</text>

      <rect x="234" y="200" width="156" height="24" rx="4" fill="rgba(56,189,248,0.08)" />
      <text x="244" y="215" fill="#38BDF8" fontSize="7.5" fontWeight={600}>Failover Latency: 42ms</text>
    </Chrome>
  );
}

/* ── 04. Novic Events ───────────────────────────── */
export function NovicEventsScreenshot() {
  return (
    <Chrome title="Novic Events — Cryptographic Ticketing" badge="LIVE">
      {/* Event Header */}
      <rect x="84" y="44" width="306" height="42" rx="6" fill="rgba(255,255,255,0.03)" />
      <text x="96" y="62" fill="#FFFFFF" fontSize="10" fontFamily="Inter, sans-serif" fontWeight={700}>CYBER_CON 2026 // ANNUAL HACKATHON</text>
      <text x="96" y="76" fill="#8B8D9A" fontSize="7.5">Registered Attendees: 480 / 500 · Hall 4 &amp; Central Auditorium</text>

      {/* QR Ticket Preview */}
      <g transform="translate(84, 98)">
        <rect width="120" height="120" rx="6" fill="#0D1E27" stroke="rgba(0,229,168,0.3)" />
        {/* QR Code grid simulation */}
        <rect x="16" y="16" width="32" height="32" fill="#00E5A8" />
        <rect x="72" y="16" width="32" height="32" fill="#00E5A8" />
        <rect x="16" y="72" width="32" height="32" fill="#00E5A8" />
        <rect x="56" y="56" width="16" height="16" fill="#00E5A8" />
        <rect x="80" y="80" width="24" height="24" fill="#38BDF8" />
      </g>

      {/* Ticket Details */}
      <g transform="translate(220, 98)">
        <text x="0" y="16" fill="#00E5A8" fontSize="8" fontWeight={700}>VIP ACCESS DELEGATE</text>
        <text x="0" y="32" fill="#FFFFFF" fontSize="11" fontWeight={700}>BHAVISH S</text>
        <text x="0" y="46" fill="#8B8D9A" fontSize="7.5">Token: #HMAC_942A_SECURE</text>
        <rect x="0" y="60" width="170" height="24" rx="4" fill="rgba(0,229,168,0.12)" />
        <text x="85" y="75" textAnchor="middle" fill="#00E5A8" fontSize="8" fontWeight={700}>STATUS: VERIFIED ENTRY ✓</text>
        <text x="0" y="104" fill="#5A5C6A" fontSize="7">Scanned at: 10:14:22 AM IST</text>
      </g>
    </Chrome>
  );
}

/* ── 05. SIEM Threat Monitor ───────────────────────────── */
export function SIEMDashboardScreenshot() {
  return (
    <Chrome title="SIEM Threat Telemetry Console" badge="DEV">
      <rect x="84" y="42" width="96" height="32" rx="4" fill="#0D1F29" stroke="rgba(56,189,248,0.2)" />
      <text x="94" y="56" fill="#8B8D9A" fontSize="7">Log Streams</text>
      <text x="94" y="68" fill="#38BDF8" fontSize="11" fontWeight={700}>1,420 eps</text>

      <rect x="188" y="42" width="96" height="32" rx="4" fill="#1C1810" stroke="rgba(245,158,11,0.2)" />
      <text x="198" y="56" fill="#8B8D9A" fontSize="7">Anomalies</text>
      <text x="198" y="68" fill="#F59E0B" fontSize="11" fontWeight={700}>14 Flagged</text>

      <rect x="292" y="42" width="98" height="32" rx="4" fill="#1F0D10" stroke="rgba(239,68,68,0.2)" />
      <text x="302" y="56" fill="#8B8D9A" fontSize="7">Threats Blocked</text>
      <text x="302" y="68" fill="#EF4444" fontSize="11" fontWeight={700}>3 Critical</text>

      {/* Log Feed */}
      {[
        { time: "11:24:02", ip: "192.168.1.104", type: "SSH Brute-Force Rate Spiked", stat: "IP DROPPED", col: "#EF4444" },
        { time: "11:23:48", ip: "10.0.4.12", type: "SQLi Pattern detected /api/v1", stat: "FILTERED", col: "#F59E0B" },
        { time: "11:23:15", ip: "172.16.0.8", type: "Port Sweep across range 20-80", stat: "ISOLATED", col: "#38BDF8" },
        { time: "11:22:50", ip: "192.168.1.1", type: "Firewall Rule reloaded cleanly", stat: "NORMAL", col: "#00E5A8" },
      ].map((log, i) => (
        <g key={i}>
          <rect x="84" y={84 + i * 34} width="306" height="28" rx="4" fill="rgba(255,255,255,0.02)" />
          <text x="92" y={101 + i * 34} fill="#5A5C6A" fontSize="7" fontFamily="monospace">{log.time}</text>
          <text x="136" y={101 + i * 34} fill="#8B8D9A" fontSize="7" fontFamily="monospace">{log.ip}</text>
          <text x="210" y={101 + i * 34} fill="#F0F0F5" fontSize="7.5">{log.type}</text>
          <rect x="330" y={91 + i * 34} width="52" height="14" rx="3" fill="rgba(255,255,255,0.04)" />
          <text x="356" y={101 + i * 34} textAnchor="middle" fill={log.col} fontSize="6.5" fontWeight={700}>{log.stat}</text>
        </g>
      ))}
    </Chrome>
  );
}

/* ── 06. PenTest Automation Suite ───────────────────────────── */
export function PenTestToolkitScreenshot() {
  return (
    <Chrome title="bhavish@kali:~/tools/recon" badge="ACTIVE">
      <rect x="84" y="42" width="306" height="182" rx="6" fill="#07131B" stroke="rgba(0,229,168,0.2)" />
      <g transform="translate(96, 62)" fontFamily="monospace" fontSize="8">
        <text x="0" y="0" fill="#00E5A8">$ python3 pentest_suite.py --target 10.10.11.40 --stealth</text>
        <text x="0" y="18" fill="#38BDF8">[+] Initializing asynchronous socket pool (threads=50)...</text>
        <text x="0" y="36" fill="#F0F0F5">[+] PORT 22/tcp  OPEN  (OpenSSH 8.9p1 Ubuntu)</text>
        <text x="0" y="54" fill="#F0F0F5">[+] PORT 80/tcp  OPEN  (Nginx 1.18.0 / Reverse Proxy)</text>
        <text x="0" y="72" fill="#F0F0F5">[+] PORT 443/tcp OPEN  (TLSv1.3 Strict-Transport-Security)</text>
        <text x="0" y="90" fill="#F59E0B">[!] AUDIT: Missing Content-Security-Policy header</text>
        <text x="0" y="108" fill="#F59E0B">[!] AUDIT: Weak Diffie-Hellman group detected</text>
        <text x="0" y="126" fill="#00E5A8">[+] Exporting report to ./reports/audit_2026.json... DONE</text>
        <text x="0" y="144" fill="#38BDF8">bhavish@kali:~/tools/recon$ <tspan fill="#00E5A8">_</tspan></text>
      </g>
    </Chrome>
  );
}

/* ── 07. Tactical Lab Simulator ───────────────────────────── */
export function TacticalLabScreenshot() {
  return (
    <Chrome title="Tactical Lab — Cybersecurity Game Simulator" badge="LIVE">
      <rect x="84" y="42" width="306" height="182" rx="6" fill="#081018" stroke="rgba(56,189,248,0.25)" />
      {/* 5x5 Matrix cells */}
      {Array.from({ length: 4 }).map((_, r) =>
        Array.from({ length: 5 }).map((_, c) => (
          <rect
            key={`${r}-${c}`}
            x={100 + c * 54}
            y={52 + r * 38}
            width="46"
            height="32"
            rx="4"
            fill={ (r + c) % 3 === 0 ? "rgba(0,229,168,0.08)" : "rgba(255,255,255,0.02)" }
            stroke="rgba(255,255,255,0.06)"
          />
        ))
      )}
      {/* Tactical nodes */}
      <circle cx="123" cy="68" r="8" fill="#00E5A8" />
      <text x="123" y="71" textAnchor="middle" fill="#08090D" fontSize="8" fontWeight={700}>START</text>

      <line x1="146" y1="140" x2="231" y2="70" stroke="#00E5A8" strokeWidth="2" strokeDasharray="2 2" />
      <text x="180" y="100" fill="#00E5A8" fontSize="7" fontWeight={700}>▲ LADDER</text>

      <line x1="285" y1="68" x2="200" y2="150" stroke="#EF4444" strokeWidth="2" />
      <text x="245" y="115" fill="#EF4444" fontSize="7" fontWeight={700}>▼ EXPLOIT</text>

      <circle cx="339" cy="182" r="8" fill="#38BDF8" />
      <text x="339" y="185" textAnchor="middle" fill="#08090D" fontSize="7" fontWeight={700}>ROOT</text>
    </Chrome>
  );
}
