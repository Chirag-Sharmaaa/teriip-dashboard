# TERIIP Dashboard — Setup & Run Guide

## Folder Structure

```
teriip_dashboard/
├── app.py              ← Main Streamlit app (run this)
├── config.py           ← Parameters, groups, centre metadata
├── data_loader.py      ← Reads & merges all centre Excel files
├── requirements.txt
└── data/
    └── centres/
        ├── AIIMS_Jodhpur_Dataset.xlsx
        ├── AIIMS_Delhi_Dataset.xlsx
        └── ... (one .xlsx per centre)
```

## Step 1 — Place your Excel files

Copy all 15 centre Excel files into:
```
teriip_dashboard/data/centres/
```

The filename should match or contain the Centre key from config.py
(e.g., `AIIMS_Jodhpur_Dataset.xlsx`). The loader reads the `Centre`
column inside the file to identify the centre — filename doesn't matter
as long as it ends in `.xlsx`.

**If no files are placed**, the dashboard will auto-generate synthetic
demo data for all 15 centres so you can see the full layout immediately.

## Step 2 — Create virtual environment (do once)

```bash
cd teriip_dashboard
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

## Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

## Step 4 — Run the dashboard

```bash
streamlit run app.py
```

Opens at: http://localhost:8501

## Step 5 — Update centre metadata (important)

Open `config.py` and edit the `CENTRE_METADATA` dictionary:
- Set correct `target` per centre (default is 200)
- Set `nabl: True/False` for each centre
- Set `dos` (date of start) as "YYYY-MM-DD"
- Verify `lat`/`lon` coordinates (approximate values already filled)
- Update centre keys to match the `Centre` column in your Excel files

## Notes

- The `Centre` column in your Excel must match a key in `CENTRE_METADATA`
  exactly (e.g., `"AIIMS_Jodhpur"`) for map/metadata to work correctly.
- Parameters missing from a centre's file are filled with NaN automatically.
- Extra columns beyond the 55 standard + meta columns are ignored.
- Filters in the sidebar (Region, Centre) update all sections live.
