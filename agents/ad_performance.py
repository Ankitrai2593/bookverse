#!/usr/bin/env python3
"""
Ad Performance Tracker
----------------------
Logs daily advertising metrics, generates weekly/monthly summaries,
and flags performance issues (low ROAS, high CPA, low CTR).

Usage:
    python ad_performance.py                 # Full report
    python ad_performance.py --init          # Re-generate 30 days of sample data
    python ad_performance.py --log           # Interactive: log today's metrics
"""

import json
import math
import os
import random
import sys
from datetime import datetime, timedelta

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
METRICS_FILE = os.path.join(BASE_DIR, "ad_metrics.json")
AD_ALERTS_FILE = os.path.join(BASE_DIR, "ad_alerts.json")

# Alert thresholds
MIN_ROAS = 2.0       # Minimum acceptable ROAS
MAX_CPA = 150.0      # Maximum acceptable CPA in INR
MIN_CTR = 1.0        # Minimum acceptable CTR in %


# ---------------------------------------------------------------------------
# Data model helpers
# ---------------------------------------------------------------------------

def _load_metrics() -> dict:
    """Load metrics from JSON file."""
    if not os.path.isfile(METRICS_FILE):
        print("Metrics file not found. Generating sample data...")
        return generate_sample_data()
    with open(METRICS_FILE, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _save_metrics(data: dict) -> None:
    """Persist metrics to JSON file."""
    with open(METRICS_FILE, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Sample data generator (30 days with realistic growth)
# ---------------------------------------------------------------------------

def generate_sample_data() -> dict:
    """
    Create 30 days of sample ad metrics simulating a growing bookstore.
    Early days have lower spend/performance; later days show growth.
    """
    data = {
        "created_at": datetime.now().isoformat(),
        "daily_metrics": [],
    }

    today = datetime.now().date()

    for day_offset in range(29, -1, -1):
        date = today - timedelta(days=day_offset)
        progress = 1 - (day_offset / 30)  # 0.0 -> 1.0 over 30 days

        # Daily spend: grows from ~300 to ~800 with some noise
        base_spend = 300 + progress * 500
        spend = round(base_spend * random.uniform(0.85, 1.15), 2)

        # Impressions: improves with spend and time (learning phase)
        cpm = random.uniform(35, 60)  # Cost per 1000 impressions
        impressions = int((spend / cpm) * 1000)

        # CTR: starts around 0.8%, improves to ~2% as ads optimize
        base_ctr = 0.8 + progress * 1.2
        ctr = round(base_ctr * random.uniform(0.8, 1.2), 2)
        ctr = max(0.3, min(ctr, 3.5))  # clamp

        clicks = max(1, int(impressions * ctr / 100))

        # Conversion rate: 2-5% of clicks convert
        conv_rate = (2.0 + progress * 3.0) * random.uniform(0.7, 1.3) / 100
        conversions = max(0, int(clicks * conv_rate))

        # Average order value: Rs.120-200
        aov = random.uniform(120, 200)
        revenue = round(conversions * aov, 2)

        # Derived metrics
        roas = round(revenue / spend, 2) if spend > 0 else 0
        cpa = round(spend / conversions, 2) if conversions > 0 else 0

        # Introduce some "bad" days for alerting demo
        if day_offset in (5, 12, 20):
            # Low ROAS day
            revenue = round(spend * random.uniform(1.0, 1.8), 2)
            roas = round(revenue / spend, 2)
            conversions = max(1, int(conversions * 0.4))
            cpa = round(spend / conversions, 2)
        if day_offset in (3, 15):
            # Low CTR day
            ctr = round(random.uniform(0.5, 0.9), 2)
            clicks = max(1, int(impressions * ctr / 100))

        entry = {
            "date": date.isoformat(),
            "spend": spend,
            "impressions": impressions,
            "clicks": clicks,
            "ctr": ctr,
            "conversions": conversions,
            "revenue": revenue,
            "roas": roas,
            "cpa": cpa,
        }
        data["daily_metrics"].append(entry)

    _save_metrics(data)
    print(f"Generated 30 days of sample data -> {METRICS_FILE}")
    return data


# ---------------------------------------------------------------------------
# Core functions
# ---------------------------------------------------------------------------

def log_daily_metrics(
    date: str,
    spend: float,
    impressions: int,
    clicks: int,
    conversions: int,
    revenue: float,
) -> dict:
    """
    Log a day's ad performance metrics. Computes derived fields automatically.

    Args:
        date:        YYYY-MM-DD
        spend:       Total ad spend in INR
        impressions: Total impressions
        clicks:      Total clicks
        conversions: Total conversions (orders)
        revenue:     Total revenue from ad-driven orders in INR

    Returns:
        The logged entry dict.
    """
    data = _load_metrics()

    ctr = round((clicks / impressions * 100), 2) if impressions > 0 else 0
    roas = round(revenue / spend, 2) if spend > 0 else 0
    cpa = round(spend / conversions, 2) if conversions > 0 else 0

    entry = {
        "date": date,
        "spend": round(spend, 2),
        "impressions": impressions,
        "clicks": clicks,
        "ctr": ctr,
        "conversions": conversions,
        "revenue": round(revenue, 2),
        "roas": roas,
        "cpa": cpa,
    }

    # Replace if date already exists, otherwise append
    existing_dates = {m["date"] for m in data["daily_metrics"]}
    if date in existing_dates:
        data["daily_metrics"] = [
            entry if m["date"] == date else m
            for m in data["daily_metrics"]
        ]
        print(f"Updated metrics for {date}")
    else:
        data["daily_metrics"].append(entry)
        data["daily_metrics"].sort(key=lambda x: x["date"])
        print(f"Logged metrics for {date}")

    _save_metrics(data)
    return entry


def _summarize(entries: list[dict], label: str) -> dict:
    """Compute aggregate metrics over a list of daily entries."""
    if not entries:
        return {"label": label, "days": 0}

    total_spend = sum(e["spend"] for e in entries)
    total_impressions = sum(e["impressions"] for e in entries)
    total_clicks = sum(e["clicks"] for e in entries)
    total_conversions = sum(e["conversions"] for e in entries)
    total_revenue = sum(e["revenue"] for e in entries)

    return {
        "label": label,
        "days": len(entries),
        "total_spend": round(total_spend, 2),
        "total_impressions": total_impressions,
        "total_clicks": total_clicks,
        "avg_ctr": round((total_clicks / total_impressions * 100), 2) if total_impressions > 0 else 0,
        "total_conversions": total_conversions,
        "total_revenue": round(total_revenue, 2),
        "roas": round(total_revenue / total_spend, 2) if total_spend > 0 else 0,
        "avg_cpa": round(total_spend / total_conversions, 2) if total_conversions > 0 else 0,
        "avg_daily_spend": round(total_spend / len(entries), 2),
        "avg_daily_revenue": round(total_revenue / len(entries), 2),
    }


def calculate_weekly_summary() -> dict:
    """Summarize the last 7 days of ad performance."""
    data = _load_metrics()
    cutoff = (datetime.now().date() - timedelta(days=7)).isoformat()
    recent = [e for e in data["daily_metrics"] if e["date"] > cutoff]
    return _summarize(recent, "Last 7 Days")


def calculate_monthly_summary() -> dict:
    """Summarize the last 30 days of ad performance."""
    data = _load_metrics()
    cutoff = (datetime.now().date() - timedelta(days=30)).isoformat()
    recent = [e for e in data["daily_metrics"] if e["date"] > cutoff]
    return _summarize(recent, "Last 30 Days")


def check_alerts() -> list[dict]:
    """
    Scan the most recent 3 days for threshold violations.
    Returns a list of alert dicts.
    """
    data = _load_metrics()
    recent = data["daily_metrics"][-3:]  # last 3 days
    alerts = []

    for entry in recent:
        date = entry["date"]

        if entry["roas"] < MIN_ROAS and entry["roas"] > 0:
            alerts.append({
                "type": "LOW_ROAS",
                "date": date,
                "value": entry["roas"],
                "threshold": MIN_ROAS,
                "message": f"ROAS dropped to {entry['roas']}x (threshold: {MIN_ROAS}x)",
            })

        if entry["cpa"] > MAX_CPA and entry["conversions"] > 0:
            alerts.append({
                "type": "HIGH_CPA",
                "date": date,
                "value": entry["cpa"],
                "threshold": MAX_CPA,
                "message": f"CPA exceeded threshold: Rs.{entry['cpa']} (max: Rs.{MAX_CPA})",
            })

        if entry["ctr"] < MIN_CTR:
            alerts.append({
                "type": "LOW_CTR",
                "date": date,
                "value": entry["ctr"],
                "threshold": MIN_CTR,
                "message": f"CTR dropped to {entry['ctr']}% (threshold: {MIN_CTR}%)",
            })

    # Persist alerts
    alert_data = {
        "generated_at": datetime.now().isoformat(),
        "alerts": alerts,
    }
    with open(AD_ALERTS_FILE, "w", encoding="utf-8") as fh:
        json.dump(alert_data, fh, indent=2, ensure_ascii=False)

    return alerts


# ---------------------------------------------------------------------------
# Console report
# ---------------------------------------------------------------------------

def print_report():
    """Print a comprehensive ad performance report."""
    data = _load_metrics()
    today = datetime.now().strftime("%Y-%m-%d %H:%M")

    print("=" * 78)
    print(f"  AD PERFORMANCE DASHBOARD  –  {today}")
    print("=" * 78)

    # --- Last 7 days daily breakdown ---
    print(f"\n{'DATE':<12} {'SPEND':>8} {'IMPR':>8} {'CLICKS':>7} {'CTR':>6} {'CONV':>5} {'REV':>9} {'ROAS':>6} {'CPA':>8}")
    print("-" * 78)

    last_7 = data["daily_metrics"][-7:]
    for e in last_7:
        flag = ""
        if e["roas"] < MIN_ROAS and e["roas"] > 0:
            flag += " [!ROAS]"
        if e["cpa"] > MAX_CPA and e["conversions"] > 0:
            flag += " [!CPA]"
        if e["ctr"] < MIN_CTR:
            flag += " [!CTR]"

        print(
            f"{e['date']:<12} "
            f"Rs.{e['spend']:>6.0f} "
            f"{e['impressions']:>8,} "
            f"{e['clicks']:>7,} "
            f"{e['ctr']:>5.1f}% "
            f"{e['conversions']:>5} "
            f"Rs.{e['revenue']:>7.0f} "
            f"{e['roas']:>5.1f}x "
            f"Rs.{e['cpa']:>6.0f}"
            f"{flag}"
        )

    # --- Weekly summary ---
    weekly = calculate_weekly_summary()
    print(f"\n{'─' * 78}")
    print(f"  WEEKLY SUMMARY ({weekly['label']})")
    print(f"{'─' * 78}")
    if weekly["days"] > 0:
        print(f"  Total Spend:      Rs.{weekly['total_spend']:,.0f}")
        print(f"  Total Revenue:    Rs.{weekly['total_revenue']:,.0f}")
        print(f"  ROAS:             {weekly['roas']}x")
        print(f"  Avg CPA:          Rs.{weekly['avg_cpa']:,.0f}")
        print(f"  Avg CTR:          {weekly['avg_ctr']}%")
        print(f"  Total Conversions:{weekly['total_conversions']}")
        print(f"  Avg Daily Spend:  Rs.{weekly['avg_daily_spend']:,.0f}")

    # --- Monthly summary ---
    monthly = calculate_monthly_summary()
    print(f"\n{'─' * 78}")
    print(f"  MONTHLY SUMMARY ({monthly['label']})")
    print(f"{'─' * 78}")
    if monthly["days"] > 0:
        print(f"  Total Spend:      Rs.{monthly['total_spend']:,.0f}")
        print(f"  Total Revenue:    Rs.{monthly['total_revenue']:,.0f}")
        print(f"  ROAS:             {monthly['roas']}x")
        print(f"  Avg CPA:          Rs.{monthly['avg_cpa']:,.0f}")
        print(f"  Avg CTR:          {monthly['avg_ctr']}%")
        print(f"  Total Conversions:{monthly['total_conversions']}")
        print(f"  Avg Daily Spend:  Rs.{monthly['avg_daily_spend']:,.0f}")
        print(f"  Avg Daily Revenue:Rs.{monthly['avg_daily_revenue']:,.0f}")

    # --- Alerts ---
    alerts = check_alerts()
    if alerts:
        print(f"\n{'─' * 78}")
        print(f"  *** PERFORMANCE ALERTS ({len(alerts)}) ***")
        print(f"{'─' * 78}")
        for a in alerts:
            print(f"  [{a['type']}] {a['date']}: {a['message']}")
    else:
        print(f"\n  All metrics within acceptable thresholds.")

    print(f"\n{'=' * 78}")


# ---------------------------------------------------------------------------
# Interactive log mode
# ---------------------------------------------------------------------------

def interactive_log():
    """Prompt user to enter today's metrics from console."""
    print("--- Log Daily Ad Metrics ---")
    date = input(f"Date (YYYY-MM-DD) [{datetime.now().date().isoformat()}]: ").strip()
    if not date:
        date = datetime.now().date().isoformat()

    try:
        spend = float(input("Total ad spend (INR): "))
        impressions = int(input("Total impressions: "))
        clicks = int(input("Total clicks: "))
        conversions = int(input("Total conversions: "))
        revenue = float(input("Total revenue from ads (INR): "))
    except (ValueError, KeyboardInterrupt):
        print("\nInvalid input. Aborting.")
        return

    entry = log_daily_metrics(date, spend, impressions, clicks, conversions, revenue)
    print(f"\nLogged: {json.dumps(entry, indent=2)}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    if "--init" in sys.argv:
        generate_sample_data()
        return

    if "--log" in sys.argv:
        interactive_log()
        return

    # Ensure data exists
    if not os.path.isfile(METRICS_FILE):
        generate_sample_data()

    print_report()


if __name__ == "__main__":
    main()
