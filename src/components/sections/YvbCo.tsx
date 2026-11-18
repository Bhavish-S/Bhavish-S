import { motion, useReducedMotion } from "framer-motion";
import { Section } from "../layout/Section";
import { fadeUp } from "../../lib/motion";
import { TACTICAL_LAB_URL } from "../../data/site";

export function YvbCo() {
  const reduce = useReducedMotion();

  return (
    <Section id="lab" className="studio-section">
      <div className="container">
        <motion.div
          variants={fadeUp}
          initial={reduce ? false : "hidden"}
          whileInView={reduce ? undefined : "show"}
          viewport={{ once: true }}
          className="studio-card"
        >
          <div className="studio-card-header">
            <div>
              <span className="section-label">INTERACTIVE SANDBOX</span>
            </div>
            <h3 className="studio-title">
              TACTICAL <span className="studio-amp">LAB</span>
            </h3>
            <p className="studio-tagline">Gamified defensive <em>simulation.</em></p>
          </div>
          <div className="studio-card-body">
            <p className="studio-desc">
              An interactive browser-based cybersecurity training simulation hosted directly in this repository.
              Navigate the cyber matrix board, roll against adversary nodes, climb vulnerability ladders, and master
              defensive security principles through gameplay.
            </p>
            <a
              href={TACTICAL_LAB_URL}
              target="_blank"
              rel="noreferrer"
              className="studio-link"
            >
              Launch Tactical Lab &#x2197;
            </a>
          </div>
        </motion.div>
      </div>
    </Section>
  );
}
