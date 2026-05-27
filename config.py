# =============================================================================
# config.py — TERIIP Dashboard Static Configuration
# =============================================================================

# ── 66 Standard Parameters ────────────────────────────────────────────────────
STANDARD_PARAMS = [
    # CBC
    "Hb", "PCV", "TRBC", "MCV", "MCH", "MCHC", "RDW",
    "TLC", "Neutrophil", "Lymphocyte", "Monocyte", "Eosinophil", "Basophil",
    "Platelet_Count", "MPV",
    "Abs_Neutrophil", "Abs_Basophil", "Abs_Eosinophil", "Abs_Lymphocyte", "Abs_Monocyte",
    "Reticulocyte_Count",
    # LFT
    "Total_Bilirubin", "Direct_Bilirubin", "Indirect_Bilirubin",
    "ALT", "AST", "ALP", "Total_Protein", "Albumin", "GGT",
    # KFT
    "Urea", "Creatinine", "Uric_Acid", "Sodium", "Potassium", "Chloride",
    # Glucose & Diabetes
    "Glucose", "HbA1c",
    # Lipid
    "Total_Cholesterol", "LDL_Cholesterol", "HDL_Cholesterol", "Triglyceride",
    # Thyroid
    "TSH", "Total_T3", "Free_T3", "Total_T4", "Free_T4",
    "Thyroglobulin_Ab", "TPO",
    # Pancreatic
    "Amylase", "Lipase",
    # Minerals & Vitamins
    "Calcium", "Phosphorus", "Iron", "Ferritin",
    "Transferrin_Saturation", "TIBC",
    "Vitamin_B12", "Folate", "Vitamin_D",
    "Copper", "Magnesium", "Zinc",
    # Inflammatory
    "CRP", "ESR",
    # Special / Categorical
    "Blood_Group", "PBS",
]

# ── Parameter Groups ──────────────────────────────────────────────────────────
PARAM_GROUPS = {
    "Complete Blood Count (CBC)": [
        "Hb", "PCV", "TRBC", "MCV", "MCH", "MCHC", "RDW",
        "TLC", "Neutrophil", "Lymphocyte", "Monocyte", "Eosinophil", "Basophil",
        "Platelet_Count", "MPV",
        "Abs_Neutrophil", "Abs_Basophil", "Abs_Eosinophil", "Abs_Lymphocyte", "Abs_Monocyte",
        "Reticulocyte_Count",
    ],
    "Liver Function Test (LFT)": [
        "Total_Bilirubin", "Direct_Bilirubin", "Indirect_Bilirubin",
        "ALT", "AST", "ALP", "Total_Protein", "Albumin", "GGT",
    ],
    "Kidney Function Test (KFT)": [
        "Urea", "Creatinine", "Uric_Acid", "Sodium", "Potassium", "Chloride",
    ],
    "Glucose & Diabetes": [
        "Glucose", "HbA1c",
    ],
    "Lipid Profile": [
        "Total_Cholesterol", "LDL_Cholesterol", "HDL_Cholesterol", "Triglyceride",
    ],
    "Thyroid Profile": [
        "TSH", "Total_T3", "Free_T3", "Total_T4", "Free_T4",
        "Thyroglobulin_Ab", "TPO",
    ],
    "Pancreatic": [
        "Amylase", "Lipase",
    ],
    "Iron & Haematinics": [
        "Iron", "Ferritin", "Transferrin_Saturation", "TIBC",
        "Vitamin_B12", "Folate",
    ],
    "Vitamins & Minerals": [
        "Vitamin_D", "Calcium", "Phosphorus", "Copper", "Magnesium", "Zinc",
    ],
    "Inflammatory Markers": [
        "CRP", "ESR",
    ],
    "Special Tests": [
        "Blood_Group", "PBS",
    ],
}

# ── Centre Metadata ───────────────────────────────────────────────────────────
# Keys MUST exactly match the value in the 'Centre' column of each Excel file.
# targets/dos/nabl — update these to actual values from your records.
CENTRE_METADATA = {
    "AIIMS_Jodhpur": {
        "display_name": "AIIMS Jodhpur",
        "city": "Jodhpur",
        "state": "Rajasthan",
        "region": "West",
        "lat": 26.2389,
        "lon": 73.0243,
        "nabl_biochem": True,
        "nabl_haem": False,
        "dos": "2025-09-02",
        "target": 400,
    },
    "AIIMS_Bhatinda": {
        "display_name": "AIIMS Bathinda",
        "city": "Bathinda",
        "state": "Punjab",
        "region": "North",
        "lat": 30.2110,
        "lon": 74.9455,
        "nabl_biochem": True,
        "nabl_haem": True,
        "dos": "2025-06-30",
        "target": 400,
    },
    "AIIMS_Bhopal": {
        "display_name": "AIIMS Bhopal",
        "city": "Bhopal",
        "state": "Madhya Pradesh",
        "region": "Central",
        "lat": 23.1981,
        "lon": 77.3271,
        "nabl_biochem": False,
        "nabl_haem": True,
        "dos": "2025-07-07",
        "target": 300,
    },
    "AIIMS_Raipur": {
        "display_name": "AIIMS Raipur",
        "city": "Raipur",
        "state": "Chhattisgarh",
        "region": "Central",
        "lat": 21.2514,
        "lon": 81.6296,
        "nabl_biochem": True,
        "nabl_haem": False,
        "dos": "2025-07-10",
        "target": 600,
    },
    "Amrita_Kochi": {
        "display_name": "Amrita Hospital Kochi",
        "city": "Kochi",
        "state": "Kerala",
        "region": "South",
        "lat": 10.0261,
        "lon": 76.3083,
        "nabl_biochem": True,
        "nabl_haem": True,
        "dos": "2025-05-26",
        "target": 200,
    },
    "Gleneagles_Chennai": {
        "display_name": "NIRRH Port Blair",
        "city": "Port Blair",
        "state": "Andaman & Nicobar Islands",
        "region": "Others",
        "lat": 11.6234,
        "lon": 92.7265,
        "nabl_biochem": True,
        "nabl_haem": True,
        "dos": "2025-09-18",
        "target": 300,
    },
    "JSS_Mysore": {
        "display_name": "JSS Hospital Mysuru",
        "city": "Mysuru",
        "state": "Karnataka",
        "region": "South",
        "lat": 12.2958,
        "lon": 76.6394,
        "nabl_biochem": True,
        "nabl_haem": True,
        "dos": "2025-08-05",
        "target": 300,
    },
    "KIMS_Bhubaneswar": {
        "display_name": "KIMS Bhubaneswar",
        "city": "Bhubaneswar",
        "state": "Odisha",
        "region": "East",
        "lat": 20.2961,
        "lon": 85.8245,
        "nabl_biochem": True,
        "nabl_haem": True,
        "dos": "2025-07-01",
        "target": 200,
    },
    "KMC_Manipal": {
        "display_name": "KMC Manipal",
        "city": "Manipal",
        "state": "Karnataka",
        "region": "South",
        "lat": 13.3516,
        "lon": 74.7843,
        "nabl_biochem": True,
        "nabl_haem": True,
        "dos": "2025-06-10",
        "target": 600,
    },
    "PD_Hinduja_Mumbai": {
        "display_name": "P D Hinduja Hospital Mumbai",
        "city": "Mumbai",
        "state": "Maharashtra",
        "region": "West",
        "lat": 19.0596,
        "lon": 72.8295,
        "nabl_biochem": True,
        "nabl_haem": True,
        "dos": "2025-07-27",
        "target": 400,
    },
    "AIIMS_Delhi": {
        "display_name": "AIIMS Delhi",
        "city": "New Delhi",
        "state": "Delhi",
        "region": "North",
        "lat": 28.5672,
        "lon": 77.2100,
        "nabl_biochem": True,
        "nabl_haem": True,
        "dos": "2025-09-02",
        "target": 400,
    },
    "AIIMS_Kalyani": {
        "display_name": "AIIMS Kalyani",
        "city": "Kalyani",
        "state": "West Bengal",
        "region": "East",
        "lat": 22.9750,
        "lon": 88.4344,
        "nabl_biochem": True,
        "nabl_haem": True,
        "dos": "2025-07-23",
        "target": 500,
    },
    "AIIMS_Guwahati": {
        "display_name": "AIIMS Guwahati",
        "city": "Guwahati",
        "state": "Assam",
        "region": "North-East",
        "lat": 26.1445,
        "lon": 91.7362,
        "nabl_biochem": False,
        "nabl_haem": False,
        "dos": "2025-07-31",
        "target": 300,
    },
    "DrBBCI_Guwahati": {
        "display_name": "Dr BBCI Guwahati",
        "city": "Guwahati",
        "state": "Assam",
        "region": "North-East",
        "lat": 26.1890,
        "lon": 91.7458,
        "nabl_biochem": True,
        "nabl_haem": True,
        "dos": "2025-08-05",
        "target": 600,
    },
    "KGMU_Lucknow": {
        "display_name": "KGMU Lucknow",
        "city": "Lucknow",
        "state": "Uttar Pradesh",
        "region": "North",
        "lat": 26.9124,
        "lon": 80.9842,
        "nabl_biochem": True,
        "nabl_haem": True,
        "dos": "2025-08-22",
        "target": 625,
    },
    "PGIMER_Chandigarh": {
        "display_name": "PGIMER Chandigarh",
        "city": "Chandigarh",
        "state": "Punjab",
        "region": "North",
        "lat": 30.7650,
        "lon": 76.7788,
        "nabl_biochem": False,
        "nabl_haem": False,
        "dos": "2025-07-09",
        "target": 600,
    },
}

# ── Age Bins ──────────────────────────────────────────────────────────────────
AGE_BINS = [18, 25,35, 45, 60, 70, 120]
AGE_LABELS = ["18–25", "26–35", "36–45", "46–60", "61-70", "70+"]
