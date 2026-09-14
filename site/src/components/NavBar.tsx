import { useEffect, useState } from 'react'
import { LogoMark } from '../components/LogoMark'
import { cn } from '../lib/cn'
import { Github, Menu, X } from 'lucide-react'

const NAV_LINKS = [
  { label: 'Features', href: '#features' },
  { label: 'API', href: '#code' },
  { label: 'Performance', href: '#performance' },
  { label: 'Research', href: '#research' },
  { label: 'Docs', href: 'https://github.com/sachncs/reachq' },
]

export function NavBar() {
  const [scrolled, setScrolled] = useState(false)
  const [open, setOpen] = useState(false)

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 24)
    onScroll()
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  return (
    <header
      className={cn(
        'fixed inset-x-0 top-0 z-50 transition-all duration-300',
        scrolled
          ? 'border-b border-line-soft bg-bg/70 backdrop-blur-xl'
          : 'bg-transparent',
      )}
    >
      <div className="container-page flex h-16 items-center justify-between">
        <a href="#top" className="flex items-center gap-2.5">
          <LogoMark size={28} withWordmark />
        </a>

        <nav className="hidden items-center gap-1 md:flex">
          {NAV_LINKS.map((l) => (
            <a
              key={l.label}
              href={l.href}
              className="rounded-full px-3.5 py-1.5 text-[13px] text-ink-soft transition-colors hover:bg-white/[0.04] hover:text-ink"
            >
              {l.label}
            </a>
          ))}
        </nav>

        <div className="hidden items-center gap-2 md:flex">
          <a
            href="https://github.com/sachncs/reachq"
            target="_blank"
            rel="noreferrer"
            className="inline-flex h-9 w-9 items-center justify-center rounded-full border border-line text-ink-soft transition-colors hover:bg-white/[0.04] hover:text-ink"
            aria-label="GitHub"
          >
            <Github size={15} strokeWidth={1.6} />
          </a>
          <a
            href="#install"
            className="btn-primary h-9 px-4 text-[13px] !py-0"
          >
            Install
          </a>
        </div>

        <button
          aria-label="Toggle menu"
          className="md:hidden inline-flex h-9 w-9 items-center justify-center rounded-full border border-line text-ink-soft"
          onClick={() => setOpen((v) => !v)}
        >
          {open ? <X size={16} /> : <Menu size={16} />}
        </button>
      </div>

      {open && (
        <div className="md:hidden border-t border-line-soft bg-bg/95 backdrop-blur-xl">
          <div className="container-page flex flex-col gap-1 py-4">
            {NAV_LINKS.map((l) => (
              <a
                key={l.label}
                href={l.href}
                onClick={() => setOpen(false)}
                className="rounded-lg px-3 py-2 text-sm text-ink-soft hover:bg-white/[0.04] hover:text-ink"
              >
                {l.label}
              </a>
            ))}
            <a
              href="#install"
              onClick={() => setOpen(false)}
              className="btn-primary mt-3 w-full"
            >
              Install reachq
            </a>
          </div>
        </div>
      )}
    </header>
  )
}
