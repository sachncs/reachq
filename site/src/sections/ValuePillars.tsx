import { motion } from 'framer-motion'
import { Cpu, GitBranch, Hash, Layers } from 'lucide-react'

const PILLARS = [
  {
    icon: GitBranch,
    title: 'Shortcut sets, done right.',
    body:
      'Build a JLS shortcut set for a dense digraph and answer reachability queries as efficiently as the paper allows — without rebuilding BFS from scratch on every call.',
    bullets: ['Theorem 2 algorithm', 'TC-pruning on by default'],
  },
  {
    icon: Layers,
    title: 'Hopsets for the shortest path.',
    body:
      'Construct a CFR hopset over a weighted digraph with optional TruncSSSP pruning, then run hop-bounded queries with a configurable (1 + ε) approximation.',
    bullets: ['Theorem 4 algorithm', '0.5× to 4× hops adjustable'],
  },
  {
    icon: Hash,
    title: 'Byte-stable. Always.',
    body:
      'Insertion-order vertex indexing, fixed RNG paths, and frozen dataclass configs. The same graph in, the same output — across processes, machines, and Python versions.',
    bullets: ['Deterministic seeds', 'Cross-process invariants'],
  },
  {
    icon: Cpu,
    title: 'Parallel when you ask for it.',
    body:
      'Opt into a process-pool dispatch for per-pivot BFS. Off by default so the easy path stays easy; on when your graph is dense enough to make it pay.',
    bullets: ['process-based parallelism', 'safe defaults, real speedup'],
  },
]

export function ValuePillars() {
  return (
    <section className="relative py-24 sm:py-32">
      <div className="container-page">
        <div className="mx-auto max-w-2xl text-center">
          <p className="eyebrow mb-4">Why reachq</p>
          <h2 className="display text-balance text-3xl font-semibold tracking-tightest sm:text-4xl">
            Reachability, built like <span className="gradient-brand">infrastructure</span>.
          </h2>
          <p className="mt-4 text-pretty text-base text-ink-soft">
            Four primitives. Each one paper-backed, each one reproducible, each
            one ready to drop into your graph pipeline.
          </p>
        </div>

        <div className="mt-16 grid grid-cols-1 gap-4 sm:grid-cols-2">
          {PILLARS.map((p, i) => (
            <motion.div
              key={p.title}
              initial={{ opacity: 0, y: 22 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: '-60px' }}
              transition={{
                duration: 0.65,
                ease: [0.16, 1, 0.3, 1],
                delay: i * 0.07,
              }}
              className="surface group relative overflow-hidden rounded-2xl p-7 transition-colors hover:border-line-strong"
            >
              <div className="pointer-events-none absolute inset-0 -z-10 opacity-0 transition-opacity duration-500 group-hover:opacity-100">
                <div className="absolute -top-32 -right-24 h-64 w-64 rounded-full bg-brand-500/15 blur-3xl" />
              </div>

              <div className="flex h-10 w-10 items-center justify-center rounded-xl border border-line bg-white/[0.04] text-ink-soft">
                <p.icon size={18} strokeWidth={1.6} />
              </div>

              <h3 className="mt-5 text-[19px] font-semibold tracking-tight">
                {p.title}
              </h3>
              <p className="mt-2.5 text-sm leading-relaxed text-ink-soft">
                {p.body}
              </p>

              <ul className="mt-5 flex flex-wrap gap-2">
                {p.bullets.map((b) => (
                  <li
                    key={b}
                    className="inline-flex items-center gap-1.5 rounded-full border border-line bg-white/[0.02] px-2.5 py-1 text-[11px] text-ink-muted"
                  >
                    <span className="h-1 w-1 rounded-full bg-accent-400" />
                    {b}
                  </li>
                ))}
              </ul>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}
