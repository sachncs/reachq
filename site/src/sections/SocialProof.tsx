import { motion } from 'framer-motion'

const PROOF = [
  { label: 'Based on', value: 'Ashvinkumar et al., 2026' },
  { label: 'License', value: 'MIT' },
  { label: 'Stack', value: 'Pure Python · NumPy · SciPy' },
  { label: 'Stability', value: 'Byte-stable across processes' },
]

export function SocialProof() {
  return (
    <section className="relative border-y border-line-soft bg-bg-soft/50 py-6">
      <div className="container-page flex flex-col items-center gap-4 text-center sm:flex-row sm:justify-between sm:text-left">
        <p className="eyebrow">Production-shaped. Research-grade.</p>
        <div className="flex flex-wrap items-center justify-center gap-x-8 gap-y-3">
          {PROOF.map((p) => (
            <motion.div
              key={p.label}
              initial={{ opacity: 0, y: 8 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: '-40px' }}
              transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
              className="flex items-baseline gap-2"
            >
              <span className="text-[10px] uppercase tracking-[0.18em] text-ink-faint">
                {p.label}
              </span>
              <span className="text-[13px] font-medium text-ink-soft">
                {p.value}
              </span>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}
