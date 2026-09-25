import { promises as fs } from 'node:fs'
import path from 'node:path'

const root = path.resolve('dist')
const htmlFiles = []

async function collect(directory) {
  for (const entry of await fs.readdir(directory, { withFileTypes: true })) {
    const full = path.join(directory, entry.name)
    if (entry.isDirectory()) await collect(full)
    else if (entry.name.endsWith('.html')) htmlFiles.push(full)
  }
}

async function exists(candidate) {
  try {
    await fs.access(candidate)
    return true
  } catch {
    return false
  }
}

await collect(root)
const links = new Set()
const errors = []

for (const file of htmlFiles) {
  const html = await fs.readFile(file, 'utf8')
  if (html.includes('mkdocs') || html.includes('data-md-color-scheme')) {
    errors.push(`${path.relative(root, file)} contains stale MkDocs output`)
  }
  for (const match of html.matchAll(/href="(\/reachq[^"#? ]*)/g)) links.add(match[1])
}

for (const link of links) {
  const relative = link.replace(/^\/reachq\/?/, '')
  const candidates = relative.endsWith('/')
    ? [path.join(root, relative, 'index.html')]
    : [path.join(root, relative), path.join(root, relative, 'index.html')]
  let found = false
  for (const candidate of candidates) {
    if (candidate.startsWith(root) && await exists(candidate)) {
      found = true
      break
    }
  }
  if (!found) errors.push(`broken internal link: ${link}`)
}

if (errors.length) {
  console.error(errors.join('\n'))
  process.exitCode = 1
} else {
  console.log(`checked ${htmlFiles.length} HTML files and ${links.size} internal links`)
}
