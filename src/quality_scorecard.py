"""
Munger-style quality scorecard for stock evaluation.
5 dimensions, each rated 1-5. Total /25. Grade: A/B/C/D.

Usage:
  from src.quality_scorecard import QualityScore, save_scorecard, load_scorecard

  score = QualityScore(
      symbol="GROWW.NS",
      moat=4, moat_notes="Strong network effects in broking, 14M+ users",
      management=3, management_notes="New public company, limited capital allocation track record",
      financials=4, financials_notes="Profitable, low debt, strong margins",
      growth=5, growth_notes="India fintech TAM massive, <5% penetration",
      valuation=3, valuation_notes="P/E 57 is rich but growth justifies if sustained",
  )
  save_scorecard(score)
"""
from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass, asdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import RESEARCH_DIR


@dataclass
class QualityScore:
    symbol: str

    # Each dimension: 1 (poor) to 5 (excellent)
    moat: int = 0
    moat_notes: str = ""

    management: int = 0
    management_notes: str = ""

    financials: int = 0
    financials_notes: str = ""

    growth: int = 0
    growth_notes: str = ""

    valuation: int = 0
    valuation_notes: str = ""

    @property
    def total(self) -> int:
        return self.moat + self.management + self.financials + self.growth + self.valuation

    @property
    def grade(self) -> str:
        t = self.total
        if t >= 20:
            return "A"  # High conviction
        if t >= 15:
            return "B"  # Moderate conviction
        if t >= 10:
            return "C"  # Watch / weak
        return "D"  # Avoid

    @property
    def grade_label(self) -> str:
        labels = {"A": "High Conviction", "B": "Moderate", "C": "Watch", "D": "Avoid"}
        return labels.get(self.grade, "")

    def summary(self) -> str:
        lines = [
            f"Quality Score: {self.symbol} — {self.total}/25 (Grade {self.grade}: {self.grade_label})",
            f"  MOAT:       {self.moat}/5  {self.moat_notes}",
            f"  Management: {self.management}/5  {self.management_notes}",
            f"  Financials: {self.financials}/5  {self.financials_notes}",
            f"  Growth:     {self.growth}/5  {self.growth_notes}",
            f"  Valuation:  {self.valuation}/5  {self.valuation_notes}",
        ]
        return "\n".join(lines)


def _scorecard_path(symbol: str) -> str:
    clean = symbol.replace(".NS", "").replace(".BO", "").upper()
    return os.path.join(RESEARCH_DIR, f"{clean}_scorecard.json")


def save_scorecard(score: QualityScore) -> str:
    path = _scorecard_path(score.symbol)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(asdict(score), f, indent=2)
    return path


def load_scorecard(symbol: str) -> QualityScore | None:
    path = _scorecard_path(symbol)
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return QualityScore(**json.load(f))


if __name__ == "__main__":
    # Demo with placeholder — fill in real scores during thesis work
    demo = QualityScore(
        symbol="GROWW.NS",
        moat=4, moat_notes="Network effects, 14M+ users, brand in young India",
        management=3, management_notes="Founder-led, new public co, limited capital allocation history",
        financials=4, financials_notes="Profitable, ~45% net margin, minimal debt",
        growth=5, growth_notes="India fintech TAM massive, mutual fund + broking penetration <5%",
        valuation=3, valuation_notes="P/E ~57 is rich; forward P/E ~34 if growth sustains",
    )
    print(demo.summary())
    path = save_scorecard(demo)
    print(f"\nSaved: {path}")
