export type ProjectStatus = "live" | "in development" | "standby";

export type ProjectCategory =
  | "cybersecurity"
  | "automation"
  | "software"
  | "web"
  | "research";

export type ArchitectureNode = {
  node: string;
  detail: string;
};

export type Project = {
  id: string;
  slug: string;
  number: string;
  title: string;
  shortTitle: string;
  category: string;
  tags: readonly ProjectCategory[];
  year: number | null;
  status: ProjectStatus;
  description: string;
  longDescription: string;
  problem: string;
  approach: string;
  technologies: readonly string[];
  highlights: readonly string[];
  architecture: readonly ArchitectureNode[];
  liveUrl: string | null;
  featuredImage: string | null;
  featured: boolean;
};

export const PROJECT_STATUS_LABEL: Record<ProjectStatus, string> = {
  live: "DEPLOYED",
  "in development": "IN DEVELOPMENT",
  standby: "STANDBY",
};

export const PROJECT_CATEGORIES: readonly {
  id: ProjectCategory | "all";
  label: string;
}[] = [
  { id: "all", label: "ALL" },
  { id: "cybersecurity", label: "CYBERSECURITY" },
  { id: "automation", label: "AUTOMATION" },
  { id: "software", label: "SOFTWARE" },
  { id: "web", label: "WEB" },
  { id: "research", label: "RESEARCH" },
] as const;

export const PROJECTS: readonly Project[] = [
  {
    id: "noc-portal",
    slug: "noc-portal",
    number: "01",
    title: "NoDue Portal",
    shortTitle: "NoDue Portal",
    category: "Student Clearance & Workflow Automation",
    tags: ["software", "automation", "web"],
    year: 2026,
    status: "live",
    description:
      "Automated campus clearance system replacing paper clearances with cryptographic verification and multi-department sign-offs.",
    longDescription:
      "NoDue Portal eliminates manual queue-based student clearance workflows across university departments (Library, Laboratory, Hostel, Accounts, and Academic Departments). Built with a high-performance React front end and Firebase/Node.js backend, it enforces strict role-based access control, real-time audit logging, and cryptographic certificate issuance upon unanimous clearance completion.",
    problem:
      "Graduating and semester students waste days standing in administrative queues across campus departments to obtain physical no-due signatures. Lost paper slips and manual fraud risk hinder administrative velocity.",
    approach:
      "Architected a centralized digital clearance engine where student identity requests flow sequentially or concurrently to authorized departmental faculty. Faculty dashboards display real-time student dues, allow instantaneous approval or hold with reason codes, and auto-issue verified clearance PDF tokens.",
    technologies: [
      "React",
      "TypeScript",
      "Node.js",
      "Express",
      "Firebase Firestore",
      "Tailwind CSS",
      "REST APIs",
    ],
    highlights: [
      "Multi-department simultaneous sign-off orchestration",
      "Role-based privilege separation (Student, Faculty HOD, Finance, Admin)",
      "Real-time due status tracking and instant push updates",
      "Cryptographic verification token generation for tamper resistance",
      "Comprehensive administrative audit trail of clearance actions",
    ],
    architecture: [
      { node: "CLIENT", detail: "React 19 + TypeScript SPA with responsive clearance dashboard" },
      { node: "AUTH / RBAC", detail: "Firebase Authentication with custom claims for faculty & students" },
      { node: "ENGINE", detail: "Node.js clearance orchestrator evaluating departmental gates" },
      { node: "DATA STORE", detail: "Cloud Firestore structured collections for dues, logs, and tokens" },
    ],
    liveUrl: "https://github.com/Bhavish-S/noc",
    featuredImage: null,
    featured: true,
  },
  {
    id: "budget-allocator",
    slug: "budget-allocator",
    number: "02",
    title: "Budget Allocator",
    shortTitle: "Budget Allocator",
    category: "Intelligent Financial Planning Platform",
    tags: ["software", "web", "automation"],
    year: 2026,
    status: "live",
    description:
      "Algorithmic budget allocation system featuring dynamic expense distribution, priority weighting, and real-time visualization.",
    longDescription:
      "Budget Allocator is a client-driven financial distribution engine that optimizes income apportionment across discretionary, operational, savings, and debt liabilities. Utilizing reactive state algorithms and clean visual telemetry, users set hard targets and allow the engine to dynamically balance category allocations while preventing deficit spending.",
    problem:
      "Individuals and student teams struggle with budgeting spreadsheets that lack reactive reallocation logic when unexpected capital constraints or shifting expenditure priorities emerge.",
    approach:
      "Developed a fluid TypeScript mathematical distribution model with constraint solvers that dynamically recalibrates downstream budget buckets as upstream amounts change, visualized via interactive charts.",
    technologies: [
      "React",
      "TypeScript",
      "Tailwind CSS",
      "Vite",
      "Chart.js",
      "LocalStorage Persistence",
    ],
    highlights: [
      "Dynamic mathematical allocation algorithms with constraint checks",
      "Interactive category re-weighting with real-time reactive feedback",
      "Zero-latency client-side calculations with local persistent state",
      "Clean dark telemetry visualization of cash flow distributions",
    ],
    architecture: [
      { node: "UI / VIEW", detail: "React dynamic slider and telemetry card interface" },
      { node: "CALC ENGINE", detail: "TypeScript mathematical distribution solver" },
      { node: "STORAGE", detail: "Encrypted local persistent browser state" },
    ],
    liveUrl: "https://github.com/Bhavish-S/budget-allocator",
    featuredImage: null,
    featured: true,
  },
  {
    id: "route-resilience",
    slug: "route-resilience",
    number: "03",
    title: "Route Resilience",
    shortTitle: "Route Resilience",
    category: "Network Fault-Tolerance & Graph Simulator",
    tags: ["cybersecurity", "research", "software"],
    year: 2026,
    status: "live",
    description:
      "Interactive network resilience graph simulator testing packet delivery and dynamic rerouting under adversarial node failures.",
    longDescription:
      "Route Resilience simulates packet transmission across complex network topologies during targeted denial-of-service attacks or infrastructure outages. Built on HTML5 Canvas and graph theory routing algorithms (Dijkstra, A*, and dynamic alternate path finding), it renders link latency, node health, and automatic route reconfiguration in real-time.",
    problem:
      "Network engineers and cybersecurity analysts require visual testbeds to understand how critical infrastructure reroutes traffic when key transit nodes are severed or compromised.",
    approach:
      "Engineered an in-browser graph visualization engine where users can build arbitrary network topologies, inject adversarial node kills, and watch traffic packets seamlessly pivot to redundant paths.",
    technologies: [
      "JavaScript",
      "HTML5 Canvas",
      "Graph Algorithms",
      "Network Modeling",
      "CSS3 Animations",
    ],
    highlights: [
      "Real-time graph physics and particle packet transit simulation",
      "Adversarial node kill and latency degradation injection",
      "Dynamic shortest path recalculation upon link disruption",
      "Resilience score telemetry and path bottleneck heatmaps",
    ],
    architecture: [
      { node: "CANVAS", detail: "60 FPS HTML5 Canvas graph rendering pipeline" },
      { node: "ALGORITHM", detail: "Real-time Dijkstra & k-shortest path rerouting algorithm" },
      { node: "TELEMETRY", detail: "Packet delivery ratio & network survivability metrics" },
    ],
    liveUrl: "https://github.com/Bhavish-S/Route_Resilience",
    featuredImage: null,
    featured: true,
  },
  {
    id: "novic-events",
    slug: "novic-events",
    number: "04",
    title: "Novic Events",
    shortTitle: "Novic Events",
    category: "Campus Event & QR Ticketing Engine",
    tags: ["software", "web", "automation"],
    year: 2026,
    status: "live",
    description:
      "Full-lifecycle event registration, cryptographic QR pass generation, and real-time door-scanning check-in system.",
    longDescription:
      "Novic Events powers campus tech symposia, hackathons, and cultural fests with automated attendee onboarding. It issues cryptographically signed QR access passes upon registration and enables organizers to verify tickets via an authenticated mobile camera scanner with instant anti-duplicate validation.",
    problem:
      "Event ticketing for large campus gatherings suffers from manual attendee lists, ticket forgery, and agonizingly slow door check-in lines.",
    approach:
      "Built a secure end-to-end ticketing platform with Node.js and cryptographic payload signing. Scanned QR codes are verified against server state in under 120ms to eliminate pass duplication.",
    technologies: [
      "Node.js",
      "Express",
      "REST APIs",
      "QR Cryptography",
      "HTML5 / Tailwind",
      "MongoDB",
    ],
    highlights: [
      "Automated cryptographic QR ticket generation upon registration",
      "Sub-150ms camera barcode scanner with duplicate detection",
      "Real-time attendee capacity and entry telemetry dashboard",
      "Exportable participant manifests and automated email notifications",
    ],
    architecture: [
      { node: "PORTAL", detail: "Responsive attendee registration and ticket showcase" },
      { node: "SCANNER", detail: "WebRTC camera-based QR decoding and validator" },
      { node: "BACKEND", detail: "Node.js REST API with tamper-proof HMAC verification" },
    ],
    liveUrl: "https://github.com/Bhavish-S/Novic-Events",
    featuredImage: null,
    featured: true,
  },
  {
    id: "siem-engine",
    slug: "siem-engine",
    number: "05",
    title: "SIEM Threat Monitor",
    shortTitle: "SIEM Threat Monitor",
    category: "Security Operations & Log Telemetry",
    tags: ["cybersecurity", "automation"],
    year: 2026,
    status: "in development",
    description:
      "Security Information & Event Management engine parsing audit logs, detecting anomalous brute-force attacks, and dispatching alerts.",
    longDescription:
      "A modular SIEM telemetry platform built for localized security monitoring. It ingests Linux auth logs, firewall syslogs, and web server hits, correlates suspicious anomaly spikes (such as SSH credential stuffing or SQL injection attempts), and fires automated defensive webhooks.",
    problem:
      "Commercial SIEM solutions are bloated and costly for small infrastructure footprints, leaving development servers blind to targeted attack vectors.",
    approach:
      "Designed an asynchronous Python log ingestion daemon utilizing regular expression rulesets and sliding-window rate counters to flag threat signatures in real-time.",
    technologies: [
      "Python 3",
      "Linux Syslog",
      "Elasticsearch",
      "Docker",
      "Bash",
      "Webhooks",
    ],
    highlights: [
      "Real-time log stream ingestion with regex threat pattern detection",
      "SSH brute-force detection with sliding-window time thresholds",
      "Instant security alert notifications via Discord/Slack webhooks",
      "Containerized architecture for one-command deployment",
    ],
    architecture: [
      { node: "INGESTION", detail: "Python async log file watcher monitoring /var/log/auth.log" },
      { node: "ANALYZER", detail: "Signature matching and IP reputation scoring pipeline" },
      { node: "DISPATCH", detail: "Automated alert webhooks and IPTables blocklist triggers" },
    ],
    liveUrl: "https://github.com/Bhavish-S",
    featuredImage: null,
    featured: true,
  },
  {
    id: "pentest-toolkit",
    slug: "pentest-toolkit",
    number: "06",
    title: "PenTest Automation Suite",
    shortTitle: "PenTest Suite",
    category: "Offensive Recon & Security Hardening",
    tags: ["cybersecurity", "automation"],
    year: 2026,
    status: "in development",
    description:
      "Modular security reconnaissance suite automating port discovery, banner grabbing, and security misconfiguration analysis.",
    longDescription:
      "The PenTest Automation Suite streamlines ethical hacking reconnaissance workflows. It performs asynchronous multi-threaded port scans, extracts daemon service banners, inspects HTTP security headers, and outputs structured JSON audit reports to accelerate attack-surface reduction.",
    problem:
      "Conducting initial security sweeps across dozens of endpoints requires chaining multiple CLI utilities, creating inconsistent documentation and slow feedback loops.",
    approach:
      "Crafted an all-in-one offensive utility using native Python socket programming, multithreading pools, and automated vulnerability heuristics to produce instant reconnaissance dossiers.",
    technologies: [
      "Python 3",
      "Socket Programming",
      "Bash Scripting",
      "Nmap Scripts",
      "Kali Linux",
    ],
    highlights: [
      "Fast multi-threaded TCP/UDP port enumeration engine",
      "Service banner grabbing with vulnerability signature cross-checks",
      "Automated HTTP security header compliance auditing",
      "Standardized JSON and Markdown audit report generation",
    ],
    architecture: [
      { node: "CLI SCANNER", detail: "Python multithreaded socket port scanner" },
      { node: "INSPECTOR", detail: "Protocol banner analyzer & header compliance checker" },
      { node: "REPORTER", detail: "Structured threat dossier and remediation generator" },
    ],
    liveUrl: "https://github.com/Bhavish-S",
    featuredImage: null,
    featured: true,
  },
  {
    id: "tactical-lab",
    slug: "tactical-lab",
    number: "07",
    title: "Tactical Lab Simulator",
    shortTitle: "Tactical Lab",
    category: "Interactive Cyber Simulation & Game",
    tags: ["cybersecurity", "web", "software"],
    year: 2026,
    status: "live",
    description:
      "Interactive browser-based cybersecurity training platform featuring dynamic game physics and simulated adversarial challenge nodes.",
    longDescription:
      "Hosted directly in the repository under /game, the Tactical Lab gamifies cybersecurity defensive training. Players navigate a cyber matrix board with animated dice mechanics, encountering firewalls, vulnerability ladders, and exploit slides designed to teach security principles through gameplay.",
    problem:
      "Traditional cybersecurity concepts can feel abstract and dry for junior engineers without interactive, gamified simulation sandboxes.",
    approach:
      "Created a zero-dependency ES module game engine running directly on GitHub Pages with dark neon styling, audio cues, and strategic defense cards.",
    technologies: [
      "JavaScript (ESM)",
      "HTML5 Canvas",
      "CSS3 Cyberpunk Theme",
      "GitHub Pages",
    ],
    highlights: [
      "Zero-dependency modular JavaScript game engine",
      "Interactive cyber matrix board with dynamic dice rolls and audio",
      "Adversarial encounter nodes simulating real cyber incidents",
      "Fully responsive and playable on both desktop and mobile",
    ],
    architecture: [
      { node: "ENGINE", detail: "Pure ES6 module state machine (game.mjs & engine.mjs)" },
      { node: "RENDERER", detail: "Hardware-accelerated CSS3 matrix grid with neon glow" },
      { node: "HOSTING", detail: "Live production deployment on GitHub Pages" },
    ],
    liveUrl: "https://bhavish-s.github.io/Bhavish-S/game/",
    featuredImage: null,
    featured: true,
  },
] as const;
