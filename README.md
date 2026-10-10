# Finish PHQ Lot Report

A Streamlit dashboard for reviewing Finish PHQ lots.

## Run locally

Install dependencies and start the app with `uv`:

```powershell
uv sync
uv run streamlit run streamlit_app.py
```

By default, the dashboard reads `data/Finish_PHQ_lot.csv`. To read the live internal share instead, set `PHQ_CSV_PATH` before starting Streamlit:

```powershell
$env:PHQ_CSV_PATH = '\\azATSHFS.intel.com\azATAnalysis$\MAOATM\CDAT\zhaohua\Finish_PHQ_lot.csv'
uv run streamlit run streamlit_app.py
```

## Refresh the Streamlit Cloud snapshot

Run `sync_phq_data.bat` on a Windows machine that can access the internal share and push to this GitHub repository. It copies the CSV into `data/`, commits that file, and pushes the change; Streamlit Cloud then redeploys from the updated repository. Use Windows Task Scheduler to run the batch file on the desired schedule, under an account with both share read access and Git push access.

**Data access:** The sync publishes the full CSV to this repository. Confirm that its visibility and contents are approved before running it. Each version remains in Git history even after later updates or file removal.
