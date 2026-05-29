# create_combined_dataset.py
# Run from the teriip_dashboard/ root folder:
#   python create_combined_dataset.py
#
# Reads all .xlsx files from data/centres/
# Writes combined output to data/combined/Combined_Dataset.xlsx

import os
import pandas as pd
from pathlib import Path

# ── Paths ─────────────────────────────────────────────────────────────────────
ROOT        = Path(__file__).parent                  # teriip_dashboard/
CENTRES_DIR = ROOT / "data" / "centres"              # data/centres/
OUTPUT_DIR  = ROOT / "data" / "combined"             # data/combined/
OUTPUT_FILE = OUTPUT_DIR / "Combined_Dataset.xlsx"

# ── Meta columns (always placed first, in this order) ─────────────────────────
META_COLS = ['File_Name', 'Centre', 'Patient_Name', 'Patient_ID',
             'Age', 'Gender', 'Collection_Date']

# ── Read all centre Excel files ───────────────────────────────────────────────
xlsx_files = sorted(CENTRES_DIR.glob("*.xlsx"))

if not xlsx_files:
    print(f"ERROR: No .xlsx files found in {CENTRES_DIR}")
    exit(1)

print(f"Found {len(xlsx_files)} centre file(s):")
frames = []

for f in xlsx_files:
    try:
        # Read only the first (data) sheet — skip the Errors sheet
        df = pd.read_excel(f, sheet_name=0)
        print(f"  ✓ {f.name:45s}  {len(df)} rows")
        frames.append(df)
    except Exception as e:
        print(f"  ✗ {f.name}  ERROR: {e}")

if not frames:
    print("ERROR: No data could be read. Exiting.")
    exit(1)

# ── Combine ───────────────────────────────────────────────────────────────────
combined = pd.concat(frames, ignore_index=True, sort=False)

# ── Column ordering: meta first, then all parameter columns alphabetically ────
meta_present   = [c for c in META_COLS if c in combined.columns]
param_cols     = sorted(c for c in combined.columns if c not in META_COLS)
combined       = combined[meta_present + param_cols]

# ── Save ──────────────────────────────────────────────────────────────────────
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

with pd.ExcelWriter(OUTPUT_FILE, engine='openpyxl') as writer:

    # ── Sheet 1: All data ──────────────────────────────────────────────────────
    combined.to_excel(writer, sheet_name='All_Patients', index=False)
    ws = writer.sheets['All_Patients']
    for col in ws.columns:
        max_len = max((len(str(cell.value or '')) for cell in col), default=0)
        ws.column_dimensions[col[0].column_letter].width = min(max_len + 2, 30)

    # ── Sheet 2: Summary ───────────────────────────────────────────────────────
    summary = (
        combined.groupby('Centre', dropna=False)
        .agg(
            Patients        = ('Patient_ID', 'count'),
            Params_Captured = ('Centre', lambda x: int(
                combined.loc[x.index, param_cols].notna().sum(axis=1).mean()
            ))
        )
        .reset_index()
    )
    summary.loc[len(summary)] = ['TOTAL', summary['Patients'].sum(), '']
    summary.to_excel(writer, sheet_name='Summary', index=False)

print(f"\n✓ Combined dataset saved → {OUTPUT_FILE}")
print(f"  Total rows   : {len(combined)}")
print(f"  Total columns: {len(combined.columns)}")
print(f"  Centres      : {combined['Centre'].nunique()}")
print(f"\nCentre breakdown:")
for centre, count in combined.groupby('Centre').size().items():
    print(f"  {centre:30s}: {count} patients")