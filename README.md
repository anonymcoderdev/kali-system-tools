# Kali Linux System Tools

A collection of lightweight system administration and analysis tools for Kali Linux. This project focuses on disk usage monitoring, installed package reporting, and cache analysis.

## Tools

### 1. Disk Space Monitor — `disk_space.sh`
A simple shell script for checking available disk space.

**Features:**
- Displays disk usage.
- Shows available storage.
- Reports disk capacity in a readable format.

**Usage:**
chmod +x disk_space.sh
./disk_space.sh

### 2. Installed Applications Report — `installed_apps_report.sh`

Generates a report of installed packages and their storage requirements.

**Features:**
- Lists installed packages.
- Displays package sizes.
- Helps identify storage-intensive software.
- Provides an overview of installed software.

**Usage:**
chmod +x installed_apps_report.sh
./installed_apps_report.sh

### 3. Kali Cache Analyzer — `kali_cache_analyzer.py`
A Python-based tool for analyzing cache directories and identifying potentially removable cache data.

**Features:**
- Scans selected application cache directories.
- Checks browser cache locations.
- Analyzes system cache directories.
- Detects Python pip and npm caches.
- Calculates cache sizes in MB and GB.
- Classifies results into two categories:
  - `LIKELY SAFE` — Cache data that is generally regenerable.
  - `REVIEW` — Data requiring manual inspection before removal.
- Displays total cache usage.
- Reports permission and read errors.

**Important:** This tool operates in read-only mode. It does not delete or modify files. All cleanup decisions remain under the user's control.

**Usage:**
python3 kali_cache_analyzer.py

## Requirements
- Kali Linux
- Bash
- Python 3
- Standard Linux utilities
No additional Python packages are required for the cache analyzer.

## Installation
Clone the repository:
git clone https://github.com/anonymcoderdev/kali-system-tools.git

Navigate to the project directory:
cd kali-system-tools
Make shell scripts executable:
chmod +x *.sh
chmod +x *.py


## Project Structure
kali-system-tools/
│
disk_space.sh
installed_apps_report.sh
kali_cache_analyzer.py
README.md

## Safety
These tools are designed for local system inspection and reporting.
- No automatic package removal.
- No automatic cache deletion.
- No modification of system configuration.
- Manual review is recommended before removing any files.

## Platform
Developed and tested for Kali Linux.

## License
This project is licensed under the MIT License.