#!/usr/bin/env python3
"""
Inventory Manager Agent
-----------------------
Tracks stock levels for 20 books and 5 bundles using a local JSON database.
Generates low-stock alerts and reorder lists.

Usage:
    python inventory_manager.py              # Run full check + report
    python inventory_manager.py --init       # Re-initialize inventory
"""

import json
import os
import sys
from datetime import datetime

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

BUNDLES = [
    "Self-Help Starter Pack (Rich Dad + Atomic Habits + Ikigai)",
    "Thriller Bundle (Silent Patient + Housemaid + Good Girl's Guide)",
    "Classic Literature Set (1984 + Alchemist + Kite Runner)",
    "Mindset Collection (Psychology of Money + Think & Grow Rich + Attitude)",
    "Bestseller Box (It Ends with Us + Haunting Adeline + Before Coffee)",
]

LOW_STOCK_THRESHOLD = 5
INITIAL_STOCK = 25
REORDER_QUANTITY_MULTIPLIER = 3  # reorder = threshold * multiplier

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INVENTORY_FILE = os.path.join(BASE_DIR, "inventory.json")
ALERTS_FILE = os.path.join(BASE_DIR, "inventory_alerts.json")


# ---------------------------------------------------------------------------
# Database helpers
# ---------------------------------------------------------------------------

def _load_inventory() -> dict:
    """Load inventory from JSON file."""
    if not os.path.isfile(INVENTORY_FILE):
        print("Inventory file not found. Initializing fresh inventory...")
        return initialize_inventory()
    with open(INVENTORY_FILE, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _save_inventory(data: dict) -> None:
    """Persist inventory to JSON file."""
    with open(INVENTORY_FILE, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)


def initialize_inventory() -> dict:
    """Create the inventory file with default stock levels."""
    data = {
        "last_updated": datetime.now().isoformat(),
        "items": {},
        "transactions": [],
    }

    # Books
    for book in BOOKS:
        data["items"][book] = {
            "type": "book",
            "stock": INITIAL_STOCK,
            "total_sold": 0,
            "low_stock_threshold": LOW_STOCK_THRESHOLD,
        }

    # Bundles (start with 10 each)
    for bundle in BUNDLES:
        data["items"][bundle] = {
            "type": "bundle",
            "stock": 10,
            "total_sold": 0,
            "low_stock_threshold": LOW_STOCK_THRESHOLD,
        }

    _save_inventory(data)
    print(f"Inventory initialized: {len(BOOKS)} books, {len(BUNDLES)} bundles")
    print(f"Saved to {INVENTORY_FILE}")
    return data


# ---------------------------------------------------------------------------
# Core functions
# ---------------------------------------------------------------------------

def add_stock(item_name: str, quantity: int) -> bool:
    """
    Add stock for an item. Returns True on success.

    Args:
        item_name: Exact name of book or bundle.
        quantity:  Number of units to add (must be positive).
    """
    if quantity <= 0:
        print(f"Error: quantity must be positive, got {quantity}")
        return False

    data = _load_inventory()

    if item_name not in data["items"]:
        print(f"Error: '{item_name}' not found in inventory.")
        return False

    data["items"][item_name]["stock"] += quantity
    data["last_updated"] = datetime.now().isoformat()
    data["transactions"].append({
        "action": "add_stock",
        "item": item_name,
        "quantity": quantity,
        "timestamp": datetime.now().isoformat(),
    })

    _save_inventory(data)
    new_stock = data["items"][item_name]["stock"]
    print(f"Added {quantity} units of '{item_name}'. New stock: {new_stock}")
    return True


def sell_item(item_name: str, quantity: int = 1) -> bool:
    """
    Record a sale. Reduces stock and increments total_sold.

    Args:
        item_name: Exact name of book or bundle.
        quantity:  Number of units sold (default 1).
    """
    if quantity <= 0:
        print(f"Error: quantity must be positive, got {quantity}")
        return False

    data = _load_inventory()

    if item_name not in data["items"]:
        print(f"Error: '{item_name}' not found in inventory.")
        return False

    current = data["items"][item_name]["stock"]
    if current < quantity:
        print(f"Error: Insufficient stock for '{item_name}'. Available: {current}, requested: {quantity}")
        return False

    data["items"][item_name]["stock"] -= quantity
    data["items"][item_name]["total_sold"] += quantity
    data["last_updated"] = datetime.now().isoformat()
    data["transactions"].append({
        "action": "sell",
        "item": item_name,
        "quantity": quantity,
        "timestamp": datetime.now().isoformat(),
    })

    _save_inventory(data)
    remaining = data["items"][item_name]["stock"]
    print(f"Sold {quantity}x '{item_name}'. Remaining stock: {remaining}")

    # Check if we just went below threshold
    if remaining <= LOW_STOCK_THRESHOLD:
        print(f"  *** LOW STOCK ALERT: '{item_name}' is at {remaining} units! ***")

    return True


def check_low_stock() -> list[dict]:
    """
    Return list of items at or below the low-stock threshold.
    Each entry has: name, type, stock, threshold.
    """
    data = _load_inventory()
    low = []
    for name, info in data["items"].items():
        if info["stock"] <= info["low_stock_threshold"]:
            low.append({
                "name": name,
                "type": info["type"],
                "stock": info["stock"],
                "threshold": info["low_stock_threshold"],
            })
    return low


def generate_reorder_list() -> list[dict]:
    """
    Build a reorder list for all low-stock items.
    Reorder quantity brings stock up to threshold * REORDER_QUANTITY_MULTIPLIER.
    """
    low_items = check_low_stock()
    reorder = []
    for item in low_items:
        target = item["threshold"] * REORDER_QUANTITY_MULTIPLIER
        qty_needed = max(target - item["stock"], 0)
        if qty_needed > 0:
            reorder.append({
                "name": item["name"],
                "type": item["type"],
                "current_stock": item["stock"],
                "reorder_quantity": qty_needed,
                "target_stock": target,
            })
    return reorder


def save_alerts(low_items: list[dict]) -> None:
    """Persist low-stock alerts to JSON."""
    alert_data = {
        "generated_at": datetime.now().isoformat(),
        "threshold": LOW_STOCK_THRESHOLD,
        "alerts": low_items,
    }
    with open(ALERTS_FILE, "w", encoding="utf-8") as fh:
        json.dump(alert_data, fh, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def print_report():
    """Print a formatted inventory report to console."""
    data = _load_inventory()
    today = datetime.now().strftime("%Y-%m-%d %H:%M")

    print("=" * 68)
    print(f"  INVENTORY REPORT  –  {today}")
    print("=" * 68)

    # Books section
    print(f"\n{'BOOKS':<40} {'Stock':>6} {'Sold':>6} {'Status':>10}")
    print("-" * 68)
    for book in BOOKS:
        info = data["items"].get(book, {})
        stock = info.get("stock", 0)
        sold = info.get("total_sold", 0)
        status = "LOW" if stock <= LOW_STOCK_THRESHOLD else "OK"
        marker = " ***" if status == "LOW" else ""
        print(f"{book:<40} {stock:>6} {sold:>6} {status:>10}{marker}")

    # Bundles section
    print(f"\n{'BUNDLES':<40} {'Stock':>6} {'Sold':>6} {'Status':>10}")
    print("-" * 68)
    for bundle in BUNDLES:
        info = data["items"].get(bundle, {})
        stock = info.get("stock", 0)
        sold = info.get("total_sold", 0)
        status = "LOW" if stock <= LOW_STOCK_THRESHOLD else "OK"
        marker = " ***" if status == "LOW" else ""
        short_name = bundle[:40]
        print(f"{short_name:<40} {stock:>6} {sold:>6} {status:>10}{marker}")

    # Summary
    total_stock = sum(i["stock"] for i in data["items"].values())
    total_sold = sum(i["total_sold"] for i in data["items"].values())
    low = check_low_stock()

    print(f"\n{'─' * 68}")
    print(f"Total items in stock:  {total_stock}")
    print(f"Total items sold:      {total_sold}")
    print(f"Low-stock alerts:      {len(low)}")

    if low:
        print("\n*** LOW STOCK ITEMS ***")
        for item in low:
            print(f"  - {item['name']}: {item['stock']} units remaining")

    # Reorder list
    reorder = generate_reorder_list()
    if reorder:
        print("\n*** REORDER LIST ***")
        print(f"{'Item':<40} {'Current':>8} {'Order':>8} {'Target':>8}")
        print("-" * 68)
        for r in reorder:
            short_name = r["name"][:40]
            print(f"{short_name:<40} {r['current_stock']:>8} {r['reorder_quantity']:>8} {r['target_stock']:>8}")

    print("=" * 68)

    # Save alerts
    save_alerts(low)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    if "--init" in sys.argv:
        initialize_inventory()
        return

    # Ensure inventory exists
    if not os.path.isfile(INVENTORY_FILE):
        initialize_inventory()

    print_report()


if __name__ == "__main__":
    main()
