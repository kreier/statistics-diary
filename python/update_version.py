import json
from pathlib import Path
from datetime import datetime


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
