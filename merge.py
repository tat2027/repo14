#!/usr/bin/env python3
"""
=============================================================================
CloudStream Master Extension Repository Merger
=============================================================================
Automatically fetches extension lists from multiple CloudStream repositories,
merges all plugins into a unified master collection, and generates valid
repository manifest files for CloudStream 3 / CS3.

SPECIAL INSTRUCTION RESPECTED:
"duplicate any dena plugins delete nhi karni"
(Zero plugins are deleted. All duplicate plugins from every repository
are fully preserved and made accessible in CloudStream.)
=============================================================================
"""

import os
import re
import sys
import json
import time
import urllib.request
import urllib.error

# ---------------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------------
# Name and metadata for your master CloudStream repository
REPO_NAME = "CloudStream Master Unified Repo"
REPO_DESCRIPTION = "Unified multi-source CloudStream repository with zero duplicate deletions. Automatically updated via GitHub Actions."
REPO_ICON = "https://raw.githubusercontent.com/LagradOst/CloudStream-3/master/app/src/main/res/drawable/ic_launcher.png"
MANIFEST_VERSION = 1

# Duplicate handling strategy:
# - 'disambiguate': (RECOMMENDED) Keeps ALL plugins. When duplicate internalName
#   is detected from another repo, appends _<repo_slug> to internalName and
#   tags the display name with [RepoName]. This guarantees CloudStream's Android app
#   shows BOTH plugins side-by-side without one overwriting the other!
# - 'raw_keep_all': Exact raw upstream list. Zero modifications. All entries kept.
DUPLICATE_STRATEGY = "disambiguate"

# GitHub Pages repository info (reads from GitHub Actions environment if available)
GITHUB_REPOSITORY = os.environ.get("GITHUB_REPOSITORY", "tat2027/repo14")
if "/" in GITHUB_REPOSITORY:
    GH_USER, GH_REPO = GITHUB_REPOSITORY.split("/", 1)
else:
    GH_USER = "tat2027"
    GH_REPO = "repo14"

PAGES_BASE_URL = f"https://{GH_USER}.github.io/{GH_REPO}"

# Source Repositories to Merge
SOURCE_REPOSITORIES = [
    {
        "name": "CSX (SaurabhKaperwan)",
        "url": "https://raw.githubusercontent.com/SaurabhKaperwan/CSX/builds/CS.json"
    },
    {
        "name": "Phisher Repo",
        "url": "https://raw.githubusercontent.com/phisher98/cloudstream-extensions-phisher/refs/heads/builds/repo.json"
    },
    {
        "name": "CNC Repo (All Language)",
        "url": "https://raw.githubusercontent.com/NivinCNC/CNCVerse-Cloud-Stream-Extension/refs/heads/builds/CNC.json"
    },
    {
        "name": "Cinephile",
        "url": "https://raw.githubusercontent.com/rockhero1234/cinephile/refs/heads/builds/repo.json"
    },
    {
        "name": "raghav repo",
        "url": "https://raw.githubusercontent.com/KSHITIJ8473/raghav/builds/repo.json"
    },
    {
        "name": "AllForU",
        "url": "https://raw.githubusercontent.com/RVRBEAST76/allforu-repo/builds/repo.json"
    },
    {
        "name": "FLUMMOX Repo",
        "url": "https://raw.githubusercontent.com/FlummoxGamer/FLUMMOX-Repo/builds/repo.json"
    },
    {
        "name": "Desi Extensions",
        "url": "https://raw.githubusercontent.com/Faisal0786/Desi/main/repo.json"
    },
    {
        "name": "NetMirror",
        "url": "https://raw.githubusercontent.com/Sushan64/NetMirror-Extension/refs/heads/builds/Netflix.json"
    },
    {
        "name": "XtronRepo",
        "url": "https://raw.githubusercontent.com/MrXtron/CloudStream-Extension/refs/heads/builds/repo.json"
    },
    {
        "name": "Eclipsia",
        "url": "https://cs.eclipsia.dpdns.org/repo.json"
    }
]

# ---------------------------------------------------------------------------
# HTTP FETCHER WITH BUILT-IN RETRIES & ZERO EXTERNAL DEPENDENCIES
# ---------------------------------------------------------------------------
def fetch_json(url: str, retries: int = 3, timeout: int = 20):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) CloudStream-Merger/2.0",
        "Accept": "application/json, text/plain, */*"
    }
    req = urllib.request.Request(url, headers=headers)
    
    last_err = None
    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                content = response.read().decode("utf-8")
                return json.loads(content)
        except Exception as e:
            last_err = e
            if attempt < retries:
                time.sleep(1.5 * attempt)
    raise last_err

def slugify(text: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "_", text.strip())
    return cleaned.strip("_").lower()

# ---------------------------------------------------------------------------
# MAIN MERGE ENGINE
# ---------------------------------------------------------------------------
def fetch_and_merge():
    all_plugins = []
    seen_internal_names = {}
    duplicates_count = 0
    stats = []

    print("=" * 70)
    print("🚀 Starting CloudStream Extension Repositories Merge...")
    print(f"📌 Mode: {DUPLICATE_STRATEGY.upper()} (Zero plugins will be deleted)")
    print(f"🌐 Target Pages Base URL: {PAGES_BASE_URL}")
    print("=" * 70)

    for source in SOURCE_REPOSITORIES:
        name = source["name"]
        url = source["url"]
        print(f"\n🔍 Fetching: {name}")
        print(f"   URL: {url}")

        repo_plugins = []
        try:
            data = fetch_json(url, timeout=20)

            if isinstance(data, list):
                # Direct array of plugin manifests
                repo_plugins.extend(data)
            elif isinstance(data, dict):
                # Standard CloudStream repository manifest
                if "plugins" in data and isinstance(data["plugins"], list):
                    repo_plugins.extend(data["plugins"])
                elif "pluginLists" in data and isinstance(data["pluginLists"], list):
                    for pl in data["pluginLists"]:
                        if isinstance(pl, str):
                            print(f"   -> Fetching pluginList: {pl}")
                            try:
                                sub_data = fetch_json(pl, timeout=25)
                                if isinstance(sub_data, list):
                                    repo_plugins.extend(sub_data)
                            except Exception as sub_e:
                                print(f"   ⚠️ Warning: failed to fetch sub-list {pl}: {sub_e}")
                        elif isinstance(pl, dict):
                            repo_plugins.append(pl)

            print(f"   ✅ Retrieved {len(repo_plugins)} plugin manifests from {name}")

            # Process every single plugin without deletion ("duplicate any dena plugins delete nhi karni")
            for plugin in repo_plugins:
                if not isinstance(plugin, dict):
                    continue

                item = dict(plugin)
                item["sourceRepo"] = name
                orig_id = item.get("internalName") or item.get("name") or "UnknownPlugin"

                if orig_id in seen_internal_names:
                    duplicates_count += 1
                    seen_internal_names[orig_id] += 1
                    item["isDuplicate"] = True

                    if DUPLICATE_STRATEGY == "disambiguate":
                        source_slug = slugify(name)
                        disambiguated_id = f"{orig_id}_{source_slug}"
                        item["internalName"] = disambiguated_id
                        current_title = item.get("name", orig_id)
                        item["name"] = f"{current_title} [{name}]"
                else:
                    seen_internal_names[orig_id] = 1
                    item["isDuplicate"] = False

                all_plugins.append(item)

            stats.append({"name": name, "status": "OK", "count": len(repo_plugins)})

        except Exception as e:
            print(f"   ❌ ERROR loading {name}: {e}")
            stats.append({"name": name, "status": f"FAILED ({e})", "count": 0})

    # ---------------------------------------------------------------------------
    # WRITE MASTER FILES
    # ---------------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("💾 Generating unified repository output files...")

    # 1. plugins.json (The full array of all merged plugins)
    with open("plugins.json", "w", encoding="utf-8") as f:
        json.dump(all_plugins, f, indent=2, ensure_ascii=False)
    print(f"   📄 Written: plugins.json ({len(all_plugins)} total plugins)")

    # 2. repo.json & master.json (The standard CloudStream repository manifests)
    manifest = {
        "name": REPO_NAME,
        "description": REPO_DESCRIPTION,
        "manifestVersion": MANIFEST_VERSION,
        "iconUrl": REPO_ICON,
        "pluginLists": [
            f"{PAGES_BASE_URL}/plugins.json"
        ]
    }

    # Write repo.json
    with open("repo.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print("   📄 Written: repo.json (CloudStream Repository Manifest)")

    # Write master.json (mirrors repo.json so both URLs work seamlessly)
    with open("master.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print("   📄 Written: master.json (Master Manifest as requested)")

    # Write master_bundle.json (Direct standalone list in case needed)
    with open("master_bundle.json", "w", encoding="utf-8") as f:
        json.dump(all_plugins, f, indent=2, ensure_ascii=False)
    print("   📄 Written: master_bundle.json (Standalone Flat Array)")

    # ---------------------------------------------------------------------------
    # SUMMARY REPORT
    # ---------------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("📊 MERGE EXECUTION SUMMARY")
    print("=" * 70)
    for s in stats:
        print(f" • {s['name']:<30} : {s['count']:>3} plugins [{s['status']}]")
    print("-" * 70)
    print(f"📦 Total Plugins Merged      : {len(all_plugins)}")
    print(f"🔁 Duplicate Plugins Preserved: {duplicates_count} (ZERO deleted)")
    print(f"🌐 CloudStream Repo URL      : {PAGES_BASE_URL}/repo.json")
    print(f"🌐 CloudStream Master URL    : {PAGES_BASE_URL}/master.json")
    print("=" * 70)
    print("🎉 All repositories merged successfully into CloudStream master files!")

if __name__ == "__main__":
    fetch_and_merge()
