#!/bin/bash
# Reopen the 2026 India Themes Screener tabs
# Usage: ./scripts/open_2026_theme_screener.sh
# Or from repo root: bash scripts/open_2026_theme_screener.sh

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LINKS_FILE="$REPO_ROOT/docs/2026_THEMES_SCREENER_LINKS.md"

echo "Opening 2026 India Themes Screener tabs in Google Chrome..."

# List of URLs (keep in sync with docs/2026_THEMES_SCREENER_LINKS.md)
URLS=(
  "https://www.screener.in/company/SOLEX/"
  "https://www.screener.in/company/526433/"
  "https://www.screener.in/company/543971/"
  "https://www.screener.in/company/MTARTECH/"
  "https://www.screener.in/company/SYRMA/"
  "https://www.screener.in/company/CGPOWER/"
  "https://www.screener.in/company/TRANSRAILL/"
  "https://www.screener.in/company/KEC/"
  "https://www.screener.in/company/AMBER/"
  "https://www.screener.in/company/MOIL/"
  "https://www.screener.in/company/WALCHANNAG/"
  "https://www.screener.in/company/POWERMECH/"
  "https://www.screener.in/company/HBLENGINE/"
  "https://www.screener.in/company/ZENTEC/"
  "https://www.screener.in/company/NILE/"
)

for url in "${URLS[@]}"; do
  open -a "Google Chrome" "$url"
  sleep 0.3  # small delay to avoid overwhelming Chrome
done

echo "Done. ${#URLS[@]} Screener tabs should now be open in Chrome."
echo "Edit $LINKS_FILE to add/remove stocks."
