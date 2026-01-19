# Update statistics using static values and some checkout things

import json
from pathlib import Path
from datetime import datetime

def update_section(file_path, marker_name, new_content):
    start_marker = f"<!-- START:{marker_name} -->"
    end_marker = f"<!-- END:{marker_name} -->"

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    start_index = content.find(start_marker)
    end_index = content.find(end_marker)

    if start_index == -1 or end_index == -1:
        raise ValueError(f"Markers for {marker_name} not found.")

    # Keep everything before start, insert new content, keep everything after end
    updated = (
        content[: start_index + len(start_marker)]
        + "\n" + new_content + "\n"
        + content[end_index:]
    )

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(updated)


# Paths
iteration_file = Path("data/iteration.json")
version_file = Path("data/version.txt")


# Read current iteration
with open(iteration_file, "r") as f:
    data = json.load(f)

print(f"Current iteration: {data['iteration']}")

# Update iteration
data["iteration"] += 1

# Write back iteration.json
with open(iteration_file, "w") as f:
    json.dump(data, f, indent=2)

print(f"Updated iteration: {data['iteration']}")

# Create version string: vYYYY.MM.DD.iteration
today = datetime.today()
version_string = f"v{today.year}.{today.month:02d}.{today.day:02d}.{data['iteration']}"

# Write to version.txt
with open(version_file, "w") as f:
    f.write(version_string)

print(f"Created version string: {version_string}")

update_section("README.md", "version", f"Version: {version_string}")
