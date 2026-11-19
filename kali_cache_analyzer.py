#!/usr/bin/env python3

import os
import pwd
from pathlib import Path

# ==========================================
# KALI LINUX CACHE ANALYZER
# Read-only storage analysis
# ==========================================

def get_user_home():
    if os.environ.get("SUDO_USER"):
        return Path(pwd.getpwnam(
            os.environ["SUDO_USER"]
        ).pw_dir)

    return Path.home()


HOME = get_user_home()

SAFE_NAMES = {
    "Cache",
    "Code Cache",
    "GPUCache",
    "cache2",
    "thumbnails",
}

results = []
errors = 0


def folder_size(path):
    global errors

    total = 0

    if not path.exists() or not path.is_dir():
        return 0

    for root, dirs, files in os.walk(path):

        dirs[:] = [
            d for d in dirs
            if not (Path(root) / d).is_symlink()
        ]

        for filename in files:
            file_path = Path(root) / filename

            try:
                if not file_path.is_symlink():
                    total += file_path.stat().st_size
            except (PermissionError, OSError):
                errors += 1

    return total


def add_result(name, path, category):
    size = folder_size(path)

    if size > 0:
        results.append({
            "name": name,
            "path": str(path),
            "size": size,
            "category": category
        })


def scan_user_cache():

    base = HOME / ".cache"

    if not base.exists():
        return

    for app_dir in base.iterdir():

        if not app_dir.is_dir() or app_dir.is_symlink():
            continue

        total = folder_size(app_dir)

        safe_dirs = []

        for root, dirs, files in os.walk(app_dir):

            dirs[:] = [
                d for d in dirs
                if not (Path(root) / d).is_symlink()
            ]

            for dirname in dirs:

                if dirname in SAFE_NAMES:
                    safe_dirs.append(
                        Path(root) / dirname
                    )

        # Avoid counting nested safe directories twice
        safe_dirs.sort(key=lambda p: len(p.parts))

        selected = []

        for path in safe_dirs:
            if not any(parent in path.parents for parent in selected):
                selected.append(path)

        safe_size = 0

        for path in selected:
            size = folder_size(path)

            if size > 0:
                safe_size += size

                results.append({
                    "name": f"{app_dir.name} / {path.name}",
                    "path": str(path),
                    "size": size,
                    "category": "LIKELY SAFE"
                })

        remaining = max(0, total - safe_size)

        if remaining > 0:
            results.append({
                "name": app_dir.name + " / Other cache data",
                "path": str(app_dir),
                "size": remaining,
                "category": "REVIEW"
            })


def scan_browser_cache():

    browsers = {
        "Chromium": HOME / ".config/chromium",
        "Google Chrome": HOME / ".config/google-chrome",
    }

    for browser, base in browsers.items():

        if not base.exists():
            continue

        for profile in base.iterdir():

            if not profile.is_dir():
                continue

            for cache_name in SAFE_NAMES:

                path = profile / cache_name

                if path.exists():
                    add_result(
                        f"{browser} / {profile.name} / {cache_name}",
                        path,
                        "LIKELY SAFE"
                    )

    firefox = HOME / ".mozilla/firefox"

    if firefox.exists():

        for profile in firefox.iterdir():

            path = profile / "cache2"

            if path.exists():
                add_result(
                    f"Firefox / {profile.name}",
                    path,
                    "LIKELY SAFE"
                )


def scan_system_cache():

    # APT downloaded package cache
    apt_cache = Path("/var/cache/apt/archives")

    add_result(
        "APT Download Cache",
        apt_cache,
        "LIKELY SAFE"
    )

    # Other system cache directories
    base = Path("/var/cache")

    if base.exists():

        for item in base.iterdir():

            if item.name == "apt":
                continue

            if item.is_dir() and not item.is_symlink():

                add_result(
                    "System / " + item.name,
                    item,
                    "REVIEW"
                )


def scan_external_caches():

    # Python pip cache
    pip_cache = HOME / ".cache/pip"

    add_result(
        "Python Pip Cache",
        pip_cache,
        "LIKELY SAFE"
    )

    # NPM cache
    npm_cache = HOME / ".npm"

    add_result(
        "Node.js NPM Cache",
        npm_cache,
        "LIKELY SAFE"
    )


def format_size(size):

    if size >= 1024 ** 3:
        return f"{size / (1024 ** 3):.2f} GB"

    return f"{size / (1024 ** 2):.2f} MB"


def print_report():

    global results

    print("\n" + "=" * 90)
    print("                 KALI LINUX CACHE ANALYZER")
    print("=" * 90)

    print("\nScanning user application caches...")
    scan_user_cache()

    print("Scanning browser caches...")
    scan_browser_cache()

    print("Scanning system caches...")
    scan_system_cache()

    print("Scanning external package caches...")
    scan_external_caches()

    # Remove duplicate paths
    unique = {}

    for item in results:
        key = item["path"]

        if key not in unique:
            unique[key] = item
        elif item["category"] == "LIKELY SAFE":
            unique[key] = item

    results = list(unique.values())

    results.sort(
        key=lambda x: x["size"],
        reverse=True
    )

    safe_total = 0
    review_total = 0

    print("\n" + "-" * 90)
    print(f"{'APPLICATION / CACHE':<38}"
          f"{'SIZE':>15}  {'STATUS':<18}")
    print("-" * 90)

    for item in results:

        print(
            f"{item['name'][:37]:<38}"
            f"{format_size(item['size']):>15}  "
            f"{item['category']:<18}"
        )

        if item["category"] == "LIKELY SAFE":
            safe_total += item["size"]
        else:
            review_total += item["size"]

    total = safe_total + review_total

    print("-" * 90)
    print(f"LIKELY SAFE CACHE: {format_size(safe_total)}")
    print(f"REQUIRES REVIEW:   {format_size(review_total)}")
    print(f"TOTAL FOUND:       {format_size(total)}")

    print("-" * 90)
    print(f"Permission/read errors: {errors}")

    print("\nSTATUS EXPLANATION:")
    print("LIKELY SAFE = Regenerable cache; generally safe to clear.")
    print("REVIEW      = Requires manual inspection before deletion.")

    print("\nNo files were deleted or modified.")
    print("=" * 90)


if __name__ == "__main__":

    print_report()
