"""Refresh the PHQ snapshot from the internal share and push it to GitHub."""
import shutil
import subprocess
import sys
from pathlib import Path


SOURCE_PATH = r"\\azATSHFS.intel.com\azATAnalysis$\MAOATM\CDAT\zhaohua\Finish_PHQ_lot.csv"
REPO_DIR = Path(__file__).parent
DEST_PATH = REPO_DIR / "data" / "Finish_PHQ_lot.csv"


def refresh_local_snapshot(
	source_path: str | Path = SOURCE_PATH,
	destination_path: str | Path = DEST_PATH,
) -> tuple[bool, str]:
	"""Copy the live CSV into the repository snapshot path."""
	source = Path(source_path)
	destination = Path(destination_path)

	try:
		destination.parent.mkdir(parents=True, exist_ok=True)
		shutil.copyfile(source, destination)
	except FileNotFoundError:
		return False, f"Source CSV not found: {source}"
	except OSError as exc:
		return False, f"Could not copy CSV from {source} to {destination}: {exc}"

	return True, f"Copied CSV from {source} to {destination}."


def run_git(*args: str) -> None:
	subprocess.run(["git", *args], cwd=REPO_DIR, check=True)


def main() -> None:
	ok, message = refresh_local_snapshot()
	if not ok:
		print(message, file=sys.stderr)
		sys.exit(1)

	print(message)
	snapshot_path = str(DEST_PATH.relative_to(REPO_DIR))
	run_git("add", "--", snapshot_path)
	result = subprocess.run(
		["git", "diff", "--cached", "--quiet", "--", snapshot_path],
		cwd=REPO_DIR,
	)
	if result.returncode == 0:
		print("No data changes since last sync; nothing to push.")
		return

	run_git("commit", "--only", "-m", "Sync Finish PHQ lot data snapshot", "--", snapshot_path)
	run_git("push")
	print("PHQ data snapshot synced and pushed.")


if __name__ == "__main__":
	main()