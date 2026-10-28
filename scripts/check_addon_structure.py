import ast
import sys
from pathlib import Path


def check_addon(addon_path: Path) -> list[str]:
    errors = []

    if not addon_path.is_dir():
        return [f"Addon directory does not exist: {addon_path}"]

    manifest_path = addon_path / "__manifest__.py"
    init_path = addon_path / "__init__.py"

    if not manifest_path.is_file():
        errors.append("Missing required file: __manifest__.py")

    if not init_path.is_file():
        errors.append("Missing required file: __init__.py")

    if manifest_path.is_file():
        try:
            manifest = ast.literal_eval(manifest_path.read_text(encoding="utf-8"))

            if not isinstance(manifest, dict):
                errors.append("__manifest__.py must contain a Python dictionary.")
            elif not manifest.get("name"):
                errors.append("Manifest is missing the required 'name' field.")
        except (SyntaxError, ValueError) as exc:
            errors.append(f"Invalid manifest syntax: {exc}")

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python scripts/check_addon_structure.py <addon_directory>")
        return 2

    addon_path = Path(sys.argv[1])
    errors = check_addon(addon_path)

    if errors:
        print(f"Addon validation failed: {addon_path}")
        for error in errors:
            print(f" - {error}")
        return 1

    print(f"Addon structure and manifest syntax are valid: {addon_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
