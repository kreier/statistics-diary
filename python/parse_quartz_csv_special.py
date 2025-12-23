# Parse the local copies of my diaries and create some statistics from it
# Diary 1: ../../quartz/content
#
# Started: 23.12.2025

import os
import re
import csv
from datetime import datetime, timedelta

# Regex to match bold dates (special cases)
bold_date_pattern = re.compile(r'^\*\*(\d{2}\.\d{2}\.\d{4})(.*)')

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
    """Check one year's markdown file for missing dates, bold counts, and special subheading stats."""
    file_path = os.path.join(folder, f"{year}.md")
    if not os.path.exists(file_path):
        print(f"⚠️ File for year {year} not found: {file_path}")
        return None

    found_dates = set()
    bold_count = 0
    special_dates = []  # list of dicts {date, word_count, text}
    special_count = 0

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        bold_match = bold_date_pattern.match(line)
        if bold_match:
            date_str = bold_match.group(1)
            found_dates.add(date_str)
            bold_count += 1

            # Check if previous line is a subheading ###
            if i > 0 and lines[i-1].strip().startswith("###"):
                special_count += 1
                # Text after the date in the same line
                text_after_date = bold_match.group(2).strip()
                word_count = len(text_after_date.split()) if text_after_date else 0

                special_dates.append({
                    "date": date_str,
                    "word_count": word_count,
                    "text": text_after_date
                })

        else:
            # Also catch non-bold dates for completeness
            date_match = re.match(r'^(\d{2}\.\d{2}\.\d{4})', line)
            if date_match:
                date_str = date_match.group(1)
                found_dates.add(date_str)

        i += 1

    all_dates = set(generate_all_dates(year))
    missing_dates = sorted(all_dates - found_dates)

    return {
        "year": year,
        "total_expected": len(all_dates),
        "found": len(found_dates),
        "missing_count": len(missing_dates),
        "missing_dates": missing_dates,
        "bold_count": bold_count,
        "special_count": special_count,
        "special_dates": special_dates,
    }

def main():
    # Folder containing the markdown files
    folder = os.path.join("..", "..", "quartz", "content", "Diary")

    # Years to check
    years = [1975, 1976, 2021, 2022, 2023, 2024, 2025]

    results = {}
    all_specials = []  # collect all special cases across years

    for year in years:
        info = check_year_file(folder, year)
        if info:
            results[year] = info
            for sd in info["special_dates"]:
                all_specials.append({
                    "year": year,
                    "date": sd["date"],
                    "word_count": sd["word_count"],
                    "text": sd["text"]
                })

    # Print summary
    for year, info in results.items():
        print(f"\nYear {year}:")
        print(f"  Expected dates: {info['total_expected']}")
        print(f"  Found dates: {info['found']}")
        print(f"  Missing dates: {info['missing_count']}")
        print(f"  Bold dates: {info['bold_count']}")
        print(f"  Special dates (bold + ### above): {info['special_count']}")
        if info['missing_count'] > 0:
            print(f"  Missing list (first 10 shown): {info['missing_dates'][:10]}")
        if info['special_count'] > 0:
            print("  Special dates list (date + word count):")
            for sd in info['special_dates'][:5]:  # show first 5
                print(f"    {sd['date']} → {sd['word_count']} words")

    # Export summary to diary_results.csv
    csv_file = "diary_results.csv"
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Year", "Expected Dates", "Found Dates", "Missing Count",
            "Bold Count", "Special Count", "Missing Dates"
        ])
        for year, info in results.items():
            writer.writerow([
                year,
                info["total_expected"],
                info["found"],
                info["missing_count"],
                info["bold_count"],
                info["special_count"],
                ";".join(info["missing_dates"])
            ])

    print(f"\n✅ Results exported to {csv_file}")

    # Export all special cases to special.csv
    special_file = "special.csv"
    with open(special_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Year", "Date", "Word Count", "Text After Date"])
        for sd in all_specials:
            writer.writerow([sd["year"], sd["date"], sd["word_count"], sd["text"]])

    print(f"✅ Special cases exported to {special_file}")

if __name__ == "__main__":
    main()
