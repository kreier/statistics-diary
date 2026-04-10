# AGENTS.md

## Project Context
**Project:** Statistics for my Diary, Blog and Projects
**Description:** A tool to aggregate, normalize, and visualize personal activity data from GitHub, WordPress, Obsidian, and legacy HTML archives into a unified timeline and heatmap.

## Agent Directives
When working on this repository, Jules should adhere to the following principles:
1. **Modularity:** Keep data extraction logic (sources) strictly separated from processing and visualization logic.
2. **Idempotency:** Scripts must be able to run multiple times without creating duplicate entries in the database/JSON files.
3. **Privacy:** Never include raw content from Obsidian or WordPress stories in the output; extract only metadata (timestamps, word counts, or category tags).

## Repository Structure
- `/sources/`: Data extraction scripts for each platform.
- `/data/`: Normalized `JSON` or `CSV` files (e.g., `activity_log.json`).
- `/python/`: Core logic for aggregation and stats calculation.
- `/visualize/`: Heatmap generation (SVG) and statistics rendering.
- `/docs/`: Project documentation and architecture logs.

## Data Source Specifications

### 1. GitHub Commits
- **Target:** `https://github.com/kreier/`
- **Method:** Use Git history or GitHub API.
- **Data Points:** Timestamp, repository name, and commit hash.

### 2. WordPress Stories
- **Method:** Parse the WordPress XML export or use the REST API.
- **Data Points:** Publish date, slug, and word count.

### 3. Obsidian Entries
- **Method:** Local Markdown file parsing.
- **Strategy:** Look for YAML frontmatter (e.g., `date: YYYY-MM-DD`) or file creation time if frontmatter is missing.
- **Filter:** Only process files within specified "Daily" or "Journal" folders.

### 4. Legacy HTML
- **Method:** `BeautifulSoup` or regex parsing of local `.html` files in the legacy directory.
- **Pattern:** Identify date patterns in `<time>` tags or specific header classes.

## Technical Standards
- **Language:** Python 3.10+
- **Date Format:** All internal dates must be normalized to ISO 8601 (`YYYY-MM-DDTHH:MM:SSZ`).
- **Dependencies:** Minimize external libraries. Prefer `pandas` for data manipulation and `matplotlib` or raw `SVG` generation for heatmaps.
- **Error Handling:** Log failures for specific entries but continue processing the rest of the batch.

## Common Agent Tasks
- "Jules, add a new source parser for the legacy HTML files in `/sources/legacy/`."
- "Jules, regenerate the `activity_log.json` by scanning all sources."
- "Jules, update the heatmap script to support a 'yearly' view."

---
*Note: This file is the primary source of truth for repository architecture. Update this file whenever the data schema changes.*
