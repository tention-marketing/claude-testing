#!/usr/bin/env python3
"""
Make a GitHub repo private using stored git credentials.
Works even when gh CLI auth has expired.
Token is read from ~/.git-credentials via git credential fill — never echoed.

Usage: python3 make_repo_private.py OWNER REPO
Example: python3 make_repo_private.py Rajeevboy claude-testing
"""

import sys
import re
import subprocess
import urllib.request
import json

def get_token():
    result = subprocess.run(
        ['git', 'credential', 'fill'],
        input='protocol=https\nhost=github.com\n',
        capture_output=True, text=True
    )
    m = re.search(r'password=(.+)', result.stdout)
    if not m:
        raise RuntimeError("No GitHub token found in git credential store.")
    return m.group(1).strip()

def set_repo_visibility(owner, repo, private: bool):
    token = get_token()
    data = json.dumps({"private": private}).encode()
    req = urllib.request.Request(
        f'https://api.github.com/repos/{owner}/{repo}',
        data=data, method='PATCH'
    )
    req.add_header('Authorization', 'token ' + token)
    req.add_header('Content-Type', 'application/json')
    req.add_header('User-Agent', 'hermes')
    try:
        resp = urllib.request.urlopen(req)
        d = json.loads(resp.read())
        print(f"Repo: {d.get('full_name')}")
        print(f"Private: {d.get('private')}")
        print("SUCCESS")
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"Error {e.code}: {body[:300]}")

def check_visibility_public(owner, repo):
    """Returns True if repo is publicly accessible without credentials."""
    result = subprocess.run(
        ['git', 'ls-remote', f'https://github.com/{owner}/{repo}'],
        capture_output=True, text=True,
        env={**__import__('os').environ, 'GIT_TERMINAL_PROMPT': '0'}
    )
    return result.returncode == 0 and bool(result.stdout.strip())

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 make_repo_private.py OWNER REPO")
        sys.exit(1)
    owner, repo = sys.argv[1], sys.argv[2]
    print(f"Checking {owner}/{repo}...")
    is_public = check_visibility_public(owner, repo)
    print(f"Currently: {'PUBLIC' if is_public else 'PRIVATE (or inaccessible)'}")
    if is_public:
        print("Making private...")
        set_repo_visibility(owner, repo, private=True)
    else:
        print("Already private — no change needed.")
