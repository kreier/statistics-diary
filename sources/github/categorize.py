import json
import re
from bs4 import BeautifulSoup

def parse_dashboard():
    with open('sources/github/kreier_github_dashboard.html', 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')

    categories_info = [
        {"id": "embedded", "name": "Embedded / IoT / Hardware"},
        {"id": "robotics", "name": "Robotics"},
        {"id": "ai", "name": "AI / ML / LLM"},
        {"id": "benchmarking", "name": "Benchmarking / Performance"},
        {"id": "data", "name": "Data / Science / Jupyter"},
        {"id": "tools", "name": "Tools / Utilities"},
        {"id": "teaching", "name": "Teaching / Education"},
        {"id": "web", "name": "Web / Frontend"},
        {"id": "mobile", "name": "Mobile (iOS / Android)"},
        {"id": "math", "name": "Math / Creative"}
    ]

    mapping = {}

    cards = soup.find_all('div', class_='card')
    for card in cards:
        header = card.find('div', class_='category-header')
        if not header:
            continue

        category_text = header.get_text()
        matched_cat = None
        for cat in categories_info:
            if cat['name'].lower() in category_text.lower() or category_text.lower() in cat['name'].lower():
                matched_cat = cat['id']
                break

        if not matched_cat:
            continue

        repo_rows = card.find_all('div', class_='repo-row')
        for row in repo_rows:
            # Check for links
            links = row.find_all('a')
            for link in links:
                repo_name = link.get_text().strip()
                if repo_name:
                    mapping[repo_name] = matched_cat

            # Check for comma separated names in text
            name_div = row.find('div', class_='repo-name')
            if name_div and not name_div.find('a'):
                text = name_div.get_text().strip()
                # Split by comma or series indicators
                parts = re.split(r'[,/–]| (?:and|plus) ', text)
                for part in parts:
                    name = part.strip().rstrip('…')
                    if name and len(name) < 30: # Heuristic to avoid long descriptions
                        mapping[name] = matched_cat

    return categories_info, mapping

def main():
    categories_info, mapping = parse_dashboard()

    # Load all repo names to ensure we have all of them
    with open('sources/github/repos.json', 'r', encoding='utf-8') as f:
        repos = json.load(f)

    all_repo_names = [r['name'] for r in repos]

    final_mapping = {}
    for name in all_repo_names:
        if name in mapping:
            final_mapping[name] = mapping[name]
        else:
            # Try fuzzy matching if exact name not found?
            # For now just leave as uncategorized if not found
            final_mapping[name] = "uncategorized"

    # Add uncategorized to categories_info
    categories_info.append({"id": "uncategorized", "name": "Uncategorized"})

    # Demonstration: Create a new category 'research' and move some repos
    categories_info.insert(0, {"id": "research", "name": "Research & Experiments"})
    if "beston-9volt-battery" in final_mapping:
        final_mapping["beston-9volt-battery"] = "research"
    if "impact" in final_mapping:
        final_mapping["impact"] = "research"

    output = {
        "categories": categories_info,
        "repo_mapping": final_mapping
    }

    with open('sources/github/repository_categories.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2)

if __name__ == "__main__":
    main()
