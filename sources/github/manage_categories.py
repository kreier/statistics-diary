import json
from collections import Counter
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, ListView, ListItem, Static, Label, Button, Input, Select
from textual.containers import Container, Horizontal, Vertical, Grid
from textual.screen import Screen, ModalScreen
from textual import on, work

REPOS_PATH = 'sources/github/repos.json'
CATEGORIES_PATH = 'sources/github/repository_categories.json'

class CategoryStats(Static):
    def update_stats(self, category_id, repos, mapping):
        cat_repos = [r for r in repos if mapping.get(r['name']) == category_id]
        count = len(cat_repos)
        stars = sum(r.get('stargazerCount', 0) for r in cat_repos)

        langs = Counter()
        for r in cat_repos:
            if r.get('primaryLanguage'):
                langs[r['primaryLanguage']['name']] += 1

        top_langs = ", ".join([f"{l} ({c})" for l, c in langs.most_common(3)])

        self.update(f"[b]Category:[/b] {category_id}\n"
                    f"[b]Repositories:[/b] {count}\n"
                    f"[b]Total Stars:[/b] {stars}\n"
                    f"[b]Top Languages:[/b] {top_langs if top_langs else 'N/A'}")

class EditCategoryScreen(ModalScreen):
    def __init__(self, category=None):
        super().__init__()
        self.category = category or {"id": "", "name": ""}

    def compose(self) -> ComposeResult:
        yield Grid(
            Label("Category ID:", classes="label"),
            Input(value=self.category["id"], id="cat_id", placeholder="e.g. tools"),
            Label("Full Name:", classes="label"),
            Input(value=self.category["name"], id="cat_name", placeholder="e.g. Tools / Utilities"),
            Horizontal(
                Button("Save", variant="success", id="save"),
                Button("Cancel", variant="error", id="cancel"),
                classes="buttons"
            ),
            id="category_dialog"
        )

    @on(Button.Pressed, "#save")
    def save(self):
        cid = self.query_one("#cat_id").value.strip()
        cname = self.query_one("#cat_name").value.strip()
        if cid and cname:
            self.dismiss({"id": cid, "name": cname})
        else:
            self.app.notify("Both ID and Name are required", variant="error")

    @on(Button.Pressed, "#cancel")
    def cancel(self):
        self.dismiss(None)

class AssignCategoryScreen(ModalScreen):
    def __init__(self, repo_name, categories, current_cat):
        super().__init__()
        self.repo_name = repo_name
        self.categories = categories
        self.current_cat = current_cat

    def compose(self) -> ComposeResult:
        options = [(c['name'], c['id']) for c in self.categories]
        yield Grid(
            Label(f"Assign [b]{self.repo_name}[/b] to category:"),
            Select(options, value=self.current_cat, id="cat_select"),
            Horizontal(
                Button("Assign", variant="success", id="assign"),
                Button("Cancel", variant="error", id="cancel"),
                classes="buttons"
            ),
            id="assign_dialog"
        )

    @on(Button.Pressed, "#assign")
    def assign(self):
        new_cat = self.query_one("#cat_select").value
        self.dismiss(new_cat)

    @on(Button.Pressed, "#cancel")
    def cancel(self):
        self.dismiss(None)

class RepoManager(App):
    CSS = """
    #main_container {
        layout: grid;
        grid-size: 2;
        grid-columns: 1fr 2fr;
    }
    .sidebar {
        border-right: tall $primary;
        padding: 1;
    }
    .content {
        padding: 1;
    }
    #category_dialog, #assign_dialog {
        padding: 1 2;
        background: $panel;
        border: thick $primary;
        width: 60;
        height: auto;
        align: center middle;
        grid-size: 2;
        grid-rows: auto auto auto;
        grid-columns: 15 40;
        grid-gutter: 1;
    }
    .label {
        height: 3;
        content-align: right middle;
    }
    .buttons {
        column-span: 2;
        align: center middle;
        height: 5;
        gap: 2;
    }
    ListItem {
        padding: 1;
    }
    .uncategorized {
        color: $warning;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("a", "add_category", "Add Category"),
        ("e", "edit_category_binding", "Edit Category"),
        ("s", "save_all", "Save All"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Vertical(
                Label("[b]Categories[/b]"),
                ListView(id="category_list"),
                classes="sidebar"
            ),
            Vertical(
                CategoryStats(id="stats"),
                Label("\n[b]Repositories in this category[/b] (click to reassign)"),
                ListView(id="repo_list"),
                classes="content"
            ),
            id="main_container"
        )
        yield Footer()

    def on_mount(self):
        self.load_data()
        self.refresh_categories()
        self.current_category = "uncategorized"
        self.refresh_repos("uncategorized")

    def load_data(self):
        try:
            with open(REPOS_PATH, 'r', encoding='utf-8') as f:
                self.repos = json.load(f)
            with open(CATEGORIES_PATH, 'r', encoding='utf-8') as f:
                cat_data = json.load(f)
                self.categories = cat_data['categories']
                self.repo_mapping = cat_data['repo_mapping']
        except Exception as e:
            self.notify(f"Error loading data: {e}", variant="error")
            self.repos = []
            self.categories = [{"id": "uncategorized", "name": "Uncategorized"}]
            self.repo_mapping = {}

        # Ensure all repos in mapping
        for r in self.repos:
            if r['name'] not in self.repo_mapping:
                self.repo_mapping[r['name']] = "uncategorized"

    def refresh_categories(self):
        list_view = self.query_one("#category_list", ListView)
        list_view.clear()
        for cat in self.categories:
            label = f"{cat['name']} ({cat['id']})"
            list_view.append(ListItem(Label(label), id=f"cat_{cat['id']}"))

    def refresh_repos(self, category_id):
        list_view = self.query_one("#repo_list", ListView)
        list_view.clear()
        cat_repos = [r for r in self.repos if self.repo_mapping.get(r['name']) == category_id]
        cat_repos.sort(key=lambda x: x['name'])
        for repo in cat_repos:
            list_view.append(ListItem(Label(repo['name']), id=f"repo_{repo['name']}"))

        self.query_one("#stats", CategoryStats).update_stats(category_id, self.repos, self.repo_mapping)

    @on(ListView.Selected, "#category_list")
    def category_selected(self, event):
        if event.item and event.item.id:
            cat_id = event.item.id.replace("cat_", "")
            self.current_category = cat_id
            self.refresh_repos(cat_id)

    @on(ListView.Selected, "#repo_list")
    def repo_selected(self, event):
        if event.item and event.item.id:
            repo_name = event.item.id.replace("repo_", "")
            self.action_assign_repo(repo_name)

    def action_assign_repo(self, repo_name):
        current_cat = self.repo_mapping.get(repo_name, "uncategorized")
        def handle_assignment(new_cat):
            if new_cat and new_cat != current_cat:
                self.repo_mapping[repo_name] = new_cat
                self.refresh_repos(self.current_category)
                self.notify(f"Moved {repo_name} to {new_cat}")

        self.push_screen(AssignCategoryScreen(repo_name, self.categories, current_cat), handle_assignment)

    def action_edit_category_binding(self):
        if hasattr(self, 'current_category'):
            self.action_edit_category(self.current_category)

    def action_add_category(self):
        def handle_new_cat(new_cat):
            if new_cat:
                # Check if ID already exists
                if any(c['id'] == new_cat['id'] for c in self.categories):
                    self.notify("Category ID already exists", variant="error")
                    return
                self.categories.append(new_cat)
                self.refresh_categories()
                self.notify(f"Added category {new_cat['name']}")

        self.push_screen(EditCategoryScreen(), handle_new_cat)

    def action_edit_category(self, cat_id):
        if cat_id == "uncategorized":
            self.notify("Cannot edit the uncategorized category", variant="error")
            return

        category = next((c for c in self.categories if c['id'] == cat_id), None)
        if not category:
            return

        def handle_edit(updated_cat):
            if updated_cat:
                old_id = category['id']
                new_id = updated_cat['id']

                # If ID changed, update mapping
                if old_id != new_id:
                    # Check if new ID already exists
                    if any(c['id'] == new_id for c in self.categories):
                        self.notify(f"Cannot change ID to {new_id}: already exists", variant="error")
                        return

                    for repo, cid in self.repo_mapping.items():
                        if cid == old_id:
                            self.repo_mapping[repo] = new_id

                category['id'] = new_id
                category['name'] = updated_cat['name']
                self.refresh_categories()
                self.refresh_repos(new_id)
                self.current_category = new_id
                self.notify(f"Updated category {category['name']}")

        self.push_screen(EditCategoryScreen(category.copy()), handle_edit)

    def action_save_all(self):
        output = {
            "categories": self.categories,
            "repo_mapping": self.repo_mapping
        }
        with open(CATEGORIES_PATH, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2)
        self.notify("Changes saved to " + CATEGORIES_PATH)

if __name__ == "__main__":
    app = RepoManager()
    app.run()
