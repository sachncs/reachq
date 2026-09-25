# reachq product page

This folder contains the Astro source for the public reachq launch page:

https://sachncs.github.io/reachq/

The launch page explains the product, onboarding path, core constructions,
performance boundaries, limitations, documentation map, and contribution path.
The library documentation itself remains in ../docs.

## Stack

- Astro: https://astro.build/
- Static output for GitHub Pages
- Plain HTML, CSS, SVG, and a small client-side script

## Develop

~~~bash
cd site
npm install
npm run dev
npm run build
npm run preview
~~~

The production output is `site/dist/`.

## Deployment

.github/workflows/pages.yml builds the Astro site with Node 22 and publishes
site/dist through the GitHub Pages Actions deployment. The workflow checks
for the generated HTML and brand assets before uploading the artifact.


## Brand assets

- public/logo.svg — light horizontal lockup for README/docs surfaces
- public/logo-reversed.svg — dark-background lockup for the launch page
- public/favicon.svg — directed-graph app icon
