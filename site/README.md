# reachq product page

The marketing site for **reachq** — a Python library for parallel shortcut
sets and hopsets on dense digraphs.

This folder is the source of the public product page published at
https://sachncs.github.io/reachq.

The source-of-truth documentation for the library itself still lives in
[`../docs`](../docs) and the project README in [`../README.md`](../README.md);
this page does **not** render markdown or docs — it is a hand-crafted product
landing page.

## Stack

- [Vite](https://vitejs.dev) + [React](https://react.dev) + TypeScript
- [Tailwind CSS](https://tailwindcss.com)
- [Framer Motion](https://www.framer.com/motion/) for refined motion
- [Lucide](https://lucide.dev) icons
- No content is rendered from `.md` / `.mdx` files — everything is JSX.

## Develop

```bash
cd site
npm install
npm run dev        # http://127.0.0.1:5173
npm run build      # produces ./dist
npm run preview    # serve the production build locally
```

## Structure

```
site/
├── index.html                 # entry HTML + SEO + OG meta
├── public/
│   ├── favicon.svg
│   ├── logo.svg
│   └── robots.txt
├── src/
│   ├── main.tsx               # React root
│   ├── App.tsx                # composes the sections
│   ├── index.css              # Tailwind base + design tokens + components
│   ├── components/            # reusable UI (LogoMark, NavBar, GraphCanvas)
│   ├── sections/              # one file per page section
│   └── lib/cn.ts              # clsx + tailwind-merge helper
├── tailwind.config.js
├── postcss.config.js
├── tsconfig*.json
├── vite.config.ts
└── package.json
```

## Deployment

`.github/workflows/pages.yml` builds and publishes `site/dist` to GitHub
Pages on every push to `master` / `main`.

The site uses `base: './'` in `vite.config.ts` so it works whether deployed
at `https://sachncs.github.io/reachq/` or a custom domain in the future.

## Design notes

- Apple-like restraint, generous spacing, strong typography.
- Cinematic dark background with a single indigo → teal accent gradient.
- Subtle radial light, low-opacity noise, and an animated layered-DAG SVG as
  the hero visual signal (shortcut edges drawn as dashed animated strokes).
- No emoji, no flashy marketing visuals — refined, premium, production-shaped.
