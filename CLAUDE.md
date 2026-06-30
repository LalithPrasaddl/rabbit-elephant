# Rabbit & Elephant — Bedtime Stories Site

A children's bedtime story site, built as static HTML for GitHub Pages.

## Project goals
- Funny, silly, and educational tone
- Dual audience: pictures for 2–3 year olds, text for 6–10 year olds
- Mobile-first (swipe to turn pages), desktop-friendly (arrow keys + buttons)
- Expandable over time: easy to add new stories and characters

## File structure

```
rabbit-elephant/
├── .nojekyll                        ← Required for GitHub Pages (no Jekyll processing)
├── index.html                       ← Bookshelf home page
├── characters.html                  ← Character profiles page
├── assets/
│   ├── css/
│   │   ├── main.css                 ← Shared: nav, fonts, colors, CSS variables
│   │   ├── book.css                 ← Bookshelf cards + page-flip reader styles
│   │   └── characters.css          ← Character card styles
│   ├── js/
│   │   ├── book.js                  ← Page flip engine (swipe, keyboard, buttons)
│   │   └── nav.js                  ← Active nav link highlighting
│   └── data/
│       ├── stories-data.js          ← Story manifest (loaded as global STORIES array)
│       └── characters-data.js      ← Character definitions (global CHARACTERS array)
└── stories/
    └── 01-the-hungry-friends/
        └── index.html              ← Self-contained story with inline SVG illustrations
```

## Design decisions

**Fonts:** Google Fonts — `Fredoka One` for headings/display, `Nunito` for body and story text.

**Color palette (CSS variables in main.css):**
- `--color-primary: #FF6B6B` (coral red)
- `--color-secondary: #FFD166` (sunny yellow)
- `--color-accent: #06C98A` (mint green)
- `--color-bg: #FFF9F0` (warm cream)

**Illustrations:** Inline SVG art per page, `viewBox="0 0 500 360"`. Characters use consistent color palette:
- Rabbit: body `#F0E8DC`, ear interior `#FFB3C6`, nose `#FF9BAE`
- Elephant: body `#A8C0CC`, ears `#C5D8E0`

**Page flip:** CSS animation (`pageEnterNext` / `pageEnterPrev`) triggered by JS adding/removing `.active` and `.dir-prev` classes. All pages are `display:none` except the active one.

**Mobile layout:** At ≤720px, `.page-spread` switches to `flex-direction: column` — illustration on top (max-height 300px), text below. Touch swipe threshold is 48px horizontal delta.

## Adding a new story

1. Create `stories/NN-story-slug/index.html` — copy the structure from `01-the-hungry-friends/index.html`.
2. Asset paths from inside a story file use `../../assets/`.
3. Add an entry to `assets/data/stories-data.js`:
   ```js
   {
     id: 'NN-story-slug',
     title: 'Story Title',
     subtitle: 'A short tagline',
     emoji: '🌟',
     description: 'One sentence description for the bookshelf card.',
     tags: ['Tag1', 'Tag2'],
     characters: ['Rabbit', 'Elephant'],
     readTime: '5 min read',
     path: 'stories/NN-story-slug/',
     cardColor: '#FFD166',   // hex used for card gradient
     comingSoon: false
   }
   ```
4. The home page (`index.html`) renders cards automatically from this array — no other changes needed.

## Adding a new character

1. Add an entry to `assets/data/characters-data.js`.
2. Add a matching SVG portrait in the `portraits` object inside `characters.html` (keyed by `id`). Use `viewBox="0 0 220 280"` for portrait orientation to match existing cards.

## Story page structure

Each story HTML has:
- `.page.page-cover` — full-width cover (index 0)
- `.page.page-spread` × N — story pages, each with `.page-illustration` (SVG) + `.page-text` (story prose)
- `#progress-fill` — thin bar at top that fills as pages advance
- `#btn-prev`, `#btn-next`, `#page-counter` — nav controls wired to `book.js`

## Deploying to GitHub Pages

```bash
git remote add origin <your-github-repo-url>
git push -u origin main
```

In GitHub repo → Settings → Pages → Source: `main` branch, folder `/` (root). The `.nojekyll` file ensures `assets/` is served correctly.

## Current stories

| # | Title | Status |
|---|-------|--------|
| 01 | The Hungry Friends | ✅ Live |

## Current characters

| Character | Favourite food | First appears in |
|-----------|---------------|-----------------|
| Rabbit | Carrot Halwa | The Hungry Friends |
| Elephant | Fruit Salad | The Hungry Friends |
