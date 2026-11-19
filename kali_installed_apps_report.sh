#!/bin/bash

# Installed Applications Report
# Kali Linux

REPORT="installed_apps_report.txt"

python3 - <<'PY' | tee installed_apps_report.txt
import os
import re
import glob
import gzip
import subprocess

packages = set()

# APT history logs
files = glob.glob("/var/log/apt/history.log*")

for path in files:
    try:
        if path.endswith(".gz"):
            with gzip.open(path, "rt", errors="ignore") as f:
                content = f.read()
        else:
            with open(path, "r", errors="ignore") as f:
                content = f.read()

        for line in content.splitlines():
            if line.startswith("Install:"):
                matches = re.findall(
                    r'([a-zA-Z0-9][a-zA-Z0-9.+-]*(?::[a-zA-Z0-9_-]+)?)\s+\(',
                    line[8:]
                )
                packages.update(matches)

    except Exception:
        pass

# Currently installed packages and their declared sizes
result = subprocess.run(
    ["dpkg-query", "-W", "-f=${binary:Package}\t${Installed-Size}\n"],
    capture_output=True,
    text=True
)

installed = {}

for line in result.stdout.splitlines():
    parts = line.split("\t")

    if len(parts) != 2:
        continue

    name, size = parts

    try:
        installed[name.split(":")[0]] = int(size)
    except ValueError:
        continue

# Match historical installations with currently installed packages
report = []

for package in packages:
    name = package.split(":")[0]

    if name in installed:
        size_kb = installed[name]
        report.append((name, size_kb))

report.sort(key=lambda x: x[1], reverse=True)

total_kb = sum(size for _, size in report)

print("=" * 65)
print("          KALI LINUX - INSTALLED APPLICATIONS REPORT")
print("=" * 65)
print(f"\n{'PACKAGE':40} {'SIZE':>15}")
print("-" * 65)

for name, size in report:
    if size >= 1024 * 1024:
        formatted = f"{size / 1024 / 1024:.2f} GB"
    else:
        formatted = f"{size / 1024:.2f} MB"

    print(f"{name:40} {formatted:>15}")

print("-" * 65)
print(f"Total packages: {len(report)}")
print(f"Total declared size: {total_kb / 1024:.2f} MB")
print("=" * 65)

if not report:
    print("\nNo matching installations found in APT history.")
    print("APT history may be empty or rotated.")
PY

