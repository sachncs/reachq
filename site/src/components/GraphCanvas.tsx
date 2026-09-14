import { useEffect, useMemo, useRef } from 'react'

type Node = { id: number; x: number; y: number; layer: number }
type Edge = { from: number; to: number; shortcut?: boolean; highlight?: boolean }

type Props = {
  className?: string
  /** side length in px for the SVG viewBox; rendered fluid via width:100% */
  size?: number
  /** number of nodes to render */
  n?: number
  /** animate the reachability pulse */
  pulse?: boolean
  /** play subtle shortcut-edge highlight */
  shortcuts?: boolean
}

/**
 * A procedurally-laid-out layered DAG with ~N nodes, ~3 layers deep.
 * Visualises dense digraphs: a base set of edges plus injected "shortcut"
 * arcs that bypass intermediate nodes (Theorem 2 of the paper).
 *
 * Renders with SVG + CSS animations; no canvas dependency.
 */
export function GraphCanvas({
  className,
  size = 800,
  n = 42,
  pulse = true,
  shortcuts = true,
}: Props) {
  const { nodes, edges, shortcuts: shortcuts_ } = useMemo(
    () => buildLayout(n, size),
    [n, size],
  )

  const svgRef = useRef<SVGSVGElement | null>(null)

  useEffect(() => {
    if (!pulse) return
    const root = svgRef.current
    if (!root) return
    const circles = root.querySelectorAll<SVGCircleElement>('[data-pulse-target]')
    const handles: number[] = []
    circles.forEach((c, i) => {
      const delay = (i * 137) % 4000
      const start = performance.now() + delay
      const tick = (now: number) => {
        const t = ((now - start) % 4000) / 4000
        const v = t < 0.5 ? t * 2 : (1 - t) * 2
        c.setAttribute('r', String(2.2 + v * 1.6))
        c.setAttribute('opacity', String(0.6 + v * 0.4))
        handles.push(requestAnimationFrame(tick))
      }
      handles.push(requestAnimationFrame(tick))
    })
    return () => {
      handles.forEach((h) => cancelAnimationFrame(h))
    }
  }, [pulse])

  return (
    <svg
      ref={svgRef}
      viewBox={`0 0 ${size} ${size}`}
      className={className}
      role="img"
      aria-label="Animated reachability graph visualisation"
    >
      <defs>
        <linearGradient id="gc-edge" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0%" stopColor="rgba(165,180,252,0.55)" />
          <stop offset="100%" stopColor="rgba(20,184,166,0.55)" />
        </linearGradient>
        <linearGradient id="gc-shortcut" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0%" stopColor="#a5b4fc" />
          <stop offset="100%" stopColor="#2dd4bf" />
        </linearGradient>
        <radialGradient id="gc-node" cx="0.5" cy="0.5" r="0.5">
          <stop offset="0%" stopColor="#ffffff" stopOpacity="1" />
          <stop offset="60%" stopColor="#a5b4fc" stopOpacity="0.85" />
          <stop offset="100%" stopColor="#4f46e5" stopOpacity="0" />
        </radialGradient>
        <radialGradient id="gc-source" cx="0.5" cy="0.5" r="0.5">
          <stop offset="0%" stopColor="#ffffff" stopOpacity="1" />
          <stop offset="60%" stopColor="#2dd4bf" stopOpacity="0.9" />
          <stop offset="100%" stopColor="#0d9488" stopOpacity="0" />
        </radialGradient>
        <filter id="gc-glow" x="-50%" y="-50%" width="200%" height="200%">
          <feGaussianBlur stdDeviation="2" />
        </filter>
      </defs>

      {/* base edges */}
      <g stroke="rgba(255,255,255,0.07)" strokeWidth={1}>
        {edges.map((e, i) => {
          const a = nodes[e.from]
          const b = nodes[e.to]
          if (!a || !b) return null
          return (
            <line
              key={`e-${i}`}
              x1={a.x}
              y1={a.y}
              x2={b.x}
              y2={b.y}
            />
          )
        })}
      </g>

      {/* shortcut edges */}
      {shortcuts && (
        <g stroke="url(#gc-shortcut)" strokeWidth={1.4}>
          {shortcuts_.map((e, i) => {
            const a = nodes[e.from]
            const b = nodes[e.to]
            if (!a || !b) return null
            return (
              <line
                key={`s-${i}`}
                x1={a.x}
                y1={a.y}
                x2={b.x}
                y2={b.y}
                strokeDasharray="4 4"
                opacity={0.85}
              >
                <animate
                  attributeName="stroke-dashoffset"
                  from="0"
                  to="32"
                  dur="3s"
                  repeatCount="indefinite"
                />
              </line>
            )
          })}
        </g>
      )}

      {/* ghost glow for nodes */}
      <g filter="url(#gc-glow)" opacity={0.55}>
        {nodes.map((n) => (
          <circle
            key={`glow-${n.id}`}
            cx={n.x}
            cy={n.y}
            r={6}
            fill={n.id === 0 ? 'url(#gc-source)' : 'url(#gc-node)'}
          />
        ))}
      </g>

      {/* nodes */}
      <g>
        {nodes.map((n) => (
          <circle
            key={`n-${n.id}`}
            data-pulse-target
            cx={n.x}
            cy={n.y}
            r={2.4}
            fill={n.id === 0 ? '#2dd4bf' : '#ffffff'}
          />
        ))}
      </g>
    </svg>
  )
}

/* ---------- deterministic layout: layered DAG ---------- */

function buildLayout(n: number, size: number) {
  const layers = 4
  const pad = size * 0.08
  const usable = size - pad * 2
  const perLayer = Math.max(2, Math.floor(n / layers))
  const nodes: Node[] = []
  const edges: Edge[] = []
  const shortcuts: Edge[] = []
  const count = perLayer * layers
  const rng = mulberry32(0xc0ffee)
  for (let layer = 0; layer < layers; layer++) {
    for (let i = 0; i < perLayer; i++) {
      nodes.push({
        id: nodes.length,
        x: pad + (i + 0.5) * (usable / perLayer) + (rng() - 0.5) * 8,
        y: pad + layer * (usable / (layers - 1)) + (rng() - 0.5) * 8,
        layer,
      })
    }
  }

  for (let i = 0; i < count; i++) {
    const a = nodes[i]
    if (!a) continue
    for (let j = 0; j < count; j++) {
      const b = nodes[j]
      if (!b) continue
      if (b.layer <= a.layer) continue
      const distance = b.layer - a.layer
      const baseP = 0.55 / distance
      if (rng() < baseP) edges.push({ from: a.id, to: b.id })
    }
  }

  for (let i = 0; i < 6; i++) {
    const a = nodes[Math.floor(rng() * count)]
    const b = nodes[Math.floor(rng() * count)]
    if (!a || !b) continue
    if (b.layer <= a.layer) continue
    if (!edges.some((e) => e.from === a.id && e.to === b.id)) {
      shortcuts.push({ from: a.id, to: b.id })
    }
  }

  return { nodes, edges, shortcuts }
}

function mulberry32(a: number) {
  return function () {
    a |= 0
    a = (a + 0x6d2b79f5) | 0
    let t = a
    t = Math.imul(t ^ (t >>> 15), t | 1)
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61)
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296
  }
}
