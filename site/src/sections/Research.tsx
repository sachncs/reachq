import { motion } from 'framer-motion'
import { CheckCircle2, FileText, Microscope, Workflow } from 'lucide-react'

const STEPS = [
  {
    icon: FileText,
    eyebrow: '1 · Citation',
    title: 'Sourced from the paper',
    body:
      'Direct implementations of Theorems 2 and 4 of Ashvinkumar, Bernstein, Probst Gutenberg & Saranurak (2026).',
  },
  {
    icon: Microscope,
    eyebrow: '2 · Refinement',
    title: 'Nine pragmatic improvements',
    body:
      'Adaptive sampling, TC-pruning, hop-bounded BFS, degree-ordered pivots, and more — all exposed as toggles.',
  },
  {
    icon: CheckCircle2,
    eyebrow: '3 · Invariants',
    title: '50-seed empirical checks',
    body:
      'Every lemma claim is re-validated across 50 random seeds. Failure means the lemma does not hold on the tested class.',
  },
  {
    icon: Workflow,
    eyebrow: '4 · Production path',
    title: 'Stable API, pure-Python wheel',
    body:
      'Typed entry points, JSON and Arrow IPC IO, NetworkX adapter, optional Cython/Numba/Rust backends.',
  },
]

export function Research() {
  return (
    <section id="research" className="relative py-24 sm:py-32">
      <div className="container-page">
        <div className="mx-auto max-w-2xl text-center">
          <p className="eyebrow mb-4">How it works</p>
          <h2 className="display text-balance text-3xl font-semibold tracking-tightest sm:text-4xl">
            From the paper,{' '}
            <span className="gradient-brand">all the way to your pipeline</span>.
          </h2>
          <p className="mt-4 text-pretty text-base text-ink-soft">
            reachq is a faithful port of the algorithms plus the engineering
            polish needed to use them in real code.
          </p>
        </div>

        <div className="relative mt-16">
          <div className="hairline absolute inset-x-0 top-7 hidden lg:block" />
          <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
            {STEPS.map((s, i) => (
              <motion.div
                key={s.eyebrow}
                initial={{ opacity: 0, y: 18 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: '-60px' }}
                transition={{
                  duration: 0.55,
                  ease: [0.16, 1, 0.3, 1],
                  delay: i * 0.08,
                }}
                className="relative"
              >
                <div className="surface relative rounded-2xl p-6">
                  <div className="flex h-12 w-12 items-center justify-center rounded-xl border border-line bg-bg-soft text-ink">
                    <s.icon size={18} strokeWidth={1.6} />
                  </div>
                  <p className="mt-5 font-mono text-[10px] uppercase tracking-[0.18em] text-brand-300">
                    {s.eyebrow}
                  </p>
                  <h3 className="mt-2 text-[15px] font-semibold tracking-tight">
                    {s.title}
                  </h3>
                  <p className="mt-2 text-[13.5px] leading-relaxed text-ink-soft">
                    {s.body}
                  </p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>

        <motion.figure
          initial={{ opacity: 0, y: 18 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-60px' }}
          transition={{ duration: 0.6 }}
          className="surface mx-auto mt-14 max-w-3xl rounded-2xl p-7 sm:p-9"
        >
          <blockquote className="text-balance text-center text-[17px] leading-relaxed text-ink sm:text-[19px]">
            <span className="text-ink-faint">“</span>
            Parallel reachability and shortest paths on non-sparse digraphs:
            near-linear work and sub-square-root depth.
            <span className="text-ink-faint">”</span>
          </blockquote>
          <figcaption className="mt-5 flex flex-wrap items-center justify-center gap-3 text-[13px] text-ink-muted">
            <span>Ashvinkumar, Bernstein, Probst Gutenberg, Saranurak</span>
            <span className="h-1 w-1 rounded-full bg-ink-faint" />
            <span className="font-mono">arXiv:2605.03892</span>
            <span className="h-1 w-1 rounded-full bg-ink-faint" />
            <span>2026</span>
          </figcaption>
        </motion.figure>
      </div>
    </section>
  )
}
