# =============================================================================
# data_loader.py — TERIIP Data Loading & Preprocessing
# =============================================================================

import os
import pandas as pd
import numpy as np
import streamlit as st
from config import STANDARD_PARAMS, CENTRE_METADATA, AGE_BINS, AGE_LABELS

DATA_DIR = os.path.join(os.path.dirname(__file__), "data", "centres")

# Columns that must exist in every centre file (non-parameter)
META_COLS = ["Centre", "Patient_ID", "Age", "Gender"]

# Optional columns we carry if present
OPTIONAL_COLS = ["Patient_Name", "File_Name"]


@st.cache_data(show_spinner="Loading centre datasets…", ttl=0)
def load_master() -> pd.DataFrame:
    """
    Reads every .xlsx file in data/centres/, keeps only standard 55 params
    + meta columns, adds a Centre key, and stacks into one master DataFrame.
    Returns empty DataFrame with correct columns if no files found.
    """
    frames = []

    if not os.path.isdir(DATA_DIR):
        st.warning(f"Data directory not found: {DATA_DIR}")
        return _empty_df()

    files = [f for f in os.listdir(DATA_DIR) if f.endswith(".xlsx")]
    if not files:
        st.warning("No .xlsx files found in data/centres/. Showing demo data.")
        return _demo_data()

    for fname in sorted(files):
        fpath = os.path.join(DATA_DIR, fname)
        try:
            df = pd.read_excel(fpath)
        except Exception as e:
            st.warning(f"Could not read {fname}: {e}")
            continue

        # ── Derive Centre key ────────────────────────────────────────────────
        # Use 'Centre' column if present, else derive from filename
        if "Centre" in df.columns:
            centre_key = df["Centre"].iloc[0] if len(df) > 0 else fname.replace(".xlsx", "")
        else:
            centre_key = fname.replace(".xlsx", "")

        df["Centre"] = centre_key

        # ── Rename Excel columns to standard param names ─────────────────────
        RENAME_MAP = {
            # CBC
            "Haemoglobin": "Hb", "Hb": "Hb",
            "Platelet Count": "Platelet_Count", "Platelet_Count": "Platelet_Count",
            "Reticulocyte Count": "Reticulocyte_Count", "Reticulocyte_Count": "Reticulocyte_Count",
            "Neutrophils": "Neutrophil", "Neutrophil": "Neutrophil",
            "Lymphocytes": "Lymphocyte", "Lymphocyte": "Lymphocyte",
            "Monocytes": "Monocyte", "Monocyte": "Monocyte",
            "Eosinophils": "Eosinophil", "Eosinophil": "Eosinophil",
            "Basophils": "Basophil", "Basophil": "Basophil",
            "WBC": "TLC",
            "Abs Neutrophil Count": "Abs_Neutrophil", "Abs_Neutrophil": "Abs_Neutrophil",
            "Abs Basophil Count": "Abs_Basophil", "Abs_Basophil": "Abs_Basophil",
            "Abs Eosinophil Count": "Abs_Eosinophil", "Abs_Eosinophil": "Abs_Eosinophil",
            "Abs Lymphocyte Count": "Abs_Lymphocyte", "Abs_Lymphocyte": "Abs_Lymphocyte",
            "Abs Monocyte Count": "Abs_Monocyte", "Abs_Monocyte": "Abs_Monocyte",
            # LFT
            "Bilirubin_Total": "Total_Bilirubin", "Total Bilirubin": "Total_Bilirubin",
            "Bilirubin_Direct": "Direct_Bilirubin", "Direct Bilirubin": "Direct_Bilirubin",
            "Indirect Bilirubin": "Indirect_Bilirubin",
            "Total_Protein": "Total_Protein", "Total Protein": "Total_Protein",
            # KFT
            "Uric_Acid": "Uric_Acid", "Uric Acid": "Uric_Acid",
            # Glucose
            "Glucose_Fasting": "Glucose", "Glucose": "Glucose",
            # Lipid
            "Total_Cholesterol": "Total_Cholesterol", "Total Cholesterol": "Total_Cholesterol",
            "LDL": "LDL_Cholesterol", "LDL Cholesterol": "LDL_Cholesterol",
            "HDL": "HDL_Cholesterol", "HDL Cholesterol": "HDL_Cholesterol",
            "Triglycerides": "Triglyceride", "Triglyceride": "Triglyceride",
            # Thyroid
            "T3_Total": "Total_T3", "Total T3": "Total_T3",
            "FT3": "Free_T3", "Free T3": "Free_T3",
            "T4_Total": "Total_T4", "Total T4": "Total_T4",
            "FT4": "Free_T4", "Free T4": "Free_T4",
            "Anti_Thyroglobulin": "Thyroglobulin_Ab", "Thyroglobulin Ab": "Thyroglobulin_Ab",
            "Anti_TPO": "TPO", "TPO": "TPO",
            # Iron & Haematinics
            "TFR_Saturation": "Transferrin_Saturation", "Transferrin Saturation": "Transferrin_Saturation",
            "Vitamin_B12": "Vitamin_B12", "Vitamin B12": "Vitamin_B12",
            # Vitamins & Minerals
            "Vitamin_D": "Vitamin_D", "Vitamin D": "Vitamin_D",
            # Special
            "Blood Group": "Blood_Group",
        }
        df.rename(columns=RENAME_MAP, inplace=True)

        # ── Keep only standard 66 params (fill missing with NaN) ─────────────
        # ── Keep only standard 66 params (fill missing with NaN) ─────────────
        # ── Keep only standard 67 params (fill missing with NaN) ─────────────
        CATEGORICAL_PARAMS = ["Blood_Group", "PBS"]
        for p in STANDARD_PARAMS:
            if p not in df.columns:
                df[p] = np.nan
            elif p in CATEGORICAL_PARAMS:
                # Keep as-is — text values like A+, B+, Normal are valid
                df[p] = df[p].replace([".", "-", "N/A", "NA", "na", "n/a", " ", ""], np.nan)
            else:
                # Force numeric, coerce bad placeholders to NaN
                df[p] = pd.to_numeric(df[p].replace([".", "-", "N/A", "NA", "na", "n/a", " "], np.nan), errors="coerce")
                
        # ── Build output row with meta + params only ─────────────────────────
        keep = ["Centre"]
        for c in ["Patient_ID", "Age", "Gender"]:
            if c in df.columns:
                keep.append(c)
            else:
                df[c] = np.nan
                keep.append(c)

        keep += STANDARD_PARAMS
        frames.append(df[keep].copy())

    if not frames:
        return _demo_data()

    master = pd.concat(frames, ignore_index=True)

    # ── Post-processing ──────────────────────────────────────────────────────
    master["Age"] = pd.to_numeric(master["Age"], errors="coerce")
    master["Age_Group"] = pd.cut(
        master["Age"], bins=AGE_BINS, labels=AGE_LABELS, right=True
    )
    master["Gender"] = master["Gender"].astype(str).str.strip().str.title()
    master["Gender"] = master["Gender"].replace({"Nan": "Unknown", "": "Unknown"})

    # Attach region from metadata
    master["Region"] = master["Centre"].map(
        lambda c: CENTRE_METADATA.get(c, {}).get("region", "Unknown")
    )
    master["Display_Name"] = master["Centre"].map(
        lambda c: CENTRE_METADATA.get(c, {}).get("display_name", c)
    )

    return master

@st.cache_data(ttl=0)
def get_centre_summary(master: pd.DataFrame) -> pd.DataFrame:
    """
    Builds a per-centre summary table with target, achieved, completion %.
    Merges with CENTRE_METADATA.
    """
    achieved = master.groupby("Centre").size().reset_index(name="Achieved")

    rows = []
    for centre_key, meta in CENTRE_METADATA.items():
        ach = achieved.loc[achieved["Centre"] == centre_key, "Achieved"].values
        ach_val = int(ach[0]) if len(ach) > 0 else 0
        target = meta.get("target", 200)
        rows.append(
            {
                "Centre": meta["display_name"],
                "Centre_Key": centre_key,
                "Region": meta["region"],
                "State": meta["state"],
                "NABL_Biochem": "✅ Yes" if meta.get("nabl_biochem", False) else "❌ No",
                "NABL_Haem":    "✅ Yes" if meta.get("nabl_haem", False) else "❌ No",
                "DOS": meta["dos"],
                "Target": target,
                "Achieved": ach_val,
                "Completion_%": round(ach_val / target * 100, 1) if target > 0 else 0,
                "lat": meta["lat"],
                "lon": meta["lon"],
            }
        )
    return pd.DataFrame(rows)


def get_param_availability(master: pd.DataFrame) -> pd.DataFrame:
    """
    Returns a DataFrame of shape (55, n_centres+1) showing
    % of non-null values for each parameter per centre.
    """
    rows = []
    for p in STANDARD_PARAMS:
        row = {"Parameter": p}
        for centre in master["Centre"].unique():
            sub = master[master["Centre"] == centre][p]
            row[centre] = round(sub.notna().mean() * 100, 1)
        row["Overall"] = round(master[p].notna().mean() * 100, 1)
        rows.append(row)
    return pd.DataFrame(rows)


# ── Demo / fallback data ──────────────────────────────────────────────────────

def _empty_df() -> pd.DataFrame:
    cols = ["Centre", "Patient_ID", "Age", "Gender", "Age_Group", "Region", "Display_Name"] + STANDARD_PARAMS
    return pd.DataFrame(columns=cols)


def _demo_data() -> pd.DataFrame:
    """Generates synthetic data for all 15 centres so the dashboard renders."""
    np.random.seed(42)
    frames = []
    for centre_key, meta in CENTRE_METADATA.items():
        n = np.random.randint(80, 180)
        df = pd.DataFrame({"Centre": centre_key, "Patient_ID": [f"{centre_key[:3].upper()}{i:04d}" for i in range(n)]})
        df["Age"] = np.random.randint(18, 75, n)
        df["Gender"] = np.random.choice(["Male", "Female"], n, p=[0.48, 0.52])
        # Simulate each parameter with realistic ranges + ~10-20% missingness
        ranges = {
            "Hb": (8, 17), "PCV": (25, 52), "TRBC": (3.5, 6.0),
            "MCV": (70, 100), "MCH": (22, 34), "MCHC": (30, 37), "RDW": (11, 18),
            "TLC": (3000, 12000), "Neutrophil": (40, 80), "Lymphocyte": (15, 45),
            "Monocyte": (2, 10), "Eosinophil": (0, 8), "Basophil": (0, 2),
            "Platelet_Count": (100000, 400000), "MPV": (7, 13),
            "Abs_Neutrophil": (1500, 8000), "Abs_Basophil": (0, 100),
            "Abs_Eosinophil": (0, 500), "Abs_Lymphocyte": (1000, 4000),
            "Abs_Monocyte": (200, 1000), "Reticulocyte_Count": (0.5, 2.5),
            "Total_Bilirubin": (0.2, 2.0), "Direct_Bilirubin": (0.05, 0.8),
            "Indirect_Bilirubin": (0.1, 1.2),
            "ALT": (10, 100), "AST": (10, 100), "ALP": (40, 200),
            "Total_Protein": (5.5, 9.0), "Albumin": (3.0, 5.5), "GGT": (10, 120),
            "Urea": (10, 60), "Creatinine": (0.5, 2.5), "Uric_Acid": (2, 9),
            "Sodium": (130, 150), "Potassium": (3.0, 6.0), "Chloride": (95, 115),
            "Glucose": (70, 200), "HbA1c": (4, 12),
            "Total_Cholesterol": (120, 280), "LDL_Cholesterol": (50, 200),
            "HDL_Cholesterol": (30, 90), "Triglyceride": (60, 400),
            "TSH": (0.1, 8.0), "Total_T3": (0.8, 2.5), "Free_T3": (1.5, 6.0),
            "Total_T4": (5, 14), "Free_T4": (0.7, 2.0),
            "Thyroglobulin_Ab": (0, 500), "TPO": (0, 600),
            "Amylase": (20, 160), "Lipase": (10, 100),
            "Calcium": (8, 11), "Phosphorus": (2, 5),
            "Iron": (40, 180), "Ferritin": (5, 300),
            "Transferrin_Saturation": (10, 50), "TIBC": (250, 450),
            "Vitamin_B12": (100, 1000), "Folate": (2, 20), "Vitamin_D": (5, 100),
            "Copper": (70, 140), "Magnesium": (1.5, 3.0), "Zinc": (50, 150),
            "CRP": (0, 50), "ESR": (1, 80),
            "Blood_Group": (1, 4),   # dummy numeric for demo only
            "PBS": (0, 1),           # dummy numeric for demo only
        }
        miss_prob = np.random.uniform(0.05, 0.20)
        for p in STANDARD_PARAMS:
            lo, hi = ranges.get(p, (0, 100))
            vals = np.random.uniform(lo, hi, n).astype(float)
            mask = np.random.random(n) < miss_prob
            vals[mask] = np.nan
            df[p] = vals
        frames.append(df)

    master = pd.concat(frames, ignore_index=True)
    master["Age"] = pd.to_numeric(master["Age"], errors="coerce")
    master["Age_Group"] = pd.cut(master["Age"], bins=AGE_BINS, labels=AGE_LABELS, right=True)
    master["Gender"] = master["Gender"].astype(str).str.strip().str.title()
    master["Region"] = master["Centre"].map(lambda c: CENTRE_METADATA.get(c, {}).get("region", "Unknown"))
    master["Display_Name"] = master["Centre"].map(lambda c: CENTRE_METADATA.get(c, {}).get("display_name", c))
    return master
