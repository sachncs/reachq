import { AnimatePresence, motion } from 'framer-motion'
import { useState } from 'react'
import { Check, Copy } from 'lucide-react'

type Tab = {
  id: string
  label: string
  badge?: string
  filename: string
  code: string
  caption: string
  highlights: string[]
}

const TABS: Tab[] = [
  {
    id: 'reachability',
    label: 'Parallel reachability',
    badge: 'Theorem 2',
    filename: 'reachq_reach.py',
    caption:
      'Build a shortcut set for a digraph, prove reachability is preserved, then query in parallel.',
    highlights: [
      'Deterministic seeds',
      'Invariant assertion included',
      'Query speedup on dense graphs',
    ],
    code: `from reachq import Digraph, RefinementConfig
from reachq.generators import random_dag
from reachq.shortcut import build_shortcut_set_for_reachability
from reachq.reachability import bfs_reachability, parallel_bfs
from reachq.invariants import assert_reachability_preserved

# A 1k-vertex random DAG.
g = random_dag(n=1000, edge_probability=0.10, random_seed=42)

# Build a JLS shortcut set with TC-pruning on.
shortcuts, beta, bound = build_shortcut_set_for_reachability(
    g,
    omega=3.0,
    random_seed=42,
    refinement=RefinementConfig(enable_tc_pruning=True, tight_tc_trigger=True),
)

# Invariant: reachability is preserved for every source.
assert_reachability_preserved(g, shortcuts)

# Now queries are fast — and provably equivalent to BFS.
sources = (g.vertices()[0], g.vertices()[len(g.vertices()) // 2])
for src in sources:
    assert parallel_bfs(g, src, shortcuts) == bfs_reachability(g, src)
`,
  },
  {
    id: 'hopset',
    label: 'Hopsets (1+ε)',
    badge: 'Theorem 4',
    filename: 'reachq_hopset.py',
    caption:
      'Construct a CFR hopset, then run hop-bounded SSSP with configurable approximation.',
    highlights: [
      '(1 + ε) approximation',
      'TruncSSSP pruning',
      'Hop-bounded queries',
    ],
    code: `from reachq import WeightedDigraph
from reachq.hopset import build_hopset_for_sssp
from reachq.shortest_paths import (
    dijkstra,
    shortest_path_hopbound,
)

g = WeightedDigraph()
for u, v, w in [
    (0, 1, 1), (1, 2, 2), (0, 2, 10),
    (2, 3, 1), (3, 4, 5), (1, 4, 6),
]:
    g.add_edge(u, v, w)

hopset, beta = build_hopset_for_sssp(g, epsilon=0.10, random_seed=42)

exact = dijkstra(g, 0)
approx = shortest_path_hopbound(g, hopset, 0, max_hops=100)

for v, d in exact.items():
    assert approx[v] <= (1 + 0.10) * d + 1e-9
`,
  },
  {
    id: 'refinement',
    label: 'Refinement tuning',
    badge: '9 toggles',
    filename: 'reachq_refine.py',
    caption:
      'A frozen dataclass of toggles. Mix and match the algorithmic refinements from the paper.',
    highlights: [
      'Adaptive sampling',
      'TC-pruning trigger',
      'Process-pool dispatch',
    ],
    code: `from reachq import RefinementConfig, Digraph
from reachq.shortcut import build_shortcut_set_for_reachability
from reachq.generators import random_dag

g = random_dag(n=2000, edge_probability=0.05, random_seed=42)

cfg = RefinementConfig(
    adaptive_sampling=True,        # adapt per-level p by observed part size
    label_compress=True,           # frozenset[int] instead of set[str]
    skip_condense=False,           # SCC condensation on
    hop_bounded_bfs=True,
    degree_ordered_pivots=True,
    tight_tc_trigger=True,
    skip_trivial_part=True,
    enable_tc_pruning=True,
    parallel=True,                 # dispatch per-pivot BFS via processes
)

shortcuts, beta, bound = build_shortcut_set_for_reachability(
    g, omega=3.0, random_seed=42, refinement=cfg,
)
`,
  },
  {
    id: 'persist',
    label: 'Save & load',
    badge: 'IO',
    filename: 'reachq_io.py',
    caption:
      'Stable on-disk serialisation. Reproducible, portable, framework-friendly.',
    highlights: ['JSON', 'Arrow IPC', 'NetworkX adapter'],
    code: `from reachq.generators import random_dag
from reachq.io import dump, load
from reachq.io_networkx import to_networkx, from_networkx

g = random_dag(n=500, edge_probability=0.1, random_seed=7)

# Round-trip via JSON.
text = dump(g)
h = load(text)
assert h.num_vertices() == g.num_vertices()

# Plug into the broader Python graph ecosystem.
nx_g = to_networkx(g)
g_back = from_networkx(nx_g)
assert g_back.num_vertices() == g.num_vertices()
`,
  },
]

export function CodeShowcase() {
  const [active, setActive] = useState<string>(TABS[0]!.id)
  const [copied, setCopied] = useState(false)
  const tab = TABS.find((t) => t.id === active) ?? TABS[0]!

  const copy = async () => {
    try {
      await navigator.clipboard.writeText(tab.code)
      setCopied(true)
      window.setTimeout(() => setCopied(false), 1500)
    } catch {
      /* no-op */
    }
  }

  return (
    <section id="code" className="relative py-24 sm:py-32">
      <div className="container-page">
        <div className="mx-auto max-w-2xl text-center">
          <p className="eyebrow mb-4">A library, not a black box</p>
          <h2 className="display text-balance text-3xl font-semibold tracking-tightest sm:text-4xl">
            Reads like Python.{' '}
            <span className="gradient-brand">Thinks like the paper.</span>
          </h2>
          <p className="mt-4 text-pretty text-base text-ink-soft">
            Every entry point is typed, documented, and shipped with a doctest
            you can run in five seconds.
          </p>
        </div>

        <div className="mt-14 grid gap-6 lg:grid-cols-[1.05fr_0.95fr] lg:items-stretch">
          <div className="flex flex-col">
            <div className="surface relative rounded-2xl p-2">
              <div
                role="tablist"
                className="flex flex-wrap gap-1 rounded-xl bg-white/[0.02] p-1.5"
              >
                {TABS.map((t) => {
                  const isActive = t.id === active
                  return (
                    <button
                      key={t.id}
                      role="tab"
                      aria-selected={isActive}
                      onClick={() => setActive(t.id)}
                      className={
                        'group inline-flex flex-1 items-center justify-center gap-2 rounded-lg px-3.5 py-2 text-[13px] font-medium transition-all ' +
                        (isActive
                          ? 'bg-white/[0.06] text-ink shadow-[inset_0_1px_0_rgba(255,255,255,0.06)]'
                          : 'text-ink-muted hover:bg-white/[0.04] hover:text-ink-soft')
                      }
                    >
                      <span className="truncate">{t.label}</span>
                      {t.badge && (
                        <span
                          className={
                            'hidden rounded-full border px-1.5 py-0.5 text-[9px] uppercase tracking-wider sm:inline ' +
                            (isActive
                              ? 'border-brand-400/30 bg-brand-500/10 text-brand-200'
                              : 'border-line text-ink-faint')
                          }
                        >
                          {t.badge}
                        </span>
                      )}
                    </button>
                  )
                })}
              </div>
            </div>

            <div className="surface-strong relative mt-4 flex flex-1 flex-col overflow-hidden rounded-2xl">
              <div className="flex items-center justify-between border-b border-line-soft px-4 py-3">
                <div className="flex items-center gap-2">
                  <span className="h-2.5 w-2.5 rounded-full bg-[#FF5F57]/70" />
                  <span className="h-2.5 w-2.5 rounded-full bg-[#FEBC2E]/70" />
                  <span className="h-2.5 w-2.5 rounded-full bg-[#28C840]/70" />
                </div>
                <span className="font-mono text-[12px] text-ink-faint">
                  {tab.filename}
                </span>
                <button
                  onClick={copy}
                  className="inline-flex items-center gap-1.5 rounded-md border border-line bg-white/[0.04] px-2.5 py-1 text-[11px] text-ink-soft transition-colors hover:bg-white/[0.08]"
                  aria-label="Copy code"
                >
                  {copied ? (
                    <>
                      <Check size={11} /> Copied
                    </>
                  ) : (
                    <>
                      <Copy size={11} /> Copy
                    </>
                  )}
                </button>
              </div>

              <div className="relative flex-1 overflow-hidden">
                <AnimatePresence mode="wait" initial={false}>
                  <motion.pre
                    key={tab.id}
                    initial={{ opacity: 0, y: 6 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -6 }}
                    transition={{ duration: 0.18, ease: [0.16, 1, 0.3, 1] }}
                    className="m-0 flex-1 overflow-x-auto p-5 font-mono text-[12.5px] leading-[1.65] text-ink-soft"
                  >
                    <code
                      className="block min-h-[420px] whitespace-pre"
                      dangerouslySetInnerHTML={{ __html: highlight(tab.code) }}
                    />
                  </motion.pre>
                </AnimatePresence>
              </div>
            </div>
          </div>

          <div className="flex flex-col">
            <div className="surface relative flex flex-1 flex-col rounded-2xl p-7">
              <p className="eyebrow">{tab.label}</p>
              <h3 className="mt-3 text-[22px] font-semibold tracking-tight">
                {tab.caption}
              </h3>
              <ul className="mt-7 space-y-3">
                {tab.highlights.map((h) => (
                  <li
                    key={h}
                    className="flex items-start gap-3 text-[14px] text-ink-soft"
                  >
                    <span className="mt-1.5 inline-block h-1.5 w-1.5 shrink-0 rounded-full bg-accent-400" />
                    <span>{h}</span>
                  </li>
                ))}
              </ul>

              <div className="mt-auto pt-10">
                <a
                  href="https://github.com/sachncs/reachq/blob/master/docs/reference.md"
                  target="_blank"
                  rel="noreferrer"
                  className="inline-flex items-center gap-1.5 text-[13px] text-brand-200 hover:text-brand-100"
                >
                  Full API reference →
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}

/* ---------- minimal Python highlighter ---------- */

function escape(s: string) {
  return s
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
}

function highlight(code: string) {
  const keywords = new Set([
    'from', 'import', 'def', 'return', 'for', 'in', 'if', 'else', 'elif',
    'assert', 'True', 'False', 'None', 'as', 'and', 'or', 'not', 'with',
    'try', 'except', 'class', 'lambda', 'pass', 'break', 'continue',
    'is', 'raise', 'yield', 'global', 'nonlocal',
  ])
  const builtins = new Set([
    'int', 'float', 'str', 'bool', 'list', 'tuple', 'set', 'dict',
    'len', 'range', 'print', 'open', 'isinstance', 'enumerate',
  ])

  const lines = escape(code).split('\n')
  return lines
    .map((line) => {
      const tokens = line.split(/(\s+|[(){}\[\],.:])/g)
      const out = tokens
        .map((t) => {
          if (/^\s+$/.test(t)) return t
          if (!t) return ''
          if (keywords.has(t)) {
            return `<span style="color:#a5b4fc">${t}</span>`
          }
          if (builtins.has(t)) {
            return `<span style="color:#c4b5fd">${t}</span>`
          }
          if (/^['"]/.test(t) && /['"]$/.test(t)) {
            return `<span style="color:#86efac">${t}</span>`
          }
          if (/^(0x[0-9a-fA-F]+|\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)$/.test(t)) {
            return `<span style="color:#fbbf24">${t}</span>`
          }
          if (/^[A-Za-z_][A-Za-z0-9_]*$/.test(t) && /[A-Z]/.test(t[0]!)) {
            return `<span style="color:#7dd3fc">${t}</span>`
          }
          if (/^[A-Za-z_][A-Za-z0-9_]*$/.test(t)) {
            return `<span style="color:#e4e4e7">${t}</span>`
          }
          if (t === '#') {
            return `<span style="color:#71717a">#`
          }
          return `<span style="color:#a1a1aa">${t}</span>`
        })
        .join('')
      // style trailing comments
      return out.replace(/(<span style="color:#71717a">#.*)$/, '$1</span>')
    })
    .join('\n')
}
