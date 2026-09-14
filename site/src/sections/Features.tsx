import { motion } from 'framer-motion'
import {
  Binary,
  CircuitBoard,
  Cog,
  GitFork,
  Layers,
  Shield,
} from 'lucide-react'

const FEATURES = [
  {
    icon: GitFork,
    title: 'JLS shortcut set',
    body:
      'A near-linear work, sub-square-root depth construction for parallel reachability on dense digraphs.',
    tag: 'Theor. 2',
  },
  {
    icon: Layers,
    title: 'CFR hopset',
    body:
      'A hop-bounded construction for approximate single-source shortest paths, with optional (1+ε) guarantee.',
    tag: 'Theor. 4',
  },
  {
    icon: CircuitBoard,
    title: 'Boolean-semiring transitive closure',
    body:
      'A full closure primitive with an explicit max_pairs budget and a clean error on overflow.',
    tag: 'Primitive',
  },
  {
    icon: Binary,
    title: 'Insertion-order indexing',
    body:
      'Vertices keep their stable insertion order across Digraph, WeightedDigraph, CSR, and JSON.',
    tag: 'Core',
  },
  {
    icon: Cog,
    title: '9 refinement toggles',
    body:
      'A frozen RefinementConfig dataclass — turn every published improvement on or off, no surprises.',
    tag: 'Tuning',
  },
  {
    icon: Shield,
    title: 'Reproducibility contract',
    body:
      'Deterministic seeds, frozen configurations, and 50-seed lemma tests across the suite.',
    tag: 'Quality',
  },
]

export function Features() {
  return (
    <section id="features" className="relative py-24 sm:py-32">
      <div className="container-page">
        <div className="mx-auto max-w-2xl text-center">
          <p className="eyebrow mb-4">What ships</p>
          <h2 className="display text-balance text-3xl font-semibold tracking-tightest sm:text-4xl">
            Built from the algorithms,{' '}
            <span className="gradient-brand">one paper at a time</span>.
          </h2>
          <p className="mt-4 text-pretty text-base text-ink-soft">
            Every feature here exists because the paper proves it works —
            and you can switch each one independently.
          </p>
        </div>

        <div className="mt-16 grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {FEATURES.map((f, i) => (
            <motion.div
              key={f.title}
              initial={{ opacity: 0, y: 18 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: '-40px' }}
              transition={{
                duration: 0.55,
                ease: [0.16, 1, 0.3, 1],
                delay: (i % 3) * 0.06,
              }}
              className="group surface relative overflow-hidden rounded-2xl p-6 transition-all hover:border-line-strong"
            >
              <div className="flex items-start justify-between">
                <div className="flex h-9 w-9 items-center justify-center rounded-lg border border-line bg-white/[0.04] text-ink-soft transition-colors group-hover:text-ink">
                  <f.icon size={16} strokeWidth={1.6} />
                </div>
                <span className="rounded-full border border-line bg-white/[0.02] px-2 py-0.5 font-mono text-[10px] uppercase tracking-wider text-ink-faint">
                  {f.tag}
                </span>
              </div>

              <h3 className="mt-5 text-[15px] font-semibold tracking-tight">
                {f.title}
              </h3>
              <p className="mt-2 text-[13.5px] leading-relaxed text-ink-soft">
                {f.body}
              </p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}
