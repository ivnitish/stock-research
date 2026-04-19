#!/usr/bin/env python3
"""
render_plan.py — Convert a Markdown research file to a styled HTML page.

Usage:
  python3 src/render_plan.py research/NEWGEN.md            # saves alongside .md
  python3 src/render_plan.py research/NEWGEN.md output/html/  # saves to output dir

Private data handling (hidden in print/PDF, visible in browser):
  Option 1 — Explicit blocks:
    <!-- PRIVATE -->
    Any content here is hidden in PDF/print
    <!-- /PRIVATE -->

  Option 2 — Auto-detected lines:
    Any line containing **Entry:** or **P&L:** is auto-wrapped as private.
    The entire "Decision History" section is auto-wrapped as private.
"""

import sys, re, os

# ---------------------------------------------------------------------------
# Step 1: Pre-process markdown — wrap PRIVATE blocks before HTML conversion
# ---------------------------------------------------------------------------

def preprocess_private(md):
    """Wrap <!-- PRIVATE --> blocks and auto-detect private lines."""

    # 1a. Explicit <!-- PRIVATE --> ... <!-- /PRIVATE --> blocks
    md = re.sub(
        r'<!--\s*PRIVATE\s*-->(.*?)<!--\s*/PRIVATE\s*-->',
        lambda m: f'\n<div class="sr-private">{m.group(1)}</div>\n',
        md, flags=re.DOTALL
    )

    # 1b. Auto-detect lines with Entry: or P&L: in bold markdown
    lines = []
    for line in md.split('\n'):
        if re.search(r'\*\*Entry:\*\*|\*\*P&L:\*\*', line):
            lines.append(f'<p class="sr-private">{line}</p>')
        else:
            lines.append(line)
    md = '\n'.join(lines)

    return md


def wrap_decision_history(html_body):
    """
    After full HTML conversion, wrap the Decision History section
    (section 10 in research files) in sr-private.
    This catches the entire section between the Decision History h2
    and the next h2.
    """
    # Find Decision History section and wrap until next h2
    pattern = re.compile(
        r'(<h2[^>]*>[^<]*[Dd]ecision\s+[Hh]istory[^<]*</h2>)(.*?)(<h2)',
        re.DOTALL
    )
    return pattern.sub(
        r'<div class="sr-private">\1\2</div>\3',
        html_body
    )


# ---------------------------------------------------------------------------
# Step 2: Markdown → HTML conversion
# ---------------------------------------------------------------------------

def md_to_html(md):
    html = md

    # Headers with anchor IDs
    def make_id(text): return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')
    html = re.sub(r'^### (.+)$', lambda m: f'<h3 id="{make_id(m.group(1))}">{m.group(1)}</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$',  lambda m: f'<h2 id="{make_id(m.group(1))}">{m.group(1)}</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.+)$',   lambda m: f'<h1 id="{make_id(m.group(1))}">{m.group(1)}</h1>', html, flags=re.MULTILINE)

    # Bold, italic, inline code
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*',     r'<em>\1</em>', html)
    html = re.sub(r'`(.+?)`',       r'<code>\1</code>', html)

    # Tables and lists (line-by-line)
    lines = html.split('\n')
    out = []; in_table = False; in_list = False

    for line in lines:
        # Pass-through already-converted HTML blocks
        stripped = line.strip()
        if stripped.startswith('<h') or stripped.startswith('<hr') \
                or stripped.startswith('<div') or stripped.startswith('</div') \
                or stripped.startswith('<p class=') or stripped.startswith('<ul') \
                or stripped.startswith('</ul') or stripped.startswith('<li'):
            if in_table: out.append('</table>'); in_table = False
            if in_list:  out.append('</ul>');    in_list  = False
            out.append(line)
            continue

        if re.match(r'^\|', line):
            if re.match(r'^\|[-| :]+\|', line): continue
            if not in_table: out.append('<table>'); in_table = True
            cells = [c.strip() for c in line.strip('|').split('|')]
            tag = 'th' if out[-1] == '<table>' else 'td'
            out.append('<tr>' + ''.join(f'<{tag}>{c}</{tag}>' for c in cells) + '</tr>')
        else:
            if in_table: out.append('</table>'); in_table = False
            if re.match(r'^- ', line):
                if not in_list: out.append('<ul>'); in_list = True
                out.append('<li>' + line[2:] + '</li>')
            elif re.match(r'^  - ', line):
                out.append('<li style="margin-left:20px">' + line[4:] + '</li>')
            else:
                if in_list: out.append('</ul>'); in_list = False
                if stripped == '---': out.append('<hr>')
                elif stripped == '':  out.append('')
                else:                 out.append('<p>' + line + '</p>')

    if in_table: out.append('</table>')
    if in_list:  out.append('</ul>')
    return '\n'.join(out)


# ---------------------------------------------------------------------------
# Step 3: Assemble full HTML page
# ---------------------------------------------------------------------------

CSS = """
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;max-width:960px;margin:40px auto;padding:0 24px;color:#1f2937;line-height:1.7;}
h1{font-size:2em;border-bottom:3px solid #1d4ed8;padding-bottom:8px;color:#1e3a5f;}
h2{font-size:1.4em;border-bottom:1px solid #e5e7eb;padding-bottom:6px;color:#1d4ed8;margin-top:32px;}
h3{font-size:1.1em;color:#374151;margin-top:24px;}
table{border-collapse:collapse;width:100%;margin:16px 0;font-size:13.5px;}
th{background:#1e3a5f;color:#fff;padding:8px 12px;text-align:left;}
td{padding:7px 12px;border-bottom:1px solid #f3f4f6;}
tr:nth-child(even){background:#f9fafb;}
code{background:#f3f4f6;padding:1px 6px;border-radius:4px;font-size:13px;color:#7c3aed;}
hr{border:none;border-top:2px solid #e5e7eb;margin:24px 0;}
ul{padding-left:20px;} li{margin:4px 0;}
strong{color:#111827;}
/* Private blocks: visible in browser, hidden in print/PDF */
.sr-private{border-left:3px solid #fbbf24;padding-left:8px;background:#fffbeb;}
#toc{position:fixed;top:80px;right:16px;width:200px;background:#fff;border:1px solid #e5e7eb;border-radius:8px;padding:12px;font-size:12px;max-height:70vh;overflow-y:auto;box-shadow:0 2px 8px rgba(0,0,0,.08);z-index:100;}
#toc summary{font-weight:600;cursor:pointer;color:#1d4ed8;margin-bottom:6px;}
#toc a{display:block;color:#374151;text-decoration:none;padding:2px 0;line-height:1.4;}
#toc a:hover{color:#1d4ed8;}
@media(max-width:1200px){#toc{display:none;}}
@media print{
  .no-print{display:none!important;}
  .sr-private{display:none!important;}
  body{max-width:100%;margin:0;padding:12px;color:#000;}
  h1{color:#000;border-bottom:2px solid #000;font-size:1.6em;}
  h2{color:#000;border-bottom:1px solid #666;font-size:1.2em;}
  h3{color:#222;}
  th{background:#333!important;color:#fff!important;-webkit-print-color-adjust:exact;print-color-adjust:exact;}
  td{border-bottom:1px solid #ccc;}
  tr:nth-child(even){background:#f5f5f5!important;-webkit-print-color-adjust:exact;print-color-adjust:exact;}
  code{background:#eee;color:#333;}
  a{color:#000;text-decoration:none;}
  table{page-break-inside:avoid;font-size:11px;}
  h2,h3{page-break-after:avoid;}
}
"""

path = sys.argv[1]
out_dir = sys.argv[2] if len(sys.argv) > 2 else None

with open(path) as f:
    md = f.read()

# Strip HTML comments (<!-- ... -->) that aren't PRIVATE markers — avoids them showing in output
md = re.sub(r'<!--(?!\s*/?PRIVATE).*?-->', '', md, flags=re.DOTALL)

md     = preprocess_private(md)
body   = md_to_html(md)
body   = wrap_decision_history(body)
title  = os.path.basename(path)

back_btn = '<a href="index.html" class="no-print" style="display:inline-block;margin-bottom:20px;padding:6px 14px;background:#1a1a2e;color:#fff;border-radius:6px;text-decoration:none;font-size:0.85rem;font-weight:500">← Portfolio</a>'

page = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><title>{title}</title>
<style>{CSS}</style></head><body>{back_btn}
<details id="toc" class="no-print"><summary>Jump to section</summary></details>
{body}
<script src="notes.js"></script>
<script>
var toc=document.getElementById('toc');
document.querySelectorAll('h2').forEach(function(h){{
  var a=document.createElement('a');
  a.href='#'+h.id; a.textContent=h.textContent;
  toc.appendChild(a);
}});
if(toc.querySelectorAll('a').length===0)toc.style.display='none';
</script>
</body></html>"""

base = os.path.basename(path).replace('.md', '.html')
out  = os.path.join(out_dir, base) if out_dir else path.replace('.md', '.html')
with open(out, 'w') as f:
    f.write(page)
print(out)
