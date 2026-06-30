# Rabbit & Elephant — Bedtime Stories

A children's bedtime story site built as static HTML, deployed on GitHub Pages.

**Live site:** _add your URL here_

## Stories

| # | Title | Status |
|---|-------|--------|
| 01 | The Hungry Friends | ✅ Live |
| 02 | Ouch! The Big Thorn | ✅ Live |

## Deploy

1. Push to GitHub
2. Go to **Settings → Pages → Source: main branch, folder / (root)**
3. Done — the site is live at `https://<your-username>.github.io/<repo-name>/`

## Adding a new story

1. Create `stories/NN-story-slug/index.html` — copy the structure from an existing story
2. Add an entry to `assets/data/stories-data.js`
3. That's it — the home page picks it up automatically

## Adding a new character

1. Add an entry to `assets/data/characters-data.js`
2. Add a matching SVG portrait inside the `portraits` object in `characters.html`

## Tech

Plain HTML, CSS, and vanilla JS. No build step, no dependencies.
