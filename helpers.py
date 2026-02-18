"""
Shared helper functions for the Dead in the Region editor app.
Used across all pages (Episode Editor, Speaker Profiles, Audience & Mood).
"""
import os
import json
import streamlit as st

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def get_github_client():
    """Return a PyGithub repo object, or None if secrets aren't set."""
    try:
        from github import Github
        token = st.secrets["github"]["token"]
        repo_name = st.secrets["github"]["repo"]
        if not token or not repo_name:
            return None
        g = Github(token)
        return g.get_repo(repo_name)
    except Exception:
        return None


def commit_json_to_github(filepath_in_repo: str, content: str, message: str):
    """Commit a JSON file to the GitHub repo. Returns (success, message)."""
    repo = get_github_client()
    if repo is None:
        return False, "GitHub not configured."
    try:
        try:
            existing = repo.get_contents(filepath_in_repo)
            repo.update_file(filepath_in_repo, message, content, existing.sha)
            return True, "Updated on GitHub."
        except Exception:
            repo.create_file(filepath_in_repo, message, content)
            return True, "Created on GitHub."
    except Exception as e:
        return False, str(e)


def load_speakers():
    """Load speakers.json and return the dict."""
    path = os.path.join(DATA_DIR, "speakers.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {"speakers": []}


def save_speakers(data: dict):
    """Save speakers data locally and to GitHub."""
    path = os.path.join(DATA_DIR, "speakers.json")
    content = json.dumps(data, indent=2)
    with open(path, "w") as f:
        f.write(content)
    gh_ok, gh_msg = commit_json_to_github(
        "data/speakers.json", content, "Update speaker profiles"
    )
    return gh_ok, gh_msg


def load_audience():
    """Load audience.json and return the dict."""
    path = os.path.join(DATA_DIR, "audience.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {"audience": {}}


def save_audience(data: dict):
    """Save audience data locally and to GitHub."""
    path = os.path.join(DATA_DIR, "audience.json")
    content = json.dumps(data, indent=2)
    with open(path, "w") as f:
        f.write(content)
    gh_ok, gh_msg = commit_json_to_github(
        "data/audience.json", content, "Update audience & mood settings"
    )
    return gh_ok, gh_msg
