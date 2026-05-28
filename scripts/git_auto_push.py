#!/usr/bin/env python3
"""
File watcher: watches ~/.hermes/hermes-agent for any changes
and auto-commits + pushes to github.com/Rajeevboy/claude-testing
"""

import time
import subprocess
import logging
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

WATCH_DIR = Path.home() / ".hermes" / "hermes-agent"
REMOTE = "rajeev"
BRANCH = "main"
DEBOUNCE_SECONDS = 10  # wait 10s after last change before pushing

# Folders/files to ignore
IGNORE_PATTERNS = [
    "__pycache__", ".git", "*.pyc", "*.pyo", "*.log",
    "venv", ".venv", "node_modules", "*.egg-info",
    "hermes-agent.egg-info", "*.db", "*.db-shm", "*.db-wal",
    ".pytest_cache", "*.tmp", "*.swp", "audio_cache", "image_cache"
]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [git-watcher] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
log = logging.getLogger("git-watcher")


def should_ignore(path: str) -> bool:
    for pat in IGNORE_PATTERNS:
        if pat.startswith("*"):
            if path.endswith(pat[1:]):
                return True
        elif pat in path:
            return True
    return False


def git_push():
    try:
        # Check if there's anything to commit
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=WATCH_DIR, capture_output=True, text=True
        )
        if not result.stdout.strip():
            log.info("No changes to commit.")
            return

        # Stage all changes
        subprocess.run(["git", "add", "-A"], cwd=WATCH_DIR, check=True)

        # Commit
        msg = f"auto: file watcher sync {time.strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(["git", "commit", "-m", msg], cwd=WATCH_DIR, check=True)

        # Push to rajeev remote
        result = subprocess.run(
            ["git", "push", REMOTE, BRANCH, "--force"],
            cwd=WATCH_DIR, capture_output=True, text=True
        )
        if result.returncode == 0:
            log.info(f"Pushed to github.com/Rajeevboy/claude-testing ({BRANCH})")
        else:
            log.error(f"Push failed: {result.stderr.strip()}")

    except subprocess.CalledProcessError as e:
        log.error(f"Git error: {e}")
    except Exception as e:
        log.error(f"Unexpected error: {e}")


class ChangeHandler(FileSystemEventHandler):
    def __init__(self):
        self._last_change = 0
        self._pending = False

    def on_any_event(self, event):
        if event.is_directory:
            return
        if should_ignore(event.src_path):
            return

        self._last_change = time.time()
        if not self._pending:
            self._pending = True

    def check_and_push(self):
        if self._pending and (time.time() - self._last_change) >= DEBOUNCE_SECONDS:
            log.info("Change detected — committing and pushing...")
            git_push()
            self._pending = False


if __name__ == "__main__":
    log.info(f"Watching: {WATCH_DIR}")
    log.info(f"Pushing to: github.com/Rajeevboy/claude-testing ({BRANCH})")
    log.info(f"Debounce: {DEBOUNCE_SECONDS}s after last change")

    handler = ChangeHandler()
    observer = Observer()
    observer.schedule(handler, str(WATCH_DIR), recursive=True)
    observer.start()

    try:
        while True:
            handler.check_and_push()
            time.sleep(2)
    except KeyboardInterrupt:
        log.info("Stopped.")
        observer.stop()
    observer.join()
