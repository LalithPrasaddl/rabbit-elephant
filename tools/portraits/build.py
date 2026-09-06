#!/usr/bin/env python3
"""Regenerate the six character portraits and inject them into characters.html.

    python3 tools/portraits/build.py

Each <name>.py writes out/<name>.svg; this script then replaces the matching
entry in the `portraits` object in characters.html. Edit the generators, not
the SVG in characters.html - that output is generated and will be overwritten.
"""
import os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
PAGE = os.path.join(ROOT, 'characters.html')
NAMES = ['rabbit', 'elephant', 'bear', 'squirrel', 'sheep', 'giraffe']


def main():
    os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
    svgs = {}
    for n in NAMES:
        subprocess.run([sys.executable, os.path.join(HERE, n + '.py')], check=True)
        svg = open(os.path.join(HERE, 'out', n + '.svg')).read().strip()
        if '`' in svg or '${' in svg:
            raise SystemExit(f'{n}: SVG contains a backtick or ${{ - it would break the JS template literal')
        svgs[n] = svg

    page = open(PAGE).read()
    for n, svg in svgs.items():
        # match `<name>: ` ... closing backtick of that entry
        pat = re.compile(r'(\n      ' + n + r': `)(.*?)(`,?\n)', re.S)
        m = pat.search(page)
        if not m:
            raise SystemExit(f'could not find the {n} portrait entry in characters.html')
        page = page[:m.start(2)] + '\n' + svg + '\n      ' + page[m.end(2):]
    open(PAGE, 'w').write(page)
    total = sum(len(v) for v in svgs.values())
    print(f'injected {len(svgs)} portraits into characters.html ({total/1024:.0f} KB of SVG)')


if __name__ == '__main__':
    main()
