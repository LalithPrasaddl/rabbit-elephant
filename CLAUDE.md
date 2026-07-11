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

**Illustrations:** Inline SVG art per page, `viewBox="0 0 500 360"` (cover uses `0 0 500 240`). Characters use consistent color palette:
- Rabbit: body `#F0E8DC`, ear interior `#FFB3C6`, nose `#FF9BAE`
- Elephant: body `#A8C0CC`, ears `#C5D8E0`

**Background template (standard for every page, every story):** Never fill a page background with a single flat `<rect>`. Every illustration should feel like the same warm, sunny meadow, using this layered recipe:
1. **Sky** — a `<linearGradient>` (unique `id` per `<svg>`, e.g. `sky-p3`) from a soft saturated color at the top to a pale near-white at the bottom. Pick the top color by mood, not randomly: cheerful/morning scenes ≈ `#BEE7FB`→`#EAF9FF`; warm/golden-hour or happy-ending scenes ≈ `#FFE8B0`→`#FFF5D8`; quieter emotional beats (confusion, mild frustration, a small mishap) ≈ a soft warm peach `#FFE3D6`→`#FFF6EE` — still warm and safe-feeling, never dark or dull, since the audience is 2–4 year olds.
2. **Sun** — 2 concentric circles (outer saturated, inner pale) somewhere in the sky; add short radiating `<line>` rays for the "cover"-style hero shots.
3. **Clouds** — 2–3 soft white overlapping ellipses (`opacity 0.7–0.9`), placed asymmetrically so the sky never looks empty.
4. **Ground** — a `<path>` with a gentle wavy top edge (quadratic `Q...T...` curve, not a hard rectangle line) filled with a green `<linearGradient>` (lighter top, darker bottom), plus a second, more-transparent wavy band beneath it for depth, plus a few grass-tuft strokes and flower dots (small circle-in-circle using the existing accent palette: `#FF6B6B`, `#FFD166`, `#C77DFF`, `#74C8E4`, `#FF9BAE`).
5. Keep the ground's top y-coordinate matched to where characters' feet/legs already sit in that page — the wavy curve should vary only ±15px around that line so characters don't appear to float or sink.

**Speech/thought bubble rule:** Always set `text-anchor="middle"` and position the `<text>` x at the bubble's `cx`. Size the bubble generously: budget roughly 8–9px of width per character at font-size 14–15 (bold), plus ~25–30px of padding on each side, and split long lines into two `<text>` elements rather than letting one line run long. Never eyeball a narrow bubble against left-aligned text — that's how text overflows the bubble edge.

**Pose clarity:** When a character is described performing a specific physical action (reaching into a bowl, swapping an item, gesturing while explaining), make sure the relevant limb/trunk path actually terminates at or overlaps the object involved, rather than stopping short in empty space nearby.

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
| 02 | Ouch! The Big Thorn | ✅ Live |
| 03 | Snow Much Help! | ✅ Live |
| 04 | Watch Your Step! | ✅ Live |
| 05 | Splash! The Pool Party | ✅ Live |

## Current characters

| Character | Favourite food | First appears in |
|-----------|---------------|-----------------|
| Rabbit | Carrot Halwa | The Hungry Friends |
| Elephant | Fruit Salad | The Hungry Friends |
| Dr. Squirrel | Acorn Pudding | Ouch! The Big Thorn |
| Dr. Sheep | Clover Tea | Snow Much Help! |
| Nurse Giraffe | Acacia Leaf Salad | Snow Much Help! |
