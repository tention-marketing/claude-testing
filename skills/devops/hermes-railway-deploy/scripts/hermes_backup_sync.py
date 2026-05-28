#!/usr/bin/env python3
"""
Hermes Backup Sync
Watches ~/.hermes personal data folders and auto-commits + pushes to a private GitHub repo.
Repo: github.com/Rajeevboy/claude-testing (PRIVATE)
Backup working dir: /home/rajeev/hermes-backup/ (a fresh clone of the repo)

What syncs: skills/, scripts/, discord_backup/, SOUL.md
What does NOT sync: sessions/, memories/, auth.json, config.yaml, hermes-agent/

Debounce: 15 seconds after last change before pushing.
Run via: terminal(background=True) in Hermes
Log: ~/.hermes/logs/backup_sync.log
"""

import time
import shutil
import subprocess
import logging
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

BACKUP_REPO = Path("/home/rajeev/hermes-backup")
SYNC_SOURCES = {
    Path.home() / ".hermes" / "skills":          BACKUP_REPO / "skills",
    Path.home() / ".hermes" / "scripts":         BACKUP_REPO / "scripts",
    Path.home() / ".hermes" / "discord_backup":  BACKUP_REPO / "discord_backup",
    Path.home() / ".hermes" / "SOUL.md":         BACKUP_REPO / "SOUL.md",
}

DEBOUNCE_SECONDS = 15

IGNORE_PATTERNS = [
    "__pycache__", ".git", "*.pyc", "*.pyo",
    "*.log", "*.tmp", "*.swp", "*.db", "*.db-shm", "*.db-wal"
]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [hermes-backup] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(Path.home() / ".hermes" / "logs" / "backup_sync.log")
    ]
)
log = logging.getLogger("hermes-backup")


def should_ignore(path: str) -> bool:
    for pat in IGNORE_PATTERNS:
        if pat.startswith("*"):
            if path.endswith(pat[1:]): return True
        elif pat in path: return True
    return False


def sync_files():
    for src, dst in SYNC_SOURCES.items():
        if not src.exists(): continue
        if src.is_dir():
            if dst.exists(): shutil.rmtree(dst)
            shutil.copytree(src, dst, ignore=shutil.ignore_patterns(
                "__pycache__", "*.pyc", "*.pyo", "*.log", ".git"))
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    log.info("Files synced to backup repo.")


def git_push():
    try:
        sync_files()
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=BACKUP_REPO, capture_output=True, text=True)
        if not result.stdout.strip():
            log.info("No changes to commit."); return
        subprocess.run(["git", "add", "-A"], cwd=BACKUP_REPO, check=True)
        msg = f"auto-backup: {time.strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(["git", "commit", "-m", msg], cwd=BACKUP_REPO, check=True)
        result = subprocess.run(
            ["git", "push", "origin", "main"],
            cwd=BACKUP_REPO, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            log.info("Pushed to github.com/Rajeevboy/claude-testing")
        else:
            log.error(f"Push failed: {result.stderr.strip()}")
    except Exception as e:
        log.error(f"Error: {e}")


class ChangeHandler(FileSystemEventHandler):
    def __init__(self):
        self._last_change = 0
        self._pending = False

    def on_any_event(self, event):
        if event.is_directory or should_ignore(event.src_path): return
        self._last_change = time.time()
        self._pending = True
        log.info(f"Change detected: {event.src_path}")

    def check_and_push(self):
        if self._pending and (time.time() - self._last_change) >= DEBOUNCE_SECONDS:
            log.info("Debounce complete — syncing and pushing...")
            git_push()
            self._pending = False


if __name__ == "__main__":
    log.info("Hermes Backup Sync started")
    log.info("Running initial sync...")
    git_push()

    handler = ChangeHandler()
    observer = Observer()
    for src in SYNC_SOURCES:
        watch_path = src if src.is_dir() else src.parent
        if watch_path.exists():
            observer.schedule(handler, str(watch_path), recursive=True)
            log.info(f"Watching: {watch_path}")

    observer.start()
    try:
        while True:
            handler.check_and_push()
            time.sleep(2)
    except KeyboardInterrupt:
        log.info("Stopped.")
        observer.stop()
    observer.join()
