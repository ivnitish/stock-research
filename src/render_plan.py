#!/usr/bin/env python3
import sys, re, os

def md_to_html(md):
    html = md
    # Headers
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    # Bold
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    # Italic
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
    # Code inline
    html = re.sub(r'`(.+?)`', r'<code>\1</code>', html)
    # Tables
    lines = html.split('\n')
    out = []; in_table = False; in_list = False
    for line in lines:
        if re.match(r'^\|', line):
            if re.match(r'^\|[-| :]+\|', line): continue
            if not in_table: out.append('<table>'); in_table = True
            cells = [c.strip() for c in line.strip('|').split('|')]
            tag = 'th' if out[-1] == '<table>' else 'td'
            out.append('<tr>'+''.join(f'<{tag}>{c}</{tag}>' for c in cells)+'</tr>')
        else:
            if in_table: out.append('</table>'); in_table = False
            if re.match(r'^- ', line):
                if not in_list: out.append('<ul>'); in_list = True
                out.append('<li>' + line[2:] + '</li>')
            elif re.match(r'^  - ', line):
                out.append('<li style="margin-left:20px">' + line[4:] + '</li>')
            else:
                if in_list: out.append('</ul>'); in_list = False
                if line.strip() == '---': out.append('<hr>')
                elif line.strip() == '': out.append('')
                elif line.strip().startswith('<h') or line.strip().startswith('<hr'): out.append(line)
                else: out.append('<p>' + line + '</p>')
    if in_table: out.append('</table>')
    if in_list: out.append('</ul>')
    return '\n'.join(out)

path = sys.argv[1]
out_dir = sys.argv[2] if len(sys.argv) > 2 else None
with open(path) as f:
    md = f.read()

body = md_to_html(md)
title = os.path.basename(path)
back_btn = '<a href="index.html" class="no-print" style="display:inline-block;margin-bottom:20px;padding:6px 14px;background:#1a1a2e;color:#fff;border-radius:6px;text-decoration:none;font-size:0.85rem;font-weight:500">← Portfolio</a>'
page = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><title>{title}</title>
<style>
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;max-width:960px;margin:40px auto;padding:0 24px;color:#1f2937;line-height:1.7;}}
h1{{font-size:2em;border-bottom:3px solid #1d4ed8;padding-bottom:8px;color:#1e3a5f;}}
h2{{font-size:1.4em;border-bottom:1px solid #e5e7eb;padding-bottom:6px;color:#1d4ed8;margin-top:32px;}}
h3{{font-size:1.1em;color:#374151;margin-top:24px;}}
table{{border-collapse:collapse;width:100%;margin:16px 0;font-size:13.5px;}}
th{{background:#1e3a5f;color:#fff;padding:8px 12px;text-align:left;}}
td{{padding:7px 12px;border-bottom:1px solid #f3f4f6;}}
tr:nth-child(even){{background:#f9fafb;}}
code{{background:#f3f4f6;padding:1px 6px;border-radius:4px;font-size:13px;color:#7c3aed;}}
hr{{border:none;border-top:2px solid #e5e7eb;margin:24px 0;}}
ul{{padding-left:20px;}} li{{margin:4px 0;}}
strong{{color:#111827;}}
@media print{{
  .no-print{{display:none!important;}}
  body{{max-width:100%;margin:0;padding:12px;color:#000;}}
  h1{{color:#000;border-bottom:2px solid #000;font-size:1.6em;}}
  h2{{color:#000;border-bottom:1px solid #666;font-size:1.2em;}}
  h3{{color:#222;}}
  th{{background:#333!important;color:#fff!important;-webkit-print-color-adjust:exact;print-color-adjust:exact;}}
  td{{border-bottom:1px solid #ccc;}}
  tr:nth-child(even){{background:#f5f5f5!important;-webkit-print-color-adjust:exact;print-color-adjust:exact;}}
  code{{background:#eee;color:#333;}}
  a{{color:#000;text-decoration:none;}}
  table{{page-break-inside:avoid;font-size:11px;}}
  h2,h3{{page-break-after:avoid;}}
}}
</style></head><body>{back_btn}{body}<script src="notes.js"></script></body></html>"""

base = os.path.basename(path).replace('.md', '.html')
out = os.path.join(out_dir, base) if out_dir else path.replace('.md', '.html')
with open(out, 'w') as f:
    f.write(page)
print(out)
