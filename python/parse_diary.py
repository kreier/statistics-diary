# Parse the local copies of my diaries and create some statistics from it
# Diary 1: /quartz/content
# Diary 2: /obsidian/saiht
# Diary 3: /data/wp_data.csv
#
# Started: 21.12.2025

import os
import re
import pandas as pd
import requests


def count_files_in_folder(folder_path):
    """
    Count total files and markdown files in a given folder.
    """
    total_files = 0
    markdown_files = 0

    # Walk through the folder
    for root, _, files in os.walk(folder_path):
        for file in files:
            total_files += 1
            if file.lower().endswith(".md"):
                markdown_files += 1

    return total_files, markdown_files


def download_csv_from_wordpress(url, save_path="../data/wp_data.csv"):
    """
    Download a CSV file from a WordPress installation and save it locally.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise error if download fails

        # Ensure target directory exists
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        with open(save_path, "wb") as f:
            f.write(response.content)

        print(f"CSV downloaded successfully to {save_path}")
    except Exception as e:
        print(f"Failed to download CSV: {e}")


def analyze_csv(csv_path="../data/wp_data.csv"):
    """
    Analyze the CSV file:
    - Count how many entries (rows) it has
    - Find oldest and newest entry in the 'Date' column
    - Compute total word count in the 'Content' column (cleaned of WP block tags, HTML, and URLs)
    - Print each cleaned line of Content
    """
    if not os.path.exists(csv_path):
        print(f"CSV file not found at {csv_path}")
        return 0, None, None, 0

    # Read CSV
    df = pd.read_csv(csv_path)

    # Count rows (entries)
    entry_count = len(df)

    # Handle Date column
    oldest_date, newest_date = None, None
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        valid_dates = df["Date"].dropna()
        if not valid_dates.empty:
            oldest_date = valid_dates.min()
            newest_date = valid_dates.max()

    # Handle Content column word count + cleaning
    total_word_count = 0
    if "Content" in df.columns:
        def clean_text(text):
            text = str(text)
            # Remove Gutenberg block comments like <!-- wp:paragraph --> or <!-- /wp:image -->
            text = re.sub(r"<!--.*?-->", " ", text)
            # Remove HTML tags
            text = re.sub(r"<[^>]+>", " ", text)
            # Remove URLs (http/https)
            text = re.sub(r"https?://\S+", " ", text)
            # Collapse whitespace
            text = re.sub(r"\s+", " ", text).strip()
            return text

        cleaned = df["Content"].dropna().astype(str).apply(clean_text)

        # Print each cleaned line
        # print("\n--- Cleaned Content Entries ---")
        # for i, line in enumerate(cleaned, start=1):
        #     print(f"Entry {i}: {line}")

        # Word count
        total_word_count = cleaned.apply(lambda x: len(x.split())).sum()

    return entry_count, oldest_date, newest_date, total_word_count



def main():
    # The two locations of my diaries
    diary1 = r"../../quartz/content"
    diary2 = r"../../obsidian/saiht"

    total1, md1 = count_files_in_folder(diary1)
    total2, md2 = count_files_in_folder(diary2)

    print(f"Diary 1: {diary1}")
    print(f"  Total files: {total1}")
    print(f"  Markdown files: {md1}\n")

    print(f"Diary 2: {diary2}")
    print(f"  Total files: {total2}")
    print(f"  Markdown files: {md2}\n")

    # Optional: combined summary
    print("Combined Summary:")
    print(f"  Total files: {total1 + total2}")
    print(f"  Markdown files: {md1 + md2}")

    # Predefined WordPress CSV URL
    wp_csv_url = "https://saiht.de/blog/wp-load.php?security_token=a940e55d19492822&export_id=5&action=get_data"
    # download_csv_from_wordpress(wp_csv_url)

    # Count CSV entries
    entries, oldest, newest, word_count = analyze_csv()

    print(f"wp_data.csv has {entries} entries")
    if oldest and newest:
        print(f"Oldest entry date: {oldest}")
        print(f"Newest entry date: {newest}")
    print(f"Total word count in 'Content' column: {word_count}")


if __name__ == "__main__":
    main()