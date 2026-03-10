"""
DCF (Discounted Cash Flow) valuation model.
3 scenarios (bear/base/bull) + reverse DCF ("what growth makes this a Nx?").

Usage:
  from src.dcf_model import dcf_valuation, reverse_dcf

  # Forward DCF
  result = dcf_valuation(
      current_fcf=1824,        # Latest annual FCF/net profit (Cr)
      growth_rates=[0.30, 0.25, 0.20, 0.15, 0.12],  # 5-year growth rates
      terminal_growth=0.05,    # Long-term growth
      discount_rate=0.12,      # WACC / required return
      shares_crores=628,       # Shares outstanding (in crores)
  )

  # Reverse DCF: what growth rate justifies current price?
  implied = reverse_dcf(
      current_price=157,
      current_fcf=1824,
      shares_crores=628,
      discount_rate=0.12,
      terminal_growth=0.05,
      years=5,
  )
"""
from __future__ import annotations


def dcf_valuation(
    current_fcf: float,
    growth_rates: list[float],
    terminal_growth: float = 0.05,
    discount_rate: float = 0.12,
    shares_crores: float = 1.0,
) -> dict:
    """
    Multi-stage DCF.
    growth_rates: list of annual growth rates for projection period (e.g. [0.30, 0.25, ...])
    Returns dict with projected FCFs, terminal value, intrinsic value per share.
    """
    years = len(growth_rates)
    fcfs = []
    fcf = current_fcf

    # Project FCFs
    for i, g in enumerate(growth_rates):
        fcf = fcf * (1 + g)
        pv = fcf / (1 + discount_rate) ** (i + 1)
        fcfs.append({"year": i + 1, "fcf": round(fcf, 1), "pv": round(pv, 1), "growth": g})

    # Terminal value (Gordon Growth)
    terminal_fcf = fcfs[-1]["fcf"] * (1 + terminal_growth)
    terminal_value = terminal_fcf / (discount_rate - terminal_growth)
    pv_terminal = terminal_value / (1 + discount_rate) ** years

    # Sum
    pv_fcfs = sum(f["pv"] for f in fcfs)
    enterprise_value = pv_fcfs + pv_terminal
    value_per_share = enterprise_value / shares_crores if shares_crores else 0

    return {
        "projected_fcfs": fcfs,
        "terminal_value": round(terminal_value, 1),
        "pv_terminal": round(pv_terminal, 1),
        "pv_fcfs": round(pv_fcfs, 1),
        "enterprise_value": round(enterprise_value, 1),
        "value_per_share": round(value_per_share, 2),
        "assumptions": {
            "current_fcf": current_fcf,
            "growth_rates": growth_rates,
            "terminal_growth": terminal_growth,
            "discount_rate": discount_rate,
            "shares_crores": shares_crores,
        },
    }


def dcf_3_scenarios(
    current_fcf: float,
    shares_crores: float,
    discount_rate: float = 0.12,
    terminal_growth: float = 0.05,
    bear_growth: list[float] | None = None,
    base_growth: list[float] | None = None,
    bull_growth: list[float] | None = None,
) -> dict:
    """Run bear/base/bull DCF scenarios. Returns dict with all three."""
    if bear_growth is None:
        bear_growth = [0.15, 0.12, 0.10, 0.08, 0.06]
    if base_growth is None:
        base_growth = [0.25, 0.20, 0.18, 0.15, 0.12]
    if bull_growth is None:
        bull_growth = [0.35, 0.30, 0.25, 0.20, 0.15]

    scenarios = {}
    for name, rates in [("bear", bear_growth), ("base", base_growth), ("bull", bull_growth)]:
        scenarios[name] = dcf_valuation(
            current_fcf=current_fcf,
            growth_rates=rates,
            terminal_growth=terminal_growth,
            discount_rate=discount_rate,
            shares_crores=shares_crores,
        )
    return scenarios


def reverse_dcf(
    current_price: float,
    current_fcf: float,
    shares_crores: float,
    discount_rate: float = 0.12,
    terminal_growth: float = 0.05,
    years: int = 5,
) -> dict:
    """
    What constant FCF growth rate justifies the current market price?
    Uses binary search to find implied growth.
    """
    target_ev = current_price * shares_crores

    lo, hi = -0.10, 1.00
    for _ in range(100):
        mid = (lo + hi) / 2
        rates = [mid] * years
        result = dcf_valuation(current_fcf, rates, terminal_growth, discount_rate, shares_crores)
        if result["enterprise_value"] < target_ev:
            lo = mid
        else:
            hi = mid

    implied_growth = round((lo + hi) / 2, 4)
    return {
        "implied_growth_rate": implied_growth,
        "implied_growth_pct": round(implied_growth * 100, 2),
        "current_price": current_price,
        "market_cap_cr": round(current_price * shares_crores, 1),
        "interpretation": f"Market is pricing in {implied_growth*100:.1f}% FCF CAGR for {years} years",
    }


def print_scenarios(scenarios: dict, current_price: float):
    """Pretty-print 3-scenario DCF results."""
    print(f"\n{'Scenario':<8} {'Value/Share':>12} {'vs Price':>10} {'Upside':>8}")
    print("-" * 42)
    for name in ["bear", "base", "bull"]:
        s = scenarios[name]
        vps = s["value_per_share"]
        upside = (vps / current_price - 1) * 100
        print(f"{name:<8} ₹{vps:>10.2f} {'':>2} ₹{current_price:.0f} {upside:>+7.1f}%")


if __name__ == "__main__":
    # GROWW example
    print("=== GROWW DCF Valuation ===")
    print("Using FY25 net profit ₹1,824 Cr as proxy for FCF")
    print("Shares: ~628 Cr (post-IPO)")

    scenarios = dcf_3_scenarios(
        current_fcf=1824,
        shares_crores=628,
        discount_rate=0.12,
        terminal_growth=0.05,
    )
    print_scenarios(scenarios, current_price=157)

    print("\n--- Reverse DCF ---")
    rev = reverse_dcf(157, 1824, 628, 0.12, 0.05, 5)
    print(f"  {rev['interpretation']}")
