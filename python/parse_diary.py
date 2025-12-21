# Parse the local copies of my diaries and create some statistics from it
# Diary 1: /quartz/content
# Diary 2: /obsidian/saiht
# Diary 3: /data/wp_export.csv
#
# Started: 21.12.2025

import os

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


def main():
    # Replace these with your diary folder paths
    folder1 = r"../../quartz/content"
    folder2 = r"../../obsidian/saiht"

    total1, md1 = count_files_in_folder(folder1)
    total2, md2 = count_files_in_folder(folder2)

    print(f"Folder 1: {folder1}")
    print(f"  Total files: {total1}")
    print(f"  Markdown files: {md1}\n")

    print(f"Folder 2: {folder2}")
    print(f"  Total files: {total2}")
    print(f"  Markdown files: {md2}\n")

    # Optional: combined summary
    print("Combined Summary:")
    print(f"  Total files: {total1 + total2}")
    print(f"  Markdown files: {md1 + md2}")


if __name__ == "__main__":
    main()