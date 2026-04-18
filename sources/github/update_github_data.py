import os
import json
import requests
import re
from datetime import datetime

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
USERNAME = "kreier"
REPOS_PATH = "sources/github/repos.json"
COMMITS_DIR = "sources/github/commits"

def to_camel_case(text):
    # Split by non-alphanumeric characters
    words = re.split(r'[^a-zA-Z0-9]', text)
    # Remove empty strings
    words = [w for w in words if w]
    if not words:
        return text
    return words[0].lower() + "".join(w.capitalize() for w in words[1:])

def run_graphql_query(query, variables=None):
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.post("https://api.github.com/graphql",
                             json={"query": query, "variables": variables},
                             headers=headers)
    if response.status_code == 200:
        result = response.json()
        if "errors" in result:
            print(f"GraphQL Errors: {result['errors']}")
            return None
        return result
    else:
        print(f"Failed to fetch data: {response.status_code} {response.text}")
        return None

def fetch_all_repositories(username):
    query = """
    query($username: String!, $cursor: String) {
      user(login: $username) {
        repositories(first: 100, after: $cursor) {
          pageInfo {
            hasNextPage
            endCursor
          }
          nodes {
            name
            description
            url
            homepageUrl
            isArchived
            isFork
            isPrivate
            updatedAt
            stargazerCount
            primaryLanguage {
              name
            }
            languages(first: 10) {
              edges {
                size
                node {
                  name
                }
              }
            }
            repositoryTopics(first: 10) {
              nodes {
                topic {
                  name
                }
              }
            }
          }
        }
      }
    }
    """
    all_repos = []
    cursor = None
    while True:
        variables = {"username": username, "cursor": cursor}
        result = run_graphql_query(query, variables)
        if not result:
            break

        repo_data = result["data"]["user"]["repositories"]
        for repo in repo_data["nodes"]:
            # Flatten some structures to match existing repos.json
            processed_repo = repo.copy()
            if repo["languages"]:
                processed_repo["languages"] = [
                    {"size": edge["size"], "node": {"name": edge["node"]["name"]}}
                    for edge in repo["languages"]["edges"]
                ]
            if repo["repositoryTopics"]:
                processed_repo["repositoryTopics"] = [
                    {"name": node["topic"]["name"]}
                    for node in repo["repositoryTopics"]["nodes"]
                ]
            else:
                processed_repo["repositoryTopics"] = None

            all_repos.append(processed_repo)

        if not repo_data["pageInfo"]["hasNextPage"]:
            break
        cursor = repo_data["pageInfo"]["endCursor"]

    return all_repos

def fetch_commits(repo_name, since_date=None):
    query = """
    query($owner: String!, $name: String!, $cursor: String, $since: DateTime) {
      repository(owner: $owner, name: $name) {
        defaultBranchRef {
          target {
            ... on Commit {
              history(first: 100, after: $cursor, since: $since) {
                pageInfo {
                  hasNextPage
                  endCursor
                }
                nodes {
                  committedDate
                  message
                  oid
                }
              }
            }
          }
        }
      }
    }
    """
    all_commits = []
    cursor = None
    while True:
        variables = {
            "owner": USERNAME,
            "name": repo_name,
            "cursor": cursor,
            "since": since_date
        }
        result = run_graphql_query(query, variables)
        if not result:
            break

        repo = result["data"]["repository"]
        if not repo or not repo["defaultBranchRef"]:
            break

        history = repo["defaultBranchRef"]["target"]["history"]
        for commit in history["nodes"]:
            all_commits.append({
                "timestamp": commit["committedDate"],
                "message": commit["message"],
                "hash": commit["oid"]
            })

        if not history["pageInfo"]["hasNextPage"]:
            break
        cursor = history["pageInfo"]["endCursor"]

    return all_commits

def main():
    if not GITHUB_TOKEN:
        print("GITHUB_TOKEN not found in environment.")
        return

    # 1. Fetch and update repository list
    print(f"Fetching repositories for {USERNAME}...")
    repositories = fetch_all_repositories(USERNAME)
    if repositories:
        with open(REPOS_PATH, 'w', encoding='utf-8') as f:
            json.dump(repositories, f, indent=2, ensure_ascii=False)
        print(f"Updated {REPOS_PATH} with {len(repositories)} repositories.")

    # 2. Ensure commits directory exists
    os.makedirs(COMMITS_DIR, exist_ok=True)

    # 3. Fetch commits for each repository
    for repo in repositories:
        repo_name = repo["name"]
        filename = f"commits_{to_camel_case(repo_name)}.json"
        filepath = os.path.join(COMMITS_DIR, filename)

        existing_commits = []
        since_date = None

        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                try:
                    existing_commits = json.load(f)
                    if existing_commits:
                        # Sort by timestamp to find the latest
                        existing_commits.sort(key=lambda x: x['timestamp'], reverse=True)
                        since_date = existing_commits[0]['timestamp']
                except json.JSONDecodeError:
                    existing_commits = []

        print(f"Fetching commits for {repo_name}...", end=" ")
        new_commits = fetch_commits(repo_name, since_date)

        if new_commits:
            # Filter out the commit that matches since_date exactly if it was returned
            if since_date:
                new_commits = [c for c in new_commits if c['timestamp'] > since_date]

            if new_commits:
                total_commits = new_commits + existing_commits
                # Sort by date descending
                total_commits.sort(key=lambda x: x['timestamp'], reverse=True)
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(total_commits, f, indent=2, ensure_ascii=False)
                print(f"Added {len(new_commits)} new commits.")
            else:
                print("Already up to date.")
        else:
            print("Already up to date or no commits found.")

if __name__ == "__main__":
    main()
