# Data structure and Processing pipeline to generate the statistics

## Sources

Currently we have 7 categories of sources:

- diary
- blog
- legacy
- subdomains
- github
- github_websites
- google_sites

### Types of sources

1. Obsidian: diary
2. Wordpress: blog
3. Github commit history: github
4. Legacy HTML Website: legacy, subdomains, github_websites, google_sites

### Metrics for each source

- Documents, items or projects: 143
- Individual pages for each item: 315
- Days documented: 1132 of 18345 (6.17%)
- Total words: 1,432,423
- Total sentences: 3,154
- Total images: 132
- Required total reading time: 15 hours 4 minutes

### Table data

| name                | source_id        | label       |  words | reading_time |
|---------------------|------------------|-------------|-------:|:------------:|
| Diary 🟩             | obsidian-diary   | Diary       |  66756 |     4h27     |
| Obsidian Blog 🟥     | obsidian-blog    | Blog2       |    730 |     0h02     |
| Project 🟪           | obsidian-project | Project     |   1791 |     0h07     |
| Travel 🟨            | obsidian-travel  | Travel      |  48251 |     3h13     |
| Website 🟦           | obsidian-website | Website     |  32307 |     2h09     |
| Wordpress Blog 🟥    | blog             | Blog        |    985 |     0h03     |
| Legacy 🟦            | legacy           | Legacy      |  18017 |     1h12     |
| Subdomain 🟪         | subdomain        | Subdomain   |  12356 |     0h49     |
| Github repository 🟧 | github           | Github      |   1677 |     0h06     |
| Github website 🟧    | github_website   | GH Website  |    715 |     0h02     |
| Google site 🟪       | google_sites     | Google site |   1403 |     0h05     |
| Sum                 | sum              | Sum         | 184988 |     12h19    |


| name                | items | pages | days |  words | sentences | images | reading_time |
|---------------------|------:|------:|-----:|-------:|----------:|:------:|:------------:|
| Diary 🟩             |   142 |   142 |   30 |  66756 |      9537 |    475 |     4h27     |
| Obsidian Blog 🟥     |    38 |    38 |   45 |    730 |       104 |     33 |     0h02     |
| Project 🟪           |    21 |    57 |   29 |   1791 |       256 |     53 |     0h07     |
| Travel 🟨            |    34 |    73 |    9 |  48251 |      6893 |     33 |     3h13     |
| Website 🟦           |     7 |    99 |   22 |  32307 |      4615 |     83 |     2h09     |
| Wordpress Blog 🟥    |    84 |    90 |   18 |    985 |       141 |     70 |     0h03     |
| Legacy 🟦            |   164 |   246 |   80 |  18017 |      2574 |     29 |     1h12     |
| Subdomain 🟪         |    15 |    23 |   23 |  12356 |      1765 |     43 |     0h49     |
| Github repository 🟧 |   150 |   195 |  105 |   1677 |       240 |     94 |     0h06     |
| Github website 🟧    |   134 |   174 |   79 |    715 |       102 |     40 |     0h02     |
| Google site 🟪       |     2 |    58 |   42 |   1403 |       200 |     43 |     0h05     |
| Sum                 |   791 |  1195 |  482 | 184988 |     26427 |    996 |     12h19    |



### Heatmap colors 🟥🟧🟨🟩🟦🟪🟫⬛

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

### Final 11 source IDs

With the 5 subcategories for obsidian the final number of `source_id`'s rises to 11:

- obsidian-diary
- obsidian-blog
- obsidian-project
- obsidian-travel
- obsidian-website
- blog
- legacy
- subdomain
- github
- github-website
- google-site

Now I need a markdown table with name, label, source_id, items, pages, words in the README.md and update it from time to time.

## Processing pipeline

### Core Architecture

```
sources.json  →  Step 1 (discover links)
              →  Step 2 (fetch + parse content)
              →  Step 3 (analyze text)
              →  results + TUI inspection
```

Each step produces **structured intermediate data**.

### Storage Strategy

```
data/
├── step1_links/
│   └── <source_id>.json
│
├── step2_content/
│   └── <source_id>/
│       ├── page1.json
│       ├── page2.json
│
├── step3_analysis/
│   └── <source_id>.json
```

The data files will also include information about "last parsed" to cache heavily and reduce unnecessary fetching.

## TUI to manage sources

The sources should be managed by a TUI (textual user interface) written in python with `textual`.

### Architecture

```
project/
│
├── tui/
│   ├── app.py              # textual app
│   ├── views/
│   │   ├── source_list.py
│   │   ├── preview.py
│   │   └── actions.py
│
├── sources/
│   ├── github.py
│   ├── wordpress.py
│   ├── website.py
│
├── core/
│   ├── parser.py
│   ├── executor.py
│
├── config/
│   └── sources.yaml
│
└── main.py
```

### 🎮 UX Ideas
- Arrow keys → navigate sources
- Enter → open source
- Tab → switch panel (sources / preview / actions)
- e → execute
- b → back
- Status bar at bottom (like vim)

