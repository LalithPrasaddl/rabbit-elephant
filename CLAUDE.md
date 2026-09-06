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
├── tools/
│   └── portraits/                   ← Generators for the characters.html portraits
│       ├── build.py                 ← Regenerates all six + injects into characters.html
│       ├── furlib.py                ← Fur / fleece / wrinkle / patch generators
│       ├── common.py                ← Shared eye, filters, mirror wrapper
│       └── <character>.py           ← One per character
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
- Bear: body `#C89A72`, muzzle/ear interior `#EAD1B0`, nose `#5C3A21`

**Three illustration styles currently coexist** (mid-redesign):

- **Generated-texture style** — `characters.html` portraits only. Built by Python generators in `tools/portraits/`, not hand-authored. See "Character portraits" below. **Never hand-edit portrait SVG in `characters.html` — it is generated output and `build.py` will overwrite it.**
- **Premium dimensional style** — the six story covers (`stories/*/index.html`, the `page-cover` illustration only). Hand-authored: no outlines, radial-gradient shading lit from upper-right, rim light + ambient occlusion. Recipe below.
- **Legacy flat style** — flat fills + thin grey stroke outlines, used by every in-story page illustration (everything past the cover, ~50 scenes). Governed by the "Background template" recipe below. Not yet migrated.

**Character portraits (`characters.html`)** are generated. To change one, edit its generator and rebuild:

```bash
python3 tools/portraits/build.py     # regenerates all six, injects them into characters.html
```

`tools/portraits/` holds `furlib.py` (texture generators), `common.py` (shared eye, filters, mirror wrapper) and one script per character. Conventions that the whole set depends on:

1. **Author facing viewer-LEFT with light from upper-LEFT**, then let `common.svg()` wrap everything in the mirror transform — the finished portrait faces right, lit from upper-right, matching the covers.
2. **Heads are FRONT-FACING**, both eyes either side of the muzzle. A profile head with eyes placed symmetrically about the head's 2D centre puts one eye on the nose and the other mid-cheek; it reads as deformed. This was the single worst bug in the first attempt.
3. **Eyes** come from `common.make_eye()` — ellipse geometry, never a hand-rolled bezier (a squashed bezier lid collapses into a slit). Keep the foreshortening `sq` ≥ 0.7 for the far eye; `lid` around 0.09 reads calm, 0 reads startled, 0.2+ reads sad.
4. **Texture is generated, not drawn**: `fur_layers()` for hair along a flow field, `edge_fur()` for hairs sprouting past the silhouette (this is what stops the outline reading as a vector curve), `curls()` for fleece, `rings()` for trunk/limb wrinkles, `speckle()` for hide mottling, `blotches()` for giraffe patches. Strokes of one tone/width/opacity merge into a single `<path>` with many subpaths to keep the file size sane.
5. **Blur filters need a generous region** — `x="-150%" y="-150%" width="400%" height="400%"`. Anything tighter clips the blur into a visible rectangle.
6. **Limbs that emerge from a body** either get drawn *behind* it (sheep, giraffe legs) or masked with a top-fade gradient (elephant legs). A leg drawn on top with a flat top edge reads as a hollow pipe.
7. **Clip every blurred shading shape** to its parent silhouette, or it floats outside as a stray smudge.
8. Warmth is deliberate: blush inside the head clip, big eyes, rounded bodies, upright posture. The naturalistic anatomy carries the realism; these carry the appeal.
9. `viewBox="0 0 320 360"`, feet baseline ≈ y 330. Prefix every gradient/filter/clip `id` with the character's short prefix (`r-`, `e-`, `b-`, `q-`, `s-`, `n-`) — all six live in the same DOM.

Portrait SVG totals ~440 KB raw / ~145 KB gzipped across the six.

**Premium character illustration recipe** (story covers): light source is always upper-right — every `radialGradient` uses `cx="~70%" cy="~25%" r="~90%"`, going from a bright warm highlight through the base tone to a deeper shade at 100%, no stroke outlines anywhere.
1. **Per major shape** (head, body, ears): fill with a dedicated radial gradient (bright→base→deep), then add a blurred dark ambient-occlusion ellipse toward the lower-left where it meets another form, then a blurred warm-white rim-light stroke along the upper-right silhouette edge.
2. **Eyes**: a radial-gradient iris (warm brown, center lighter than edge) rather than a flat dark circle, plus two catchlights (one bright white, one small warm-tinted) and a thin brow stroke above.
3. **Grounding**: one large blurred dark ellipse under the feet as a contact shadow.
4. **Species-specific realism details** (add what's anatomically appropriate, skip what isn't): visible separated legs/feet with toe or hoof marks, a tail, whiskers, ear-vein lines, trunk/neck wrinkles, tusks — small touches that read as "a real creature," not a toy.

**Background template (standard for every page, every story — legacy flat style only):** Never fill a page background with a single flat `<rect>`. Every illustration should feel like the same warm, sunny meadow, using this layered recipe:
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
2. Add a generator at `tools/portraits/<id>.py` (copy the closest existing one — `bear.py` is the simplest quadruped), add its name to `NAMES` in `tools/portraits/build.py`, add an empty `` <id>: `` ` `` `` entry to the `portraits` object in `characters.html`, then run `python3 tools/portraits/build.py`. Follow the conventions under "Character portraits" above.

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
| 06 | Bonk! The Bumpy Ride Home | ✅ Live |

## Current characters

| Character | Favourite food | First appears in |
|-----------|---------------|-----------------|
| Rabbit | Carrot Halwa | The Hungry Friends |
| Elephant | Fruit Salad | The Hungry Friends |
| Dr. Squirrel | Acorn Pudding | Ouch! The Big Thorn |
| Dr. Sheep | Clover Tea | Snow Much Help! |
| Nurse Giraffe | Acacia Leaf Salad | Snow Much Help! |
| Bear | Honey Crumble | Bonk! The Bumpy Ride Home |
