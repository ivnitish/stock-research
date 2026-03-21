/**
 * notes.js — Research Notes Widget
 * Shared across all thesis pages. Auto-detects ticker from filename.
 * Reads from Google Sheets (published CSV). Writes via Apps Script.
 *
 * Setup: see docs/SHEETS_SETUP.md
 */

(function() {
  // ── Config (fill these in after Sheet setup) ──
  const SHEET_CSV_URL   = 'YOUR_PUBLISHED_NOTES_CSV_URL';   // File→Share→Publish to web→Notes tab→CSV
  const APPS_SCRIPT_URL = 'YOUR_APPS_SCRIPT_URL_HERE';      // same URL as submit.html

  // ── Detect ticker from page filename ──
  const ticker = window.location.pathname
    .split('/').pop()
    .replace('.html', '')
    .toUpperCase();

  if (!ticker || ticker === 'INDEX' || ticker === 'SUBMIT') return;

  // ── Inject widget into page ──
  const widget = document.createElement('div');
  widget.id = 'notes-widget';
  widget.innerHTML = `
    <div style="max-width:960px;margin:40px auto 0;padding:0 24px 60px">
      <div style="border-top:2px solid #e5e7eb;padding-top:28px">
        <div style="font-size:0.68rem;text-transform:uppercase;letter-spacing:1px;color:#9ca3af;margin-bottom:6px">Research Notes</div>
        <h2 style="font-size:1.1rem;font-weight:700;color:#1a1a2e;margin:0 0 18px">${ticker} — Points to Consider</h2>

        <div id="notes-list" style="margin-bottom:24px"></div>

        <div style="background:#f8f9ff;border:1px solid #e0e4f0;border-radius:10px;padding:18px">
          <div style="font-size:0.78rem;font-weight:600;color:#374151;margin-bottom:10px">Add a note</div>
          <textarea id="note-text"
            style="width:100%;padding:9px 12px;border:1px solid #d1d5db;border-radius:7px;font-size:0.85rem;font-family:inherit;resize:vertical;min-height:80px;outline:none;color:#1f2937;background:white"
            placeholder="Observation, data point, concern, or catalyst worth tracking…"></textarea>
          <div style="display:flex;gap:10px;margin-top:10px;align-items:center">
            <input id="note-author"
              style="flex:0 0 160px;padding:8px 12px;border:1px solid #d1d5db;border-radius:7px;font-size:0.82rem;font-family:inherit;outline:none;background:white"
              placeholder="Your name" />
            <button id="note-submit"
              style="padding:8px 20px;background:#1a1a2e;color:white;border:none;border-radius:7px;font-size:0.82rem;font-weight:600;cursor:pointer">
              Save Note
            </button>
            <span id="note-status" style="font-size:0.78rem;color:#6b7280"></span>
          </div>
        </div>
      </div>
    </div>
  `;
  document.body.appendChild(widget);

  // ── Load existing notes ──
  function loadNotes() {
    const list = document.getElementById('notes-list');
    if (SHEET_CSV_URL.startsWith('YOUR_')) {
      list.innerHTML = '<p style="font-size:0.8rem;color:#9ca3af;font-style:italic">Notes not configured yet — see SHEETS_SETUP.md</p>';
      return;
    }

    fetch(SHEET_CSV_URL + '&t=' + Date.now()) // cache-bust
      .then(r => r.text())
      .then(csv => {
        const rows = parseCSV(csv).filter(r => r.ticker && r.ticker.toUpperCase() === ticker);
        if (rows.length === 0) {
          list.innerHTML = '<p style="font-size:0.8rem;color:#9ca3af;font-style:italic">No notes yet — be the first to add one.</p>';
          return;
        }
        // newest first
        rows.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
        list.innerHTML = rows.map(r => `
          <div style="background:white;border:1px solid #e5e7eb;border-radius:8px;padding:12px 16px;margin-bottom:10px">
            <div style="font-size:0.75rem;color:#9ca3af;margin-bottom:5px">
              <strong style="color:#374151">${esc(r.author || 'Anonymous')}</strong>
              &nbsp;·&nbsp;${formatDate(r.timestamp)}
            </div>
            <div style="font-size:0.86rem;color:#1f2937;line-height:1.6;white-space:pre-wrap">${esc(r.note)}</div>
          </div>
        `).join('');
      })
      .catch(() => {
        list.innerHTML = '<p style="font-size:0.8rem;color:#9ca3af">Could not load notes.</p>';
      });
  }

  // ── Submit new note ──
  document.getElementById('note-submit').addEventListener('click', function() {
    const text   = document.getElementById('note-text').value.trim();
    const author = document.getElementById('note-author').value.trim() || 'Anonymous';
    const status = document.getElementById('note-status');

    if (!text) { status.textContent = 'Write something first.'; return; }
    if (APPS_SCRIPT_URL.startsWith('YOUR_')) {
      status.textContent = 'Not configured yet — see SHEETS_SETUP.md';
      return;
    }

    this.disabled = true;
    this.textContent = 'Saving…';
    status.textContent = '';

    fetch(APPS_SCRIPT_URL, {
      method: 'POST',
      body: JSON.stringify({
        type: 'note',
        ticker: ticker,
        author: author,
        note: text,
        submitted_at: new Date().toISOString()
      })
    })
    .then(r => r.json())
    .then(json => {
      if (json.result === 'success') {
        document.getElementById('note-text').value = '';
        status.style.color = '#166534';
        status.textContent = '✓ Saved';
        setTimeout(() => { status.textContent = ''; loadNotes(); }, 800);
      } else throw new Error(json.error);
    })
    .catch(err => {
      status.style.color = '#991b1b';
      status.textContent = 'Error: ' + err.message;
    })
    .finally(() => {
      this.disabled = false;
      this.textContent = 'Save Note';
    });
  });

  // ── Helpers ──
  function parseCSV(csv) {
    const lines = csv.trim().split('\n');
    const headers = lines[0].split(',').map(h => h.trim().toLowerCase().replace(/\s+/g, '_'));
    return lines.slice(1).map(line => {
      // handle commas inside quoted fields
      const vals = [];
      let cur = '', inQ = false;
      for (let i = 0; i < line.length; i++) {
        if (line[i] === '"') { inQ = !inQ; }
        else if (line[i] === ',' && !inQ) { vals.push(cur); cur = ''; }
        else { cur += line[i]; }
      }
      vals.push(cur);
      const obj = {};
      headers.forEach((h, i) => { obj[h] = (vals[i] || '').trim(); });
      return obj;
    });
  }

  function esc(s) {
    return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  }

  function formatDate(iso) {
    if (!iso) return '';
    try {
      const d = new Date(iso);
      return d.toLocaleDateString('en-IN', { day:'numeric', month:'short', year:'numeric' });
    } catch { return iso; }
  }

  loadNotes();
})();
