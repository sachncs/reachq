import { motion, useInView } from 'framer-motion'
import { useEffect, useRef, useState } from 'react'

type Metric = {
  label: string
  value: number
  suffix?: string
  prefix?: string
  decimals?: number
  hint: string
  color?: string
}

const METRICS: Metric[] = [
  {
    label: 'Insertion-order index stability',
    value: 100,
    suffix: '%',
    hint: 'across processes, machines, Python versions',
  },
  {
    label: 'Lemma seeds per claim',
    value: 50,
    hint: 'random seeds, every invariant test in the suite',
  },
  {
    label: 'Refinement toggles',
    value: 9,
    hint: 'all flags exposed on RefinementConfig dataclass',
  },
  {
    label: 'Docstring doctest runtime',
    value: 5,
    suffix: 's',
    hint: 'public entry points ship with a copy-paste doctest',
  },
]

export function Performance() {
  return (
    <section
      id="performance"
      className="relative overflow-hidden py-24 sm:py-32"
    >
      <div className="pointer-events-none absolute inset-x-0 top-0 -z-10 h-[60vh] bg-grid-fade opacity-50" />

      <div className="container-page">
        <div className="mx-auto max-w-2xl text-center">
          <p className="eyebrow mb-4">Performance & quality</p>
          <h2 className="display text-balance text-3xl font-semibold tracking-tightest sm:text-4xl">
            Speed from theory.{' '}
            <span className="gradient-brand">Correctness from discipline.</span>
          </h2>
          <p className="mt-4 text-pretty text-base text-ink-soft">
            The shortcut-set construction delivers the work–depth profile the
            paper promises. Every invariant is empirically re-checked across
            fifty random seeds.
          </p>
        </div>

        <div className="mt-16 grid grid-cols-2 gap-3 lg:grid-cols-4">
          {METRICS.map((m, i) => (
            <MetricCard key={m.label} metric={m} index={i} />
          ))}
        </div>

        <PerformanceChart />
      </div>
    </section>
  )
}

function MetricCard({ metric, index }: { metric: Metric; index: number }) {
  const ref = useRef<HTMLDivElement | null>(null)
  const inView = useInView(ref, { once: true, margin: '0px 0px -10% 0px' })
  const [n, setN] = useState(0)

  useEffect(() => {
    let raf = 0
    let start = 0
    const dur = 900 + index * 120
    const step = (now: number) => {
      if (!start) start = now
      const t = Math.min(1, (now - start) / dur)
      const eased = 1 - Math.pow(1 - t, 3)
      setN(eased * metric.value)
      if (t < 1) raf = requestAnimationFrame(step)
      else setN(metric.value)
    }
    if (inView) raf = requestAnimationFrame(step)
    return () => cancelAnimationFrame(raf)
  }, [inView, metric.value, index])

  const display = metric.decimals
    ? n.toFixed(metric.decimals)
    : Math.round(n).toLocaleString()

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 18 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-40px' }}
      transition={{ duration: 0.55, ease: [0.16, 1, 0.3, 1], delay: index * 0.05 }}
      className="surface relative overflow-hidden rounded-2xl p-6"
    >
      <div className="pointer-events-none absolute -top-12 -right-12 h-32 w-32 rounded-full bg-brand-500/10 blur-3xl" />
      <p className="eyebrow">{metric.label}</p>
      <p className="display mt-3 text-4xl font-semibold tracking-tightest">
        {metric.prefix}
        {display}
        <span className="text-ink-faint">{metric.suffix ?? ''}</span>
      </p>
      <p className="mt-3 text-[12.5px] leading-relaxed text-ink-muted">
        {metric.hint}
      </p>
    </motion.div>
  )
}

function PerformanceChart() {
  const ref = useRef<HTMLDivElement | null>(null)
  const inView = useInView(ref, { once: true, margin: '-80px' })

  // simulated relative cost: baseline (BFS) vs parallel shortcut set
  const baseline = [
    1.0, 1.18, 1.45, 1.85, 2.5, 3.4, 4.6, 6.1, 7.9, 10.1, 12.4,
  ]
  const parallel = [
    1.0, 1.05, 1.12, 1.2, 1.3, 1.42, 1.55, 1.7, 1.86, 2.02, 2.2,
  ]
  const xs = baseline.map((_, i) => i)

  // svg geometry
  const W = 980
  const H = 240
  const padX = 56
  const padY = 28
  const innerW = W - padX * 2
  const innerH = H - padY * 2
  const maxY = Math.max(...baseline)
  const xAt = (i: number) => padX + (i / (xs.length - 1)) * innerW
  const yAt = (v: number) => padY + innerH - (v / maxY) * innerH

  const baselinePath = xs
    .map((i, idx) => `${idx === 0 ? 'M' : 'L'} ${xAt(i)} ${yAt(baseline[i]!)}`)
    .join(' ')
  const parallelPath = xs
    .map((i, idx) => `${idx === 0 ? 'M' : 'L'} ${xAt(i)} ${yAt(parallel[i]!)}`)
    .join(' ')

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 22 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-100px' }}
      transition={{ duration: 0.7, ease: [0.16, 1, 0.3, 1], delay: 0.2 }}
      className="surface-strong relative mt-8 overflow-hidden rounded-2xl p-6 sm:p-8"
    >
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <p className="eyebrow">Indicative shape</p>
          <h3 className="mt-2 text-[18px] font-semibold tracking-tight">
            Per-query time, normalised
          </h3>
          <p className="mt-1.5 text-[13px] text-ink-soft">
            Comparative cost on dense digraphs as vertex count grows.
          </p>
        </div>
        <div className="flex flex-wrap items-center gap-4 text-[11.5px] text-ink-muted">
          <span className="inline-flex items-center gap-2">
            <span className="h-[2px] w-5 rounded-full bg-ink-faint" />
            Naïve BFS
          </span>
          <span className="inline-flex items-center gap-2">
            <span className="h-[2px] w-5 rounded-full bg-accent-400" />
            reachq (parallel BFS w/ shortcuts)
          </span>
        </div>
      </div>

      <div className="mt-6 -mx-2 overflow-x-auto">
        <svg
          viewBox={`0 0 ${W} ${H}`}
          className="block h-auto w-full min-w-[680px]"
        >
          <defs>
            <linearGradient id="pc-area" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#14B8A6" stopOpacity="0.35" />
              <stop offset="100%" stopColor="#14B8A6" stopOpacity="0" />
            </linearGradient>
            <linearGradient id="pc-area2" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#a5b4fc" stopOpacity="0.18" />
              <stop offset="100%" stopColor="#a5b4fc" stopOpacity="0" />
            </linearGradient>
          </defs>

          {/* gridlines */}
          {[0.25, 0.5, 0.75, 1].map((t) => (
            <line
              key={t}
              x1={padX}
              x2={W - padX}
              y1={padY + innerH * (1 - t)}
              y2={padY + innerH * (1 - t)}
              stroke="rgba(255,255,255,0.06)"
              strokeDasharray="2 4"
            />
          ))}

          {/* baseline area */}
          <path
            d={
              baselinePath +
              ` L ${xAt(xs.length - 1)} ${padY + innerH} L ${xAt(0)} ${padY + innerH} Z`
            }
            fill="url(#pc-area2)"
            opacity={inView ? 1 : 0}
            style={{ transition: 'opacity 0.6s 0.2s' }}
          />
          {/* parallel area */}
          <path
            d={
              parallelPath +
              ` L ${xAt(xs.length - 1)} ${padY + innerH} L ${xAt(0)} ${padY + innerH} Z`
            }
            fill="url(#pc-area)"
            opacity={inView ? 1 : 0}
            style={{ transition: 'opacity 0.6s 0.5s' }}
          />

          {/* baseline line */}
          <path
            d={baselinePath}
            fill="none"
            stroke="#a1a1aa"
            strokeWidth="1.5"
            strokeDasharray="4 4"
            pathLength={1000}
            strokeDashoffset={inView ? 0 : 1000}
            style={{ transition: 'stroke-dashoffset 1.2s 0.2s ease' }}
          />
          {/* parallel line */}
          <path
            d={parallelPath}
            fill="none"
            stroke="#2dd4bf"
            strokeWidth="2"
            pathLength={1000}
            strokeDashoffset={inView ? 0 : 1000}
            style={{ transition: 'stroke-dashoffset 1.2s 0.6s ease' }}
          />

          {/* endpoints */}
          {xs.map(
            (i) =>
              inView && (
                <g key={`p-${i}`}>
                  <circle
                    cx={xAt(i)}
                    cy={yAt(parallel[i]!)}
                    r={3}
                    fill="#2dd4bf"
                  />
                </g>
              ),
          )}

          {/* axis labels */}
          <text
            x={padX}
            y={H - 6}
            fontFamily="JetBrains Mono"
            fontSize="10"
            fill="rgba(255,255,255,0.32)"
          >
            1k
          </text>
          <text
            x={W - padX}
            y={H - 6}
            textAnchor="end"
            fontFamily="JetBrains Mono"
            fontSize="10"
            fill="rgba(255,255,255,0.32)"
          >
            n → dense
          </text>
          <text
            x={padX - 8}
            y={padY + 6}
            fontFamily="JetBrains Mono"
            fontSize="10"
            fill="rgba(255,255,255,0.32)"
          >
            t
          </text>
        </svg>
      </div>
    </motion.div>
  )
}
