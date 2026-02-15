#!/usr/bin/env python3
"""
Fetches software products reaching End-of-Life (EOL) in a user-specified year
from https://endoflife.date and exports the results to a CSV file in ~/eol/
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import requests
except ImportError:
    print("Missing dependency: requests\nInstall with: pip install requests")
    sys.exit(1)


ASCII_BANNER = r"""
   _____                                      
  /     \ ___.__. _____   ____   ____   ____  
 /  \ /  <   |  |/     \ /  _ \ /    \ /  _ \ 
/    Y    \___  |  Y Y  (  <_> )   |  (  <_> )
\____|__  / ____|__|_|  /\____/|___|  /\____/ 
        \/\/          \/            \/        
""".rstrip("\n")

BASE_URL = "https://endoflife.date/api"


def prompt_year() -> str:
    while True:
        year = input("Enter the EOL year to search for (e.g., 2026): ").strip()
        if len(year) == 4 and year.isdigit():
            return year
        print("Please enter a valid 4-digit year (e.g., 2026).")


def get_json(url: str, timeout: int = 30) -> Any:
    resp = requests.get(url, timeout=timeout)
    resp.raise_for_status()
    return resp.json()


def safe_str(value: Any) -> str:
    return "" if value is None else str(value)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch EOL software products for a given year.")
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=Path.home() / "eol",
        help="Output folder for the CSV file (default: ~/eol)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    print(ASCII_BANNER)
    print("\nBy twitter: @Menno_Gijzen_")
    print("===========================================\n")

    target_year = prompt_year()

    output_dir = args.output
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"eol_{target_year}.csv"

    try:
        all_products: List[str] = get_json(f"{BASE_URL}/all.json")
    except requests.RequestException as e:
        print(f"Failed to fetch product list: {e}")
        return 1

    results: List[Dict[str, str]] = []

    for product_name in all_products:
        try:
            product_detail: List[Dict[str, Any]] = get_json(f"{BASE_URL}/{product_name}.json")
        except requests.RequestException:
            print(f"Error fetching details for product: {product_name}")
            continue

        for version in product_detail:
            eol = safe_str(version.get("eol"))
            if target_year in eol:
                results.append(
                    {
                        "Product": product_name,
                        "EOLDate": eol,
                        "Cycle": safe_str(version.get("cycle")),
                    }
                )
                break  # only one hit per product

    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Product", "EOLDate", "Cycle"])
        writer.writeheader()
        writer.writerows(results)

    print(f"\nFound {len(results)} products with an EOL in {target_year}.")
    print(f"Data exported to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
