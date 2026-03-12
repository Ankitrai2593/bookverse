#!/usr/bin/env python3
"""
Master Runner
-------------
Runs all bookstore automation agents in sequence and produces a combined
daily dashboard report.

Usage:
    python run_all.py                # Run all agents
    python run_all.py --skip-prices  # Skip price scraping (faster for testing)

Schedule via cron (daily at 8 AM):
    0 8 * * * cd "/Users/ankit/Documents/Trading & Finance/bookstore/agents" && python3 run_all.py >> /tmp/bookstore_daily.log 2>&1
"""

import json
import os
import sys
import time
from datetime import datetime

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

# Add agents dir to path so we can import modules
sys.path.insert(0, BASE_DIR)


def separator(title: str) -> None:
    """Print a section separator."""
    print(f"\n{'#' * 78}")
    print(f"#  {title}")
    print(f"{'#' * 78}\n")


def run_agent(name: str, func, skip: bool = False) -> bool:
    """
    Run a single agent function with timing and error handling.
    Returns True on success, False on failure.
    """
    if skip:
        print(f"  [SKIPPED] {name}")
        return True

    start = time.time()
    try:
        func()
        elapsed = time.time() - start
        print(f"\n  [OK] {name} completed in {elapsed:.1f}s")
        return True
    except Exception as exc:
        elapsed = time.time() - start
        print(f"\n  [ERROR] {name} failed after {elapsed:.1f}s: {exc}")
        return False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    skip_prices = "--skip-prices" in sys.argv
    start_time = time.time()
    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    results = {}

    print("=" * 78)
    print(f"  BOOKSTORE DAILY AUTOMATION DASHBOARD")
    print(f"  Run started: {today}")
    print("=" * 78)

    # ------------------------------------------------------------------
    # 1. Inventory Manager
    # ------------------------------------------------------------------
    separator("AGENT 1: INVENTORY MANAGER")
    import inventory_manager
    results["inventory"] = run_agent("Inventory Manager", inventory_manager.print_report)

    # ------------------------------------------------------------------
    # 2. Price Monitor
    # ------------------------------------------------------------------
    separator("AGENT 2: PRICE MONITOR")
    if skip_prices:
        print("  Price monitoring skipped (use without --skip-prices to enable).")
        print("  Scraping takes ~2 min due to polite request delays.")
        results["prices"] = True
    else:
        import price_monitor
        results["prices"] = run_agent("Price Monitor", price_monitor.main)

    # ------------------------------------------------------------------
    # 3. Social Media Bot
    # ------------------------------------------------------------------
    separator("AGENT 3: SOCIAL MEDIA CONTENT BOT")
    import social_media_bot
    results["social"] = run_agent("Social Media Bot", social_media_bot.main)

    # ------------------------------------------------------------------
    # 4. Ad Performance Tracker
    # ------------------------------------------------------------------
    separator("AGENT 4: AD PERFORMANCE TRACKER")
    import ad_performance
    results["ads"] = run_agent("Ad Performance Tracker", ad_performance.print_report)

    # ------------------------------------------------------------------
    # Combined Summary
    # ------------------------------------------------------------------
    elapsed_total = time.time() - start_time

    separator("COMBINED DAILY SUMMARY")

    # Inventory summary
    if os.path.isfile(os.path.join(BASE_DIR, "inventory_alerts.json")):
        with open(os.path.join(BASE_DIR, "inventory_alerts.json")) as f:
            inv_alerts = json.load(f)
        n_inv = len(inv_alerts.get("alerts", []))
        print(f"  Inventory alerts:    {n_inv} low-stock items")
    else:
        print(f"  Inventory alerts:    N/A")

    # Price alerts
    if os.path.isfile(os.path.join(BASE_DIR, "price_alerts.json")):
        with open(os.path.join(BASE_DIR, "price_alerts.json")) as f:
            price_alerts = json.load(f)
        n_price = len(price_alerts) if isinstance(price_alerts, list) else 0
        print(f"  Price alerts:        {n_price} books undercut by competitors")
    else:
        print(f"  Price alerts:        N/A (scraping skipped)")

    # Social media
    if os.path.isfile(os.path.join(BASE_DIR, "content_calendar.json")):
        with open(os.path.join(BASE_DIR, "content_calendar.json")) as f:
            cal = json.load(f)
        n_posts = sum(len(d["posts"]) for d in cal.get("days", []))
        print(f"  Social posts planned:{n_posts} posts for the week")
    else:
        print(f"  Social posts:        N/A")

    # Ad performance
    if os.path.isfile(os.path.join(BASE_DIR, "ad_alerts.json")):
        with open(os.path.join(BASE_DIR, "ad_alerts.json")) as f:
            ad_alerts = json.load(f)
        n_ad = len(ad_alerts.get("alerts", []))
        print(f"  Ad alerts:           {n_ad} performance warnings")
    else:
        print(f"  Ad alerts:           N/A")

    # Agent status
    print(f"\n  Agent Status:")
    for agent, ok in results.items():
        status = "OK" if ok else "FAILED"
        print(f"    {agent:<20} [{status}]")

    print(f"\n  Total runtime: {elapsed_total:.1f}s")
    print("=" * 78)
    print(f"  Next scheduled run: tomorrow at 8:00 AM")
    print("=" * 78)


if __name__ == "__main__":
    main()
