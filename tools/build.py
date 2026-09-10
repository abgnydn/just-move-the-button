#!/usr/bin/env python3
"""Build dist/index.html: one self-contained file (CSS inlined, ES modules bundled, images as data URIs).
Usage: python3 tools/build.py            -> dist/index.html
       python3 tools/build.py --maxh 520 -> downscale embedded images to this height (default 640)
"""
import base64, io, re, sys, pathlib
from PIL import Image
ROOT = pathlib.Path(__file__).resolve().parent.parent
maxh = int(sys.argv[sys.argv.index('--maxh')+1]) if '--maxh' in sys.argv else 640

def data_uri(rel):
    im = Image.open(ROOT/rel)
    if im.height > maxh: im = im.resize((int(im.width*maxh/im.height), maxh), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, 'PNG', optimize=True)
    return 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()

# bundle modules: strip import/export, concatenate in dependency order
order = ['heroes.js', 'instruments.js', 'story.js', 'engine.js']
js = []
for f in order:
    src = (ROOT/'src'/f).read_text()
    src = re.sub(r'^import .*?;\s*$', '', src, flags=re.M)
    src = re.sub(r'^export (const|function|let)', r'\1', src, flags=re.M)
    js.append(f'// ---- {f} ----\n' + src)
js = '\n'.join(js)
# inline asset paths
js = re.sub(r"'(assets/[^']+\.png)'", lambda m: "'" + data_uri(m.group(1)) + "'", js)
css = (ROOT/'src/tokens.css').read_text() + '\n' + (ROOT/'src/comic.css').read_text()
html = (ROOT/'index.html').read_text()
html = re.sub(r'<link rel="stylesheet" href="src/tokens.css">\s*<link rel="stylesheet" href="src/comic.css">', f'<style>\n{css}\n</style>', html)
html = html.replace('<script type="module" src="src/engine.js"></script>', f'<script>\n(function(){{\n{js}\n}})();\n</script>')
out = ROOT/'dist/index.html'; out.write_text(html)
print(f'wrote {out} ({out.stat().st_size//1024} KB)')
