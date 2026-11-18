const SKILLS = [
  "Python",
  "Linux / Kali",
  "Docker",
  "Kubernetes",
  "React",
  "TypeScript",
  "Node.js",
  "PostgreSQL",
  "SIEM & Splunk",
  "DevSecOps",
  "Nmap / Wireshark",
  "REST APIs",
  "GitHub Actions",
  "Firebase",
  "AWS Cloud",
  "Vite",
];

export function TechMarquee() {
  const doubled = [...SKILLS, ...SKILLS];

  return (
    <div className="marquee-section" aria-hidden="true">
      <div className="marquee-track">
        {doubled.map((skill, i) => (
          <span key={`${skill}-${i}`} className="marquee-item">
            {skill}
            <span className="marquee-separator"> &#10022; </span>
          </span>
        ))}
      </div>
    </div>
  );
}

export default TechMarquee;
