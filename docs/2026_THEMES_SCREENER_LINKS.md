# 2026 India Themes — Screener Links (Reopen List)

## Telegram summary
Reference list of Screener.in links for 2026 India themes stocks (semicon/EMS, nuclear revival, power transmission/grid, BESS, data centers, critical minerals etc.). 

Use the reopen script `scripts/open_2026_theme_screener.sh` or the commands below to quickly restore the tabs. PDF version attached for easy offline reference and sharing.

**Purpose:** Store the list of Screener.in tabs for theme-related stocks (semicon/EMS, nuclear, power transmission, BESS, data centers, shipbuilding, critical minerals, etc.).

These tabs were closed during a cleanup session on 2026-07-07. Use this file to reopen them later for research.

**How to keep track:**
- Edit this file when you close more tabs or discover new relevant ones.
- Add new entries in the list below (use consistent format).
- Run the reopen script to open a batch in Chrome.
- For individual research, the per-stock `research/TICKER.md` files often link back to fundamentals.

**Last updated:** 2026-07-07 (from tab cleanup)

## Theme Stocks Screener Links

| Company                  | Ticker / ID     | Screener URL                                      | Theme Notes                  |
|--------------------------|-----------------|---------------------------------------------------|------------------------------|
| Solex Energy             | SOLEX           | https://www.screener.in/company/SOLEX/            | Solar / power equipment     |
| ASM Technologies         | 526433          | https://www.screener.in/company/526433/           | EMS / Semicon               |
| Bondada Engineering      | 543971          | https://www.screener.in/company/543971/           | Power / BESS / Infra        |
| MTAR Technologies        | MTARTECH        | https://www.screener.in/company/MTARTECH/         | Nuclear / Precision         |
| Syrma SGS Technology     | SYRMA           | https://www.screener.in/company/SYRMA/            | EMS / Electronics mfg       |
| CG Power & Industrial    | CGPOWER         | https://www.screener.in/company/CGPOWER/          | Power equipment / Nuclear   |
| Transrail Lighting       | TRANSRAILL      | https://www.screener.in/company/TRANSRAILL/       | Power transmission / Grid   |
| KEC International        | KEC             | https://www.screener.in/company/KEC/              | Power T&D / Transmission    |
| Amber Enterprises        | AMBER           | https://www.screener.in/company/AMBER/            | AC / Data center cooling    |
| MOIL                     | MOIL            | https://www.screener.in/company/MOIL/             | Critical minerals           |
| Walchandnagar Industries | WALCHANNAG      | https://www.screener.in/company/WALCHANNAG/       | Nuclear / Defence           |
| Power Mech Projects      | POWERMECH       | https://www.screener.in/company/POWERMECH/        | Power / Infra EPC           |
| HBL Engineering          | HBLENGINE       | https://www.screener.in/company/HBLENGINE/        | Batteries / Defence         |
| Zen Technologies         | ZENTEC          | https://www.screener.in/company/ZENTEC/           | Defence / Training sims     |
| NILE                     | NILE            | https://www.screener.in/company/NILE/             | Power / Infra               |

## Additional Theme-Related (from research)

Add more here as you research (e.g. RIR, SPEL, MOSCHIP, MICEL, Kilburn, Salzer, WPIL, Azad, TDPOWERSYS, KRN, Quality Power, SPML, Aeroflex, etc.).

## Quick Reopen Commands

### Option 1: Run the script (recommended)
```bash
cd "/Users/nitish/stocks automation"
./scripts/open_2026_theme_screener.sh
```

### Option 2: Copy-paste this one-liner (bash)
```bash
open -a "Google Chrome" "https://www.screener.in/company/SOLEX/" &
open -a "Google Chrome" "https://www.screener.in/company/526433/" &
open -a "Google Chrome" "https://www.screener.in/company/543971/" &
open -a "Google Chrome" "https://www.screener.in/company/MTARTECH/" &
open -a "Google Chrome" "https://www.screener.in/company/SYRMA/" &
open -a "Google Chrome" "https://www.screener.in/company/CGPOWER/" &
open -a "Google Chrome" "https://www.screener.in/company/TRANSRAILL/" &
open -a "Google Chrome" "https://www.screener.in/company/KEC/" &
open -a "Google Chrome" "https://www.screener.in/company/AMBER/" &
open -a "Google Chrome" "https://www.screener.in/company/MOIL/" &
open -a "Google Chrome" "https://www.screener.in/company/WALCHANNAG/" &
open -a "Google Chrome" "https://www.screener.in/company/POWERMECH/" &
open -a "Google Chrome" "https://www.screener.in/company/HBLENGINE/" &
open -a "Google Chrome" "https://www.screener.in/company/ZENTEC/" &
open -a "Google Chrome" "https://www.screener.in/company/NILE/" &
echo "Opened theme Screener tabs. Check Chrome."
```

### Option 3: AppleScript (more control, one window or new tabs)
Copy this into Script Editor or run via terminal:
```applescript
tell application "Google Chrome"
    activate
    set theTabURLs to {"https://www.screener.in/company/SOLEX/", "https://www.screener.in/company/526433/", "https://www.screener.in/company/543971/", "https://www.screener.in/company/MTARTECH/", "https://www.screener.in/company/SYRMA/", "https://www.screener.in/company/CGPOWER/", "https://www.screener.in/company/TRANSRAILL/", "https://www.screener.in/company/KEC/", "https://www.screener.in/company/AMBER/", "https://www.screener.in/company/MOIL/", "https://www.screener.in/company/WALCHANNAG/", "https://www.screener.in/company/POWERMECH/", "https://www.screener.in/company/HBLENGINE/", "https://www.screener.in/company/ZENTEC/", "https://www.screener.in/company/NILE/"}
    set newWin to make new window
    set URL of active tab of newWin to item 1 of theTabURLs
    repeat with i from 2 to count of theTabURLs
        make new tab at end of tabs of newWin with properties {URL:item i of theTabURLs}
    end repeat
end tell
```

## How to Maintain
- When you close more relevant Screener tabs for these themes, add the URLs here.
- When we do another cleanup, ask me to "add the closed ones to the 2026 theme Screener list".
- Cross-reference with individual `research/XXX.md` files and the main India 2026 themes research.
- For broader tracking, see also `docs/FINTWITTER_WATCHLIST.md` (active themes section) and `output/html/portfolio.html`.

**Tip:** You can bookmark this markdown file in Chrome for quick access: `file:///Users/nitish/stocks automation/docs/2026_THEMES_SCREENER_LINKS.md`
