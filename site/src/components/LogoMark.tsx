import { cn } from '@/lib/cn'

type LogoMarkProps = {
  size?: number
  className?: string
  withWordmark?: boolean
}

export function LogoMark({ size = 32, className, withWordmark = false }: LogoMarkProps) {
  return (
    <span className={cn('inline-flex items-center gap-2.5', className)}>
      <svg
        viewBox="0 0 64 64"
        width={size}
        height={size}
        aria-hidden="true"
        className="shrink-0"
      >
        <defs>
          <linearGradient id="lm-g" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stopColor="#818CF8" />
            <stop offset="55%" stopColor="#6366F1" />
            <stop offset="100%" stopColor="#14B8A6" />
          </linearGradient>
          <radialGradient id="lm-hl" cx="0.3" cy="0.25" r="0.7">
            <stop offset="0%" stopColor="#ffffff" stopOpacity="0.4" />
            <stop offset="60%" stopColor="#ffffff" stopOpacity="0" />
          </radialGradient>
        </defs>
        <rect width="64" height="64" rx="14" fill="url(#lm-g)" />
        <rect width="64" height="64" rx="14" fill="url(#lm-hl)" />
        <g stroke="#ffffff" strokeOpacity="0.32" strokeWidth="1.2" fill="none">
          <line x1="11" y1="14" x2="27" y2="14" />
          <line x1="27" y1="14" x2="49" y2="24" />
          <line x1="11" y1="14" x2="32" y2="37" />
          <line x1="49" y1="24" x2="32" y2="37" />
          <line x1="32" y1="37" x2="52" y2="50" />
          <line x1="11" y1="14" x2="52" y2="50" />
        </g>
        <g fill="#ffffff">
          <circle cx="11" cy="14" r="1.6" />
          <circle cx="49" cy="24" r="1.6" />
          <circle cx="32" cy="37" r="1.6" />
          <circle cx="52" cy="50" r="1.6" />
        </g>
        <g fill="none" stroke="#ffffff" strokeWidth="3.6" strokeLinecap="round">
          <circle cx="35" cy="32" r="13" />
          <line x1="44" y1="41" x2="50" y2="47" />
        </g>
        <circle cx="35" cy="32" r="2.4" fill="#ffffff" />
      </svg>
      {withWordmark && (
        <span className="display text-[17px] font-semibold tracking-tightest text-ink">
          reachq
        </span>
      )}
    </span>
  )
}
