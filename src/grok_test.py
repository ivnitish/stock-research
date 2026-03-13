#!/usr/bin/env python3
"""Test Grok API integration for stocks research cost/speed comparison."""

import os
import json
import requests
from datetime import datetime

def test_grok(query: str, model: str = "grok-4-latest") -> dict:
    """
    Test a single Grok query.

    Args:
        query: The prompt to send
        model: Grok model to use (grok-4-latest, grok-2-latest, etc.)

    Returns:
        dict with response, tokens, cost estimate
    """
    api_key = os.getenv("XAI_API_KEY")
    if not api_key:
        return {"error": "XAI_API_KEY environment variable not set"}

    url = "https://api.x.ai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    payload = {
        "messages": [
            {
                "role": "system",
                "content": "You are a financial research assistant. Be concise and factual.",
            },
            {
                "role": "user",
                "content": query,
            }
        ],
        "model": model,
        "stream": False,
        "temperature": 0,
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()

        result = {
            "model": model,
            "query": query[:50] + "..." if len(query) > 50 else query,
            "response": data["choices"][0]["message"]["content"],
            "input_tokens": data["usage"]["prompt_tokens"],
            "output_tokens": data["usage"]["completion_tokens"],
            "total_tokens": data["usage"]["total_tokens"],
            "timestamp": datetime.now().isoformat(),
        }

        # Rough cost estimate (Grok pricing ~$5/1M input, $15/1M output)
        input_cost = (result["input_tokens"] / 1_000_000) * 5
        output_cost = (result["output_tokens"] / 1_000_000) * 15
        result["estimated_cost_usd"] = round(input_cost + output_cost, 6)

        return result

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


if __name__ == "__main__":
    # Test queries for stocks research
    test_queries = [
        "What is NVIDIA's current stock price and market cap? One sentence.",
        "Summarize NVIDIA's Q4 2024 earnings in 2 sentences.",
        "What are the top 3 risks to NVIDIA's business in 2026?",
    ]

    print("=" * 70)
    print("GROK API TEST — Stocks Research Cost/Speed Benchmark")
    print("=" * 70)
    print(f"\nAPI Key loaded: {bool(os.getenv('XAI_API_KEY'))}")
    print(f"Model: grok-4-latest\n")

    total_cost = 0
    total_tokens = 0

    for i, query in enumerate(test_queries, 1):
        print(f"\n--- Query {i} ---")
        print(f"Q: {query}")

        result = test_grok(query)

        if "error" in result:
            print(f"❌ Error: {result['error']}")
            continue

        print(f"\nA: {result['response'][:150]}...")
        print(f"\nTokens: {result['total_tokens']} (in:{result['input_tokens']} + out:{result['output_tokens']})")
        print(f"Cost: ${result['estimated_cost_usd']:.6f}")

        total_cost += result["estimated_cost_usd"]
        total_tokens += result["total_tokens"]

    print("\n" + "=" * 70)
    print(f"TOTALS: {total_tokens} tokens | ${total_cost:.6f} estimated cost")
    print(f"Cost per 1000 tokens: ${(total_cost / total_tokens * 1000):.4f}")
    print("=" * 70)
    print("\nComparison (Claude API):")
    print("  Claude Sonnet: $3/1M input, $15/1M output")
    print("  Claude Opus:   $15/1M input, $75/1M output")
    print("\nConclusion: Use Grok for high-volume web research; Claude for analysis.")
