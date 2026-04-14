# Sources for my Heatmap statistics diary

## Repository Structure
- `/sources/`: Data extraction scripts for each platform.
- `/data/`: Normalized `JSON` or `CSV` files (e.g., `activity_log.json`).
- `/python/`: Core logic for aggregation and stats calculation.
- `/visualize/`: Heatmap generation (SVG) and statistics rendering.
- `/docs/`: Project documentation and architecture logs.

## Data Source Specifications

- diary
- blog
- legacy
- subdomains
- github
- github_websites
- google_sites

### Types

- Obsidian: diary
- Wordpress: blog
- Legacy HTML Website: legacy, subdomains, github_websites, google_sites
- Github commit history: github

### Metrics

- Documents or projects: 143
- Individual pages: 315
- Days documented: 1132 of 18345 (6.17%)
- Total words: 1,432,423
- Total sentences: 3,154
- Total images: 132
- Required total reading time: 15 hours 4 minutes

### Table data

| category        | label       | items | pages | days | words | sentences | images | reading_time |
|-----------------|-------------|------:|------:|-----:|------:|----------:|-------:|:------------:|
| diary           | Diary       |   142 |   142 |   30 | 66756 |       300 |    200 |     4h11     |
| blog            | Blog        |     0 |     0 |    0 |     0 |         0 |      0 |     0h00     |
| legacy          | Legacy      |     0 |     0 |    0 |     0 |         0 |      0 |     0h00     |
| subdomains      | Subdomain   |     0 |     0 |    0 |     0 |         0 |      0 |     0h00     |
| github          | Github      |     0 |     0 |    0 |     0 |         0 |      0 |     0h00     |
| github_websites | GH Website  |     0 |     0 |    0 |     0 |         0 |      0 |     0h00     |
| google_sites    | Google site |     0 |     0 |    0 |     0 |         0 |      0 |     0h00     |
| sum             | Sum         |   142 |   142 |   30 | 66756 |       300 |    200 |     4h11     |

## Local database JSON structure

In the `/data/` folder is the parsed data from the 7 sources inside of `JSON` files.

## Heatmap colors 🟥🟧🟨🟩🟦🟪🟫⬛

1. Obsidian and Quartz **diary** at [diary.saiht.de](https://diary.saiht.de) has 1,023,452 words that would require 13 hours to read. In total some 83 markdown files. 312 of 18,923 days are documented.
   - Diary 🟩: 123 days are documented
   - Blog 🟥: 82 entries
   - Projects 🟪: 15 documented
   - Travel 🟨: 12 countries and 42 days
   - Websites 🟦: 4 major ones and 10 abandoned ones
2. Wordpress **blog** 🟥 at [saiht.de/blog](https://saiht.de/blog) with 104 articles and 42,324 words
3. **Legacy** 🟦 website of saiht.de at [saiht.de/legacy](https://saiht.de/legacy) with 64 pages, 13,124 words
4. Older projects at **subdomains** 🟪, listed at [saiht.de/x](https://saiht.de/x) with 20 subdomains, 35 pages, 1,234 words
5. GitHub projects with **github** 🟧 commits: 170 projects, with the main websites containing 23,234 words
6. Websites to some github projects as **github_websites** 🟧 for 130 projects, containing 14,874 word
7. Additional websites as **google_sites** 🟪 with 14 sites, containing 1,423 words


