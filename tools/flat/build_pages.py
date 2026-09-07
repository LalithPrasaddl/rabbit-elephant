#!/usr/bin/env python3
"""Regenerate the in-story page illustrations and inject them into the story HTML.

    python3 tools/flat/build_pages.py                  # every story in pages.PAGES
    python3 tools/flat/build_pages.py 06               # just this one

Same contract as tools/scenes/build_covers.py: the generated SVG is written into the
committed HTML, so GitHub Pages still serves plain static files with no build step.
The story file's cover (page 0) is never touched - that belongs to build_covers.py.
Edit tools/flat/pages.py, not the SVG in the story.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
from pages import PAGES

# the illustration of a spread page: <div class="page-illustration"> ... one <svg>
SPREAD = re.compile(
    r'(<div class="page page-spread".*?<div class="page-illustration">\s*)(<svg\b.*?</svg>)',
    re.S)


def build(slug, fns):
    path = os.path.join(ROOT, 'stories', slug, 'index.html')
    html = open(path).read()
    found = list(SPREAD.finditer(html))
    if len(found) != len(fns):
        raise SystemExit(f'{slug}: {len(found)} spread illustrations in the page but '
                         f'{len(fns)} compose functions in pages.py - they must line up')

    out, prev, total = [], 0, 0
    for m, fn in zip(found, fns):
        svg = (f'<svg viewBox="0 0 500 360" xmlns="http://www.w3.org/2000/svg">'
               f'{fn()}</svg>')
        total += len(svg)
        out.append(html[prev:m.start(2)])
        out.append(svg)
        prev = m.end(2)
    out.append(html[prev:])
    open(path, 'w').write("".join(out))
    print(f'{slug}: injected {len(fns)} page illustrations ({total/1024:.1f} KB of SVG)')


def main():
    want = sys.argv[1:]
    todo = {s: f for s, f in PAGES.items() if not want or any(s.startswith(w) for w in want)}
    if not todo:
        raise SystemExit(f'nothing matches {want}; pages.py has {sorted(PAGES)}')
    for slug, fns in todo.items():
        build(slug, fns)


if __name__ == '__main__':
    main()
