# Google Sheets Backend — Setup (5 minutes)

## Step 1 — Create a Google Sheet

1. Go to sheets.google.com → New spreadsheet
2. Name it: `Stock Research — Friend Submissions`
3. Row 1 headers (paste this exactly into A1):
   `Timestamp | Author | Ticker | Company | CMP | MCap | Grade | One-liner | Q1 ROIC | Q2 Runway | Q3 Math | Q4 Kill | Q5 Anchor | Fair Value | Buy Zone | Risks`

## Step 2 — Create Apps Script

1. In the Sheet: Extensions → Apps Script
2. Delete all existing code, paste this:

```javascript
function doPost(e) {
  try {
    const ss   = SpreadsheetApp.getActiveSpreadsheet();
    const data = JSON.parse(e.postData.contents);

    if (data.type === 'note') {
      // ── Research note on an existing stock ──
      const notesSheet = ss.getSheetByName('Notes') || ss.insertSheet('Notes');
      if (notesSheet.getLastRow() === 0) {
        notesSheet.appendRow(['Timestamp', 'Ticker', 'Author', 'Note']);
      }
      notesSheet.appendRow([data.submitted_at, data.ticker, data.author, data.note]);

    } else {
      // ── Full thesis submission ──
      const thesisSheet = ss.getSheetByName('Theses') || ss.getActiveSheet();
      thesisSheet.appendRow([
        data.submitted_at, data.author, data.ticker, data.company,
        data.cmp, data.mcap, data.grade, data.one_liner,
        data.q1, data.q2, data.q3, data.q4, data.q5,
        data.fair_value, data.buy_zone, data.risks
      ]);
    }

    return ContentService
      .createTextOutput(JSON.stringify({ result: 'success' }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch(err) {
    return ContentService
      .createTextOutput(JSON.stringify({ result: 'error', error: err.message }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}
```

3. Save (Ctrl+S)

## Step 3 — Deploy as Web App

1. Click **Deploy** → **New deployment**
2. Click the gear icon next to "Type" → select **Web app**
3. Settings:
   - Description: `Thesis submission endpoint`
   - Execute as: **Me**
   - Who has access: **Anyone** (so your friend can submit without a Google account)
4. Click **Deploy**
5. Copy the **Web app URL** (looks like `https://script.google.com/macros/s/ABC.../exec`)

## Step 3b — Publish the Notes tab (so stock pages can read notes)

After the first note is added (or manually create the Notes tab):

1. In the Sheet: **File → Share → Publish to web**
2. Select the **Notes** tab (not the whole document)
3. Format: **Comma-separated values (.csv)**
4. Click **Publish** → copy the URL

This URL goes into `notes.js` (see Step 4b below).

## Step 4 — Paste URL into submit.html

Open `/Users/nitish/stocks automation/output/html/submit.html`

Find this line:
```javascript
const APPS_SCRIPT_URL = 'YOUR_APPS_SCRIPT_URL_HERE';
```

Replace with your actual URL:
```javascript
const APPS_SCRIPT_URL = 'https://script.google.com/macros/s/YOUR_ID/exec';
```

Then push to GitHub.

## Step 4b — Paste URLs into notes.js

Open `/Users/nitish/stocks automation/output/html/notes.js`

Replace both placeholders:
```javascript
const SHEET_CSV_URL   = 'https://docs.google.com/spreadsheets/d/YOUR_ID/pub?output=csv&gid=NOTES_GID';
const APPS_SCRIPT_URL = 'https://script.google.com/macros/s/YOUR_ID/exec';
```

Then push to GitHub. Every stock thesis page will now show notes and allow adding new ones.

## Step 5 — Share link with friend

Send them: `https://ivnitish.github.io/stock-research/submit.html`

That's it. Every submission appears as a new row in your Sheet instantly.

---

## Reviewing Submissions

Open the Google Sheet — each row is a full thesis with all Q&A answers.
You can then paste promising theses into Claude and ask it to score them
against the Quality Score framework (Section 2 of _TEMPLATE.md).
