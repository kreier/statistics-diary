# Parse the local copies of my diaries and create some statistics from it
# Diary 1: ../../quartz/content
#
# Started: 23.12.2025

import os
import re
from datetime import datetime, timedelta

# Regex to match dates (with optional bold **)
date_pattern = re.compile(r'^\**(\d{2}\.\d{2}\.\d{4})')

def generate_all_dates(year):
    """Generate all dates for a given year in DD.MM.YYYY format."""
    start = datetime(year, 1, 1)
    end = datetime(year, 12, 31)
    delta = timedelta(days=1)
    dates = []
    while start <= end:
        dates.append(start.strftime("%d.%m.%Y"))
        start += delta
    return dates

def check_year_file(folder, year):
    """Check one year's markdown file for missing dates and bold counts."""
    file_path = os.path.join(folder, f"{year}.md")
    if not os.path.exists(file_path):
        print(f"⚠️ File for year {year} not found: {file_path}")
        return None

    found_dates = set()
    bold_count = 0

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            match = date_pattern.match(line.strip())
            if match:
                date_str = match.group(1)
                found_dates.add(date_str)
                if line.strip().startswith("**"):
                    bold_count += 1

    all_dates = set(generate_all_dates(year))
    missing_dates = sorted(all_dates - found_dates)

    return {
        "year": year,
        "total_expected": len(all_dates),
        "found": len(found_dates),
        "missing_count": len(missing_dates),
        "missing_dates": missing_dates,
        "bold_count": bold_count,
    }

def main():
    # Folder containing the markdown files
    folder = os.path.join("..", "..", "quartz", "content", "Diary")

    # Years to check
    years = [1975, 1976, 2021, 2022, 2023, 2024, 2025]

    results = {}
    for year in years:
        info = check_year_file(folder, year)
        if info:
            results[year] = info

    # Print summary
    for year, info in results.items():
        print(f"\nYear {year}:")
        print(f"  Expected dates: {info['total_expected']}")
        print(f"  Found dates: {info['found']}")
        print(f"  Missing dates: {info['missing_count']}")
        print(f"  Bold dates: {info['bold_count']}")
        if info['missing_count'] > 0:
            print(f"  Missing list (first 10 shown): {info['missing_dates'][:10]}")

if __name__ == "__main__":
    main()
