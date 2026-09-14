import { motion } from 'framer-motion'
import { Check, Copy } from 'lucide-react'
import { useState } from 'react'

const STEPS = [
  'Pure-Python wheel · numpy · scipy',
  'MIT licensed · no telemetry',
  'Runs on Python 3.10 – 3.13',
]

export function Install() {
  const [copied, setCopied] = useState(false)
  const installCmd = 'pip install -e ".[dev]"  # from source for now'

  const copy = async () => {
    try {
      await navigator.clipboard.writeText(installCmd)
      setCopied(true)
      window.setTimeout(() => setCopied(false), 1500)
    } catch {
      /* no-op */
    }
  }

  return (
    <section id="install" className="relative py-24 sm:py-32">
      <div className="container-narrow">
        <motion.div
          initial={{ opacity: 0, y: 22 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-100px' }}
          transition={{ duration: 0.7, ease: [0.16, 1, 0.3, 1] }}
          className="surface-strong relative overflow-hidden rounded-3xl p-8 sm:p-12"
        >
          <div className="pointer-events-none absolute -top-32 left-1/2 -z-10 h-80 w-[40rem] -translate-x-1/2 rounded-full bg-brand-500/15 blur-3xl" />
          <div className="pointer-events-none absolute inset-0 -z-10 bg-mesh-1 opacity-50" />

          <p className="eyebrow text-center">Get started in 30 seconds</p>
          <h2 className="display mt-3 text-center text-balance text-3xl font-semibold tracking-tightest sm:text-[40px]">
            Install, build, query.
          </h2>
          <p className="mx-auto mt-4 max-w-xl text-center text-pretty text-base text-ink-soft">
            Clone the repo and install in editable mode. A PyPI release is on
            the roadmap.
          </p>

          <div className="mx-auto mt-8 max-w-2xl">
            <div className="flex items-center justify-between rounded-t-2xl border border-line-soft border-b-0 bg-black/40 px-4 py-3">
              <div className="flex items-center gap-2">
                <span className="h-2.5 w-2.5 rounded-full bg-[#FF5F57]/70" />
                <span className="h-2.5 w-2.5 rounded-full bg-[#FEBC2E]/70" />
                <span className="h-2.5 w-2.5 rounded-full bg-[#28C840]/70" />
              </div>
              <span className="font-mono text-[12px] text-ink-faint">terminal</span>
              <button
                onClick={copy}
                aria-label="Copy install command"
                className="inline-flex items-center gap-1.5 rounded-md border border-line bg-white/[0.04] px-2.5 py-1 text-[11px] text-ink-soft transition-colors hover:bg-white/[0.08]"
              >
                {copied ? <Check size={11} /> : <Copy size={11} />}
                {copied ? 'Copied' : 'Copy'}
              </button>
            </div>
            <pre className="overflow-x-auto rounded-b-2xl border border-line-soft border-t-0 bg-black/40 p-5 font-mono text-[13px] leading-[1.7] text-ink-soft">
              <code>
                <span style={{ color: '#a5b4fc' }}>$</span>{' '}
                <span style={{ color: '#e4e4e7' }}>git clone</span>{' '}
                <span style={{ color: '#86efac' }}>
                  https://github.com/sachncs/reachq.git
                </span>
                {'\n'}
                <span style={{ color: '#a5b4fc' }}>$</span>{' '}
                <span style={{ color: '#e4e4e7' }}>cd</span>{' '}
                <span style={{ color: '#e4e4e7' }}>reachq</span>
                {'\n'}
                <span style={{ color: '#a5b4fc' }}>$</span>{' '}
                <span style={{ color: '#e4e4e7' }}>{installCmd}</span>
              </code>
            </pre>
          </div>

          <ul className="mx-auto mt-8 flex max-w-2xl flex-col items-stretch gap-2 sm:flex-row sm:items-center sm:justify-center sm:gap-6">
            {STEPS.map((s) => (
              <li
                key={s}
                className="inline-flex items-center justify-center gap-2 text-[13px] text-ink-soft"
              >
                <Check size={13} className="text-accent-400" strokeWidth={2.2} />
                {s}
              </li>
            ))}
          </ul>
        </motion.div>
      </div>
    </section>
  )
}
