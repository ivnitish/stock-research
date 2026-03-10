"""
P/B-ROE (Justified Price-to-Book) valuation model.

Theory: A stock's fair P/B ratio is determined by its ROE relative to cost of equity.
  Justified P/B = (ROE - g) / (CoE - g)
  If ROE > CoE → stock deserves premium to book (P/B > 1)
  If ROE < CoE → stock should trade below book (P/B < 1)

This is more meaningful than P/E for:
- Financial companies (banks, brokers like GROWW)
- Capital-heavy businesses
- Companies where book value is a real economic asset

Usage:
  from src.pb_roe_model import justified_pb, pb_roe_valuation, pb_roe_scenarios

  val = pb_roe_valuation(
      book_value_per_share=11.9,
      roe=0.50,
      cost_of_equity=0.12,
      growth=0.15,
      current_price=157,
  )
"""
from __future__ import annotations


def justified_pb(
    roe: float,
    cost_of_equity: float = 0.12,
    growth: float = 0.05,
) -> float:
    """
    Gordon Growth justified P/B = (ROE - g) / (CoE - g).
    roe, cost_of_equity, growth as decimals (e.g. 0.50 for 50%).
    """
    if cost_of_equity <= growth:
        # When growth >= CoE, Gordon model breaks. Use residual income approach instead:
        # P/B ≈ 1 + (ROE - CoE) / CoE × years_of_excess (assume 10 years)
        excess_years = 10
        return 1 + (roe - cost_of_equity) / cost_of_equity * excess_years
    return (roe - growth) / (cost_of_equity - growth)


def pb_roe_valuation(
    book_value_per_share: float,
    roe: float,
    cost_of_equity: float = 0.12,
    growth: float = 0.10,
    current_price: float = 0,
    current_pb: float | None = None,
) -> dict:
    """
    Full P/B-ROE valuation.
    Returns justified P/B, fair value, and comparison to current price.
    """
    j_pb = justified_pb(roe, cost_of_equity, growth)
    fair_value = book_value_per_share * j_pb

    if current_pb is None and current_price > 0 and book_value_per_share > 0:
        current_pb = current_price / book_value_per_share

    upside = ((fair_value / current_price) - 1) * 100 if current_price > 0 else None

    # ROE decomposition insight
    roe_spread = roe - cost_of_equity
    verdict = "CREATES value" if roe_spread > 0 else "DESTROYS value"

    return {
        "justified_pb": round(j_pb, 2),
        "fair_value": round(fair_value, 2),
        "current_price": current_price,
        "current_pb": round(current_pb, 2) if current_pb else None,
        "upside_pct": round(upside, 1) if upside is not None else None,
        "roe_spread": round(roe_spread * 100, 1),
        "verdict": f"ROE {roe*100:.0f}% vs CoE {cost_of_equity*100:.0f}% → {verdict} (spread: {roe_spread*100:.1f}%)",
        "assumptions": {
            "book_value_per_share": book_value_per_share,
            "roe": roe,
            "cost_of_equity": cost_of_equity,
            "growth": growth,
        },
    }


def pb_roe_scenarios(
    book_value_per_share: float,
    current_price: float,
    cost_of_equity: float = 0.12,
    bear_roe: float = 0.25,
    base_roe: float = 0.40,
    bull_roe: float = 0.50,
    bear_growth: float = 0.08,
    base_growth: float = 0.12,
    bull_growth: float = 0.18,
) -> dict:
    """3-scenario P/B-ROE valuation."""
    scenarios = {}
    for name, roe, g in [
        ("bear", bear_roe, bear_growth),
        ("base", base_roe, base_growth),
        ("bull", bull_roe, bull_growth),
    ]:
        scenarios[name] = pb_roe_valuation(
            book_value_per_share=book_value_per_share,
            roe=roe,
            cost_of_equity=cost_of_equity,
            growth=g,
            current_price=current_price,
        )
    return scenarios


def implied_roe(
    current_price: float,
    book_value_per_share: float,
    cost_of_equity: float = 0.12,
    growth: float = 0.10,
) -> dict:
    """What ROE does the market price imply?"""
    current_pb = current_price / book_value_per_share if book_value_per_share > 0 else 0
    # justified_pb = (ROE - g) / (CoE - g)
    # ROE = justified_pb * (CoE - g) + g
    implied = current_pb * (cost_of_equity - growth) + growth
    return {
        "implied_roe": round(implied, 4),
        "implied_roe_pct": round(implied * 100, 2),
        "current_pb": round(current_pb, 2),
        "interpretation": f"At P/B {current_pb:.1f}x, market implies ROE of {implied*100:.1f}% (sustainable)",
    }


def print_scenarios(scenarios: dict, current_price: float):
    """Pretty-print 3-scenario results."""
    print(f"\n{'Scenario':<8} {'ROE':>6} {'Just P/B':>9} {'Fair Val':>10} {'Upside':>8}")
    print("-" * 46)
    for name in ["bear", "base", "bull"]:
        s = scenarios[name]
        roe = s["assumptions"]["roe"] * 100
        print(f"{name:<8} {roe:>5.0f}% {s['justified_pb']:>8.1f}x ₹{s['fair_value']:>8.0f} {s['upside_pct']:>+7.1f}%")


if __name__ == "__main__":
    print("=== GROWW P/B-ROE Valuation ===")
    print("Book Value: ₹11.9/share | Current ROE: 50% | Price: ₹157\n")

    scenarios = pb_roe_scenarios(
        book_value_per_share=11.9,
        current_price=157,
        cost_of_equity=0.12,
        bear_roe=0.25, bear_growth=0.08,
        base_roe=0.40, base_growth=0.12,
        bull_roe=0.50, bull_growth=0.18,
    )
    print_scenarios(scenarios, 157)

    print("\n--- Implied ROE ---")
    imp = implied_roe(157, 11.9, 0.12, 0.10)
    print(f"  {imp['interpretation']}")

    print("\n--- What this means ---")
    print("  If GROWW sustains ROE of 50%, justified P/B is very high")
    print("  because ROE (50%) >> Cost of Equity (12%)")
    print("  The key question: can 50% ROE sustain as book value grows?")
