# CloudStream Master Unified Repo

Automated multi-source CloudStream 3 extension repository automatically synced and merged using GitHub Actions.

![Build Status](https://github.com/tat2027/repo14/actions/workflows/build.yml/badge.svg)

---

## 📱 How to Add to CloudStream

1. Open **CloudStream 3** on your Android device or Android TV.
2. Go to **Settings** (Gear icon) -> **Extensions**.
3. Tap **Add Repository**.
4. Enter either of these URLs:
   - **Repository URL:** `https://tat2027.github.io/repo14/repo.json`
   - **Master JSON URL:** `https://tat2027.github.io/repo14/master.json`
5. Tap **Download**. All extensions will immediately appear ready to install!

---

## ⚡ Unified Source Repositories Included

This repository automatically merges all of the following extension sources:

- **CSX (SaurabhKaperwan)**: `https://raw.githubusercontent.com/SaurabhKaperwan/CSX/builds/CS.json`
- **Phisher Repo**: `https://raw.githubusercontent.com/phisher98/cloudstream-extensions-phisher/refs/heads/builds/repo.json`
- **CNC Repo (All Language)**: `https://raw.githubusercontent.com/NivinCNC/CNCVerse-Cloud-Stream-Extension/refs/heads/builds/CNC.json`
- **Cinephile**: `https://raw.githubusercontent.com/rockhero1234/cinephile/refs/heads/builds/repo.json`
- **raghav repo**: `https://raw.githubusercontent.com/KSHITIJ8473/raghav/builds/repo.json`
- **AllForU**: `https://raw.githubusercontent.com/RVRBEAST76/allforu-repo/builds/repo.json`
- **FLUMMOX Repo**: `https://raw.githubusercontent.com/FlummoxGamer/FLUMMOX-Repo/builds/repo.json`
- **Desi Extensions**: `https://raw.githubusercontent.com/Faisal0786/Desi/main/repo.json`
- **NetMirror**: `https://raw.githubusercontent.com/Sushan64/NetMirror-Extension/refs/heads/builds/Netflix.json`
- **XtronRepo**: `https://raw.githubusercontent.com/MrXtron/CloudStream-Extension/refs/heads/builds/repo.json`
- **Eclipsia**: `https://cs.eclipsia.dpdns.org/repo.json`

---

## 🛡️ Duplicate Handling ("duplicate any dena plugins delete nhi karni")

- **Zero Plugin Deletion**: No plugins are ever filtered out or deleted.
- If multiple repositories provide the same extension (e.g., Bollyflix, CineStream, VegaMovies), both versions are preserved.
- Under **disambiguate mode**, duplicate extensions are tagged with their source name (e.g. `Bollyflix [CSX]` and `Bollyflix [XtronRepo]`) so CloudStream displays both in the app UI, allowing you to install either provider.

---

## ⏰ Automated Updates

GitHub Actions automatically runs `merge.py` **every 6 hours** using cron schedule (`0 */6 * * *`) and whenever you click **Run workflow** in the GitHub Actions tab.
