# Assembles painbet-design-system.html from frames.json (produced by extract.cjs)
# plus index.html's own <style> block. Run `node extract.cjs` first.
import json, re, html as htmlmod, os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
OUT = os.path.join(REPO_ROOT, 'painbet-design-system.html')

frames = json.load(open(os.path.join(HERE, 'frames.json')))
index_html = open(os.path.join(REPO_ROOT, 'index.html')).read()
css = re.search(r'<style>(.*?)</style>', index_html, re.S).group(1)

# ---------- figma-safe renames (order matters: specific tokens before generic ones) ----------
RENAMES = [
    (r'\bmodal-bg\b', 'card-bg'),
    (r'\bsheet-bg\b', 'board-bg'),
    (r'\bgmodal\b', 'gameframe'),
    (r'\bghead\b', 'gameframe-head'),
    (r'\bmhead\b', 'card-head'),
    (r'\bmbody\b', 'card-body'),
    (r'\bmtabs\b', 'tabs'),
    (r'\bmodal\b', 'card'),
    (r'\bsheet\b', 'board'),
]

def rename(text):
    for pattern, repl in RENAMES:
        text = re.sub(pattern, repl, text)
    return text

def strip_event_handlers(text):
    # strip on*="..." attributes (dead in a static export, and keeps the doc free of
    # references to functions that no longer exist here)
    text = re.sub(r'\s+on[a-z]+="[^"]*"', '', text)
    text = re.sub(r"\s+on[a-z]+='[^']*'", '', text)
    return text

def strip_dialog_signals(text):
    text = re.sub(r'\s+role="dialog"', '', text)
    text = re.sub(r"\s+role='dialog'", '', text)
    text = re.sub(r'\s+aria-modal="[^"]*"', '', text)
    return text

def inputs_to_divs(text):
    # native <input> can abort a subtree in some html-to-figma importers; render as a
    # static styled div showing the placeholder/value instead (not interactive anyway)
    def repl(m):
        tag = m.group(0)
        ph = re.search(r'placeholder="([^"]*)"', tag)
        val = re.search(r'value="([^"]*)"', tag)
        typ = re.search(r'type="([^"]*)"', tag)
        cls = re.search(r'class="([^"]*)"', tag)
        text_content = htmlmod.escape(val.group(1) if val else (ph.group(1) if ph else ''))
        is_pw = typ and typ.group(1) == 'password'
        if is_pw and text_content:
            text_content = '•' * min(len(text_content), 10)
        cls_attr = f' class="inp-el {cls.group(1)}"' if cls else ' class="inp-el"'
        muted = ' inp-el-empty' if not (val or (typ and typ.group(1)=='checkbox')) else ''
        return f'<div{cls_attr}{muted}>{text_content}</div>'
    return re.sub(r'<input\b[^>]*/?>', repl, text)

# ---------- per-kind sizing + structural CSS overrides ----------
KIND_WIDTH = {
    'chrome-vertical': 240,
    'chrome-horizontal': 1320,
    'chrome-horizontal-mobile': 390,
    'view': 1320,
    'modal': 520,
    'gmodal': 1180,
    'sheet': 560,
    'betslip-desktop': 380,
    'swatch': 1320,
}

processed = []
for f in frames:
    body = f['html']
    body = strip_dialog_signals(body)
    body = strip_event_handlers(body)
    body = inputs_to_divs(body)
    body = rename(body)
    width = KIND_WIDTH.get(f['kind'], 1320)
    processed.append({**f, 'html': body, 'width': width})

css = rename(css)

EXTRA_CSS = """
/* ============ design-system board wrapper (not part of painbet's live site) ============ */
html,body.figboard-doc{background:#0e0f10;margin:0}
.figboard{display:flex;flex-wrap:wrap;align-items:flex-start;gap:56px;padding:56px;background:#0e0f10}
.figframe{display:flex;flex-direction:column;gap:12px;flex:none}
.figframe-label{font:800 12px var(--sans);letter-spacing:.08em;text-transform:uppercase;color:#9a9da3}
.figframe-inner{position:relative;background:var(--bg);box-shadow:0 0 0 1px hsla(0,0%,100%,.08)}
.figframe-inner.pad{padding:32px}

/* neutralize fixed/sticky positioning captured from the live app so each frame renders
   in normal document flow at a fixed, predictable size instead of overlaying the page */
.figframe .sidebar{position:relative!important;height:auto!important;top:auto!important;width:100%!important}
.figframe .mobilebar{position:relative!important;left:auto!important;right:auto!important;bottom:auto!important;display:grid!important}
.figframe .card-bg{position:relative!important;inset:auto!important;display:flex!important;padding:0!important;background:transparent!important;backdrop-filter:none!important}
.figframe .gameframe{position:relative!important;inset:auto!important;display:flex!important;padding:0!important;background:transparent!important;backdrop-filter:none!important}
.figframe .gameframe .gframe{width:100%!important;height:600px!important}
.figframe .board-bg{position:relative!important;inset:auto!important;display:flex!important;padding:0!important;background:transparent!important;backdrop-filter:none!important;align-items:flex-start!important}
.figframe .board{max-height:none!important;width:100%!important;animation:none!important}
.figframe .betslip{position:relative!important;right:auto!important;top:auto!important;bottom:auto!important;width:100%!important;box-shadow:none!important}
.figframe .betslip-tab{position:relative!important;right:auto!important;top:auto!important;transform:none!important}
.figframe .view{display:block!important}
.figframe .odds.sel{background:var(--red)}

/* components swatch */
.swatch-board{display:flex;flex-direction:column;gap:28px;width:100%}
.swatch-row{display:flex;flex-direction:column;gap:10px}
.swatch-title{font:800 11px var(--sans);letter-spacing:.1em;text-transform:uppercase;color:var(--ink-lo)}
.swatch-items{display:flex;flex-wrap:wrap;gap:14px;align-items:center}

/* static input replacement */
.inp-el{width:100%;background:transparent;color:var(--white);font:inherit;padding:0}
.inp-el-empty{color:var(--ink-lo)}
"""

BOARD_TITLE = "pain.bet — Design System (extracted from index.html)"

frame_html_parts = []
for f in processed:
    pad = '' if f['kind'] in ('view','swatch') else ' pad'
    frame_html_parts.append(f'''
  <div class="figframe" style="width:{f['width']}px">
    <div class="figframe-label">{htmlmod.escape(f['label'])}</div>
    <div class="figframe-inner{pad}">
{f['html']}
    </div>
  </div>''')

doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{BOARD_TITLE}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<style>
{css}
{EXTRA_CSS}
</style>
</head>
<body class="figboard-doc">
<div class="figboard">
{''.join(frame_html_parts)}
</div>
</body>
</html>
'''

open(OUT, 'w').write(doc)
print('wrote', OUT, len(doc), 'bytes,', len(processed), 'frames')
