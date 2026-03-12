#!/usr/bin/env python3
"""
Price Monitor Agent
-------------------
Scrapes competitor bookstores (kitabay.com, bindassbooks.in) to compare
prices against our catalog. Flags undercuts and saves results to CSV.

Usage:
    python price_monitor.py

Schedule daily via cron:
    0 8 * * * cd /path/to/agents && python price_monitor.py
"""

import csv
import json
import os
import re
import time
from datetime import datetime
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BOOKS = [
    "Rich Dad Poor Dad",
    "Atomic Habits",
    "Psychology of Money",
    "Ikigai",
    "Think and Grow Rich",
    "The Alchemist",
    "The Secret",
    "48 Laws of Power",
    "It Ends with Us",
    "The Silent Patient",
    "A Good Girl's Guide to Murder",
    "The Kite Runner",
    "Haunting Adeline",
    "1984",
    "The Housemaid",
    "Before the Coffee Gets Cold",
    "Palace of Illusions",
    "Who Moved My Cheese",
    "Attitude Is Everything",
    "Crime and Punishment",
]

OUR_PRICES = [
    89, 129, 119, 99, 89, 119, 89, 139, 169, 129,
    149, 139, 229, 89, 169, 129, 149, 89, 89, 179,
]

# Map title -> our price for quick lookup
PRICE_MAP = dict(zip(BOOKS, OUR_PRICES))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "price_comparison.csv")
ALERT_FILE = os.path.join(BASE_DIR, "price_alerts.json")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-IN,en;q=0.9",
}

REQUEST_TIMEOUT = 15  # seconds
DELAY_BETWEEN_REQUESTS = 2  # seconds – be polite to servers


# ---------------------------------------------------------------------------
# Scraping helpers
# ---------------------------------------------------------------------------

def _extract_price_from_text(text: str) -> float | None:
    """Pull the first number that looks like an INR price from a string."""
    if not text:
        return None
    # Match patterns like ₹89, Rs.89, Rs 89, 89.00, etc.
    match = re.search(r'[₹]?\s*(\d[\d,]*\.?\d*)', text.replace(",", ""))
    if match:
        try:
            return float(match.group(1))
        except ValueError:
            return None
    return None


def scrape_kitabay(title: str) -> float | None:
    """
    Search kitabay.com for a book title and return the lowest listed price.
    Returns None if the book is not found or scraping fails.
    """
    try:
        search_url = f"https://kitabay.com/search?q={quote_plus(title)}"
        resp = requests.get(search_url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "lxml")

        # Kitabay uses Shopify-style product cards.
        # Look for sale-price / price elements in product grid.
        prices = []

        # Strategy 1: look for <span class="price"> or similar
        for tag in soup.select(".price, .product-price, .price--sale, [class*='price']"):
            p = _extract_price_from_text(tag.get_text())
            if p and 10 < p < 5000:  # sanity range for a book
                prices.append(p)

        # Strategy 2: scan all text containing ₹ or Rs
        if not prices:
            for tag in soup.find_all(string=re.compile(r'[₹]|Rs\.?')):
                p = _extract_price_from_text(tag)
                if p and 10 < p < 5000:
                    prices.append(p)

        return min(prices) if prices else None

    except Exception as exc:
        print(f"  [kitabay] Error searching '{title}': {exc}")
        return None


def scrape_bindassbooks(title: str) -> float | None:
    """
    Search bindassbooks.in for a book title and return the lowest listed price.
    Returns None if the book is not found or scraping fails.
    """
    try:
        search_url = f"https://bindassbooks.in/search?q={quote_plus(title)}"
        resp = requests.get(search_url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "lxml")

        prices = []

        # Similar Shopify structure
        for tag in soup.select(".price, .product-price, .price--sale, [class*='price']"):
            p = _extract_price_from_text(tag.get_text())
            if p and 10 < p < 5000:
                prices.append(p)

        if not prices:
            for tag in soup.find_all(string=re.compile(r'[₹]|Rs\.?')):
                p = _extract_price_from_text(tag)
                if p and 10 < p < 5000:
                    prices.append(p)

        return min(prices) if prices else None

    except Exception as exc:
        print(f"  [bindass] Error searching '{title}': {exc}")
        return None


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

def monitor_prices() -> list[dict]:
    """Scrape both competitors for every book and return comparison rows."""
    today = datetime.now().strftime("%Y-%m-%d")
    results = []
    alerts = []

    print("=" * 72)
    print(f"  PRICE MONITOR REPORT  –  {today}")
    print("=" * 72)
    print(f"{'Book':<35} {'Ours':>6} {'Kitabay':>8} {'Bindass':>8} {'Alert':>6}")
    print("-" * 72)

    for title in BOOKS:
        our_price = PRICE_MAP[title]

        kitabay_price = scrape_kitabay(title)
        time.sleep(DELAY_BETWEEN_REQUESTS)

        bindass_price = scrape_bindassbooks(title)
        time.sleep(DELAY_BETWEEN_REQUESTS)

        # Compute cheapest competitor price
        competitor_prices = [p for p in [kitabay_price, bindass_price] if p is not None]
        min_competitor = min(competitor_prices) if competitor_prices else None
        diff = (our_price - min_competitor) if min_competitor else None

        flagged = diff is not None and diff > 0  # competitor is cheaper

        row = {
            "book_title": title,
            "our_price": our_price,
            "kitabay_price": kitabay_price,
            "bindass_price": bindass_price,
            "price_diff": diff,
            "date": today,
        }
        results.append(row)

        if flagged:
            alerts.append({
                "book": title,
                "our_price": our_price,
                "cheapest_competitor": min_competitor,
                "diff": diff,
                "date": today,
            })

        # Console line
        kb_str = f"₹{kitabay_price:.0f}" if kitabay_price else "N/A"
        bb_str = f"₹{bindass_price:.0f}" if bindass_price else "N/A"
        flag_str = " ⚠ YES" if flagged else ""
        print(f"{title:<35} ₹{our_price:>4}  {kb_str:>8} {bb_str:>8} {flag_str}")

    print("-" * 72)
    print(f"Total books monitored: {len(results)}")
    print(f"Price alerts (competitor cheaper): {len(alerts)}")
    print("=" * 72)

    return results, alerts


def save_csv(results: list[dict]) -> None:
    """Append today's results to the CSV file."""
    file_exists = os.path.isfile(CSV_FILE)
    fieldnames = [
        "book_title", "our_price", "kitabay_price",
        "bindass_price", "price_diff", "date",
    ]
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerows(results)
    print(f"\nResults saved to {CSV_FILE}")


def save_alerts(alerts: list[dict]) -> None:
    """Save price-drop alerts to JSON (overwrite daily)."""
    with open(ALERT_FILE, "w", encoding="utf-8") as fh:
        json.dump(alerts, fh, indent=2, ensure_ascii=False)
    if alerts:
        print(f"Price alerts saved to {ALERT_FILE}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    results, alerts = monitor_prices()
    save_csv(results)
    save_alerts(alerts)

    if alerts:
        print("\n*** ATTENTION: The following books are cheaper at competitors ***")
        for a in alerts:
            print(f"  - {a['book']}: Ours ₹{a['our_price']} vs ₹{a['cheapest_competitor']} (diff ₹{a['diff']})")


if __name__ == "__main__":
    main()
