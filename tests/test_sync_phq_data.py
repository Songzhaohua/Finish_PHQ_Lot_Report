import tempfile
import unittest
from pathlib import Path

from sync_phq_data import refresh_local_snapshot


class RefreshPHQSnapshotTests(unittest.TestCase):
	def test_refresh_local_snapshot_copies_source_file(self):
		with tempfile.TemporaryDirectory() as temp_dir:
			temp_path = Path(temp_dir)
			source = temp_path / "source.csv"
			destination = temp_path / "data" / "snapshot.csv"
			source.write_text("LOT,QUANTITY\nA,10\n", encoding="utf-8")

			ok, message = refresh_local_snapshot(source, destination)

			self.assertTrue(ok)
			self.assertEqual(
				destination.read_text(encoding="utf-8"), "LOT,QUANTITY\nA,10\n"
			)
			self.assertIn("Copied", message)

	def test_refresh_local_snapshot_reports_missing_source(self):
		with tempfile.TemporaryDirectory() as temp_dir:
			temp_path = Path(temp_dir)
			source = temp_path / "missing.csv"
			destination = temp_path / "data" / "snapshot.csv"

			ok, message = refresh_local_snapshot(source, destination)

			self.assertFalse(ok)
			self.assertIn("Source CSV not found", message)
			self.assertFalse(destination.exists())


if __name__ == "__main__":
	unittest.main()