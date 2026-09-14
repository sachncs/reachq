import { motion } from 'framer-motion'
import { ArrowRight, Github, Star } from 'lucide-react'

export function CTA() {
  return (
    <section className="relative py-20 sm:py-28">
      <div className="container-page">
        <motion.div
          initial={{ opacity: 0, y: 22 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-80px' }}
          transition={{ duration: 0.7, ease: [0.16, 1, 0.3, 1] }}
          className="relative overflow-hidden rounded-3xl border border-line-soft bg-gradient-to-br from-white/[0.04] via-white/[0.02] to-white/[0.01] p-10 sm:p-16"
        >
          <div className="pointer-events-none absolute -top-32 left-1/3 -z-10 h-96 w-96 -translate-x-1/2 rounded-full bg-brand-500/20 blur-[120px]" />
          <div className="pointer-events-none absolute -bottom-32 right-0 -z-10 h-96 w-96 rounded-full bg-accent/15 blur-[120px]" />

          <div className="mx-auto max-w-2xl text-center">
            <h2 className="display text-balance text-4xl font-semibold tracking-tightest sm:text-[52px]">
              <span className="gradient-text">Make dense digraphs</span>
              <br />
              <span className="gradient-brand">fast to query.</span>
            </h2>
            <p className="mt-5 text-pretty text-base text-ink-soft sm:text-lg">
              Citation-grade reachability, in a few lines of Python. Star the
              repo, try the API, cite the paper.
            </p>

            <div className="mt-9 flex flex-col items-center justify-center gap-3 sm:flex-row">
              <a href="#install" className="btn-primary !px-6 !py-3 text-[14px] group">
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
                <Star size={14} className="text-amber-300/80" />
                Star on GitHub
                <Github size={14} className="ml-1 opacity-70" />
              </a>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  )
}
