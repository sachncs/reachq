import { LogoMark } from '@/components/LogoMark'

const COLUMNS = [
  {
    title: 'Product',
    links: [
      { label: 'Features', href: '#features' },
      { label: 'API', href: '#code' },
      { label: 'Performance', href: '#performance' },
      { label: 'Research', href: '#research' },
    ],
  },
  {
    title: 'Library',
    links: [
      {
        label: 'GitHub',
        href: 'https://github.com/sachncs/reachq',
      },
      {
        label: 'Docs',
        href: 'https://github.com/sachncs/reachq/tree/master/docs',
      },
      { label: 'Reference', href: 'https://github.com/sachncs/reachq/blob/master/docs/reference.md' },
      { label: 'Examples', href: 'https://github.com/sachncs/reachq/blob/master/docs/examples.md' },
    ],
  },
  {
    title: 'Citation',
    links: [
      {
        label: 'Paper (arXiv)',
        href: 'https://arxiv.org/abs/2605.03892',
      },
      { label: 'BibTeX', href: 'https://github.com/sachncs/reachq#citation' },
      { label: 'Changelog', href: 'https://github.com/sachncs/reachq/blob/master/CHANGELOG.md' },
      { label: 'Roadmap', href: 'https://github.com/sachncs/reachq#roadmap' },
    ],
  },
]

export function Footer() {
  return (
    <footer className="relative border-t border-line-soft py-14 sm:py-20">
      <div className="container-page">
        <div className="grid gap-12 lg:grid-cols-[1.2fr_2fr]">
          <div>
            <LogoMark size={28} withWordmark />
            <p className="mt-4 max-w-xs text-pretty text-sm leading-relaxed text-ink-soft">
              Parallel reachability and shortest-path algorithms on dense
              digraphs. Pure Python. MIT. Citation-grade.
            </p>
            <p className="mt-6 font-mono text-[11px] text-ink-faint">
              <span className="rounded-full border border-line bg-white/[0.02] px-2 py-1">
                v0.9.0
              </span>
            </p>
          </div>

          <div className="grid grid-cols-2 gap-8 sm:grid-cols-3">
            {COLUMNS.map((col) => (
              <div key={col.title}>
                <p className="eyebrow">{col.title}</p>
                <ul className="mt-4 space-y-2.5">
                  {col.links.map((l) => (
                    <li key={l.label}>
                      <a
                        href={l.href}
                        className="text-[13.5px] text-ink-soft transition-colors hover:text-ink"
                      >
                        {l.label}
                      </a>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>

        <div className="mt-14 flex flex-col items-start justify-between gap-4 border-t border-line-soft pt-6 text-[12px] text-ink-faint sm:flex-row sm:items-center">
          <p>
            © {new Date().getFullYear()} Sachin. Released under the MIT License.
          </p>
          <p className="font-mono">
            Built with{' '}
            <a
              href="https://vitejs.dev"
              className="text-ink-muted hover:text-ink-soft"
            >
              Vite
            </a>{' '}
            ·{' '}
            <a
              href="https://react.dev"
              className="text-ink-muted hover:text-ink-soft"
            >
              React
            </a>{' '}
            ·{' '}
            <a
              href="https://tailwindcss.com"
              className="text-ink-muted hover:text-ink-soft"
            >
              Tailwind
            </a>
          </p>
        </div>
      </div>
    </footer>
  )
}
