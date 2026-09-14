import { motion } from 'framer-motion'
import { GraphCanvas } from '../components/GraphCanvas'
import { ArrowRight, Github, Sparkles, Star } from 'lucide-react'

const fadeUp = {
  hidden: { opacity: 0, y: 16 },
  show: (i: number) => ({
    opacity: 1,
    y: 0,
    transition: {
      delay: 0.06 * i + 0.1,
      duration: 0.7,
      ease: [0.16, 1, 0.3, 1] as [number, number, number, number],
    },
  }),
}

export function Hero() {
  return (
    <section
      id="top"
      className="relative isolate overflow-hidden pt-32 pb-24 sm:pt-40 sm:pb-32 lg:pt-48 lg:pb-40"
    >
      {/* ambient background */}
      <div className="pointer-events-none absolute inset-0 -z-10 bg-mesh-1 opacity-90" />
      <div className="pointer-events-none absolute inset-x-0 top-0 -z-10 h-[80vh] bg-grid-fade opacity-80" />
      <div className="pointer-events-none absolute inset-0 -z-10 bg-noise opacity-40 mix-blend-overlay" />
      <div className="pointer-events-none absolute inset-x-0 top-0 -z-10 h-px bg-gradient-to-r from-transparent via-white/15 to-transparent" />

      {/* hero animated graph backdrop */}
      <div className="pointer-events-none absolute inset-0 -z-10 mask-radial opacity-70">
        <GraphCanvas
          className="absolute left-1/2 top-1/2 h-[820px] w-[820px] -translate-x-1/2 -translate-y-1/2 sm:h-[940px] sm:w-[940px]"
          size={820}
          n={48}
        />
      </div>

      <div className="container-page relative">
        <motion.div
          initial="hidden"
          animate="show"
          variants={{
            hidden: {},
            show: { transition: { staggerChildren: 0.08 } },
          }}
          className="flex flex-col items-center text-center"
        >
          <motion.span
            custom={0}
            variants={fadeUp}
            className="pill mb-7 !py-1.5 !px-3.5"
          >
            <span className="pill-dot animate-pulseGlow" />
            <span className="text-ink-soft">Built on Ashvinkumar et al. (2026)</span>
            <span className="hidden h-3 w-px bg-line sm:block" />
            <Star size={11} className="text-amber-300/80" strokeWidth={1.8} />
            <span className="text-ink-muted">v0.9.0</span>
          </motion.span>

          <motion.h1
            custom={1}
            variants={fadeUp}
            className="display max-w-4xl text-balance text-[44px] font-semibold leading-[1.04] tracking-tightest sm:text-[64px] lg:text-[78px]"
          >
            <span className="gradient-text">Graph reachability,</span>
            <br />
            <span className="gradient-brand">queryable.</span>
          </motion.h1>

          <motion.p
            custom={2}
            variants={fadeUp}
            className="mt-6 max-w-2xl text-pretty text-base leading-relaxed text-ink-soft sm:text-lg"
          >
            <strong className="text-ink">reachq</strong> builds parallel shortcut
            sets and hopsets for dense directed graphs — deterministic,
            reproducible, and citation-grade. Pure Python. Optional process
            parallelism. Designed for the algorithms behind the paper.
          </motion.p>

          <motion.div
            custom={3}
            variants={fadeUp}
            className="mt-10 flex flex-col items-center gap-3 sm:flex-row sm:gap-3"
          >
            <a href="#install" className="btn-primary group !px-6 !py-3 text-[14px]">
              Install reachq
              <ArrowRight
                size={15}
                className="transition-transform group-hover:translate-x-0.5"
              />
            </a>
            <a
              href="https://github.com/sachncs/reachq"
              target="_blank"
              rel="noreferrer"
              className="btn-ghost !px-6 !py-3 text-[14px]"
            >
              <Github size={15} /> Star on GitHub
            </a>
          </motion.div>

          <motion.div
            custom={4}
            variants={fadeUp}
            className="mt-10 flex items-center gap-6 text-[12px] text-ink-muted"
          >
            <span className="hidden sm:inline-flex items-center gap-2">
              <span className="h-1 w-1 rounded-full bg-emerald-400" /> MIT licensed
            </span>
            <span className="inline-flex items-center gap-2">
              <Sparkles size={11} strokeWidth={1.6} /> Pure Python ≥ 3.10
            </span>
            <span className="hidden sm:inline-flex items-center gap-2">
              <span className="h-1 w-1 rounded-full bg-brand-400" /> numpy · scipy
            </span>
          </motion.div>
        </motion.div>
      </div>

      {/* fade-to-bg at the bottom */}
      <div className="pointer-events-none absolute inset-x-0 bottom-0 h-32 bg-gradient-to-b from-transparent to-bg" />
    </section>
  )
}
