import tempfile
import unittest
from pathlib import Path

from scripts.check_addon_structure import check_addon


class TestAddonStructure(unittest.TestCase):
    def test_missing_manifest_is_reported(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            addon_path = Path(temp_dir)
            (addon_path / "__init__.py").touch()

            errors = check_addon(addon_path)

            self.assertIn(
                "Missing required file: __manifest__.py",
                errors,
            )


if __name__ == "__main__":
    unittest.main()
