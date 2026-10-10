@echo off
REM Copies the live PHQ CSV into the repository and pushes the updated snapshot.
cd /d "%~dp0"
python sync_phq_data.py