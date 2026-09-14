/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        sans: [
          'Inter',
          'ui-sans-serif',
          'system-ui',
          '-apple-system',
          'BlinkMacSystemFont',
          'Segoe UI',
          'Roboto',
          'Helvetica Neue',
          'Arial',
          'sans-serif',
        ],
        display: [
          '"Inter Display"',
          'Inter',
          'ui-sans-serif',
          'system-ui',
          '-apple-system',
          'sans-serif',
        ],
        mono: [
          '"JetBrains Mono"',
          'ui-monospace',
          'SFMono-Regular',
          'Menlo',
          'Monaco',
          'Consolas',
          'monospace',
        ],
      },
      colors: {
        bg: {
          DEFAULT: '#07070B',
          soft: '#0A0A12',
          card: '#0E0E18',
          inset: '#08080E',
        },
        line: {
          DEFAULT: 'rgba(255,255,255,0.08)',
          soft: 'rgba(255,255,255,0.05)',
          strong: 'rgba(255,255,255,0.14)',
        },
        ink: {
          DEFAULT: '#F4F4F7',
          soft: 'rgba(244,244,247,0.72)',
          muted: 'rgba(244,244,247,0.52)',
          faint: 'rgba(244,244,247,0.32)',
        },
        brand: {
          50: '#EEF2FF',
          100: '#E0E7FF',
          200: '#C7D2FE',
          300: '#A5B4FC',
          400: '#818CF8',
          500: '#6366F1',
          600: '#4F46E5',
          700: '#4338CA',
          800: '#3730A3',
          900: '#312E81',
        },
        accent: {
          DEFAULT: '#14B8A6',
          400: '#2DD4BF',
          500: '#14B8A6',
          600: '#0D9488',
        },
      },
      letterSpacing: {
        tightest: '-0.04em',
        tighter: '-0.025em',
      },
      backgroundImage: {
        'grid-fade':
          'radial-gradient(ellipse at top, rgba(99,102,241,0.18), transparent 55%)',
        'mesh-1':
          'radial-gradient(at 20% 20%, rgba(99,102,241,0.35) 0px, transparent 45%), radial-gradient(at 80% 0%, rgba(20,184,166,0.28) 0px, transparent 45%), radial-gradient(at 100% 60%, rgba(139,92,246,0.22) 0px, transparent 50%)',
        'mesh-2':
          'radial-gradient(at 0% 100%, rgba(56,189,248,0.18) 0px, transparent 45%), radial-gradient(at 100% 100%, rgba(99,102,241,0.22) 0px, transparent 50%)',
        'noise':
          "url(\"data:image/svg+xml;utf8,<svg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0.04 0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>\")",
      },
      boxShadow: {
        glow: '0 0 80px -20px rgba(99,102,241,0.45)',
        'glow-soft': '0 0 60px -25px rgba(99,102,241,0.35)',
        card: '0 1px 0 0 rgba(255,255,255,0.04) inset, 0 0 0 1px rgba(255,255,255,0.04)',
      },
      keyframes: {
        'fade-up': {
          '0%': { opacity: '0', transform: 'translateY(12px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        shimmer: {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
        pulseGlow: {
          '0%, 100%': { opacity: '0.5' },
          '50%': { opacity: '1' },
        },
        floaty: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-6px)' },
        },
      },
      animation: {
        'fade-up': 'fade-up 0.7s cubic-bezier(0.16, 1, 0.3, 1) both',
        shimmer: 'shimmer 6s linear infinite',
        pulseGlow: 'pulseGlow 3s ease-in-out infinite',
        floaty: 'floaty 6s ease-in-out infinite',
      },
    },
  },
  plugins: [],
}
