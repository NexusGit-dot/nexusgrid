
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
            manifest = ast.literal_eval(
                manifest_path.read_text(encoding="utf-8")
            )

            if not isinstance(manifest, dict):
                errors.append("__manifest__.py must contain a Python dictionary.")
            elif not manifest.get("name"):
                errors.append("Manifest is missing the required 'name' field.")
        except (SyntaxError, ValueError) as exc:
            errors.append(f"Invalid manifest syntax: {exc}")

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print(
            "Usage: python scripts/check_addon_structure.py "
            "<addon_directory|addons_directory>"
        )
        return 2

    target_path = Path(sys.argv[1])

    if not target_path.is_dir():
        print(f"Directory does not exist: {target_path}")
        return 1

    if (target_path / "__manifest__.py").is_file():
        addon_paths = [target_path]
    else:
        addon_paths = sorted(
            path
            for path in target_path.iterdir()
            if path.is_dir() and not path.name.startswith(".")
        )

    if not addon_paths:
        print(f"No addon directories found in: {target_path}")
        return 1

    failed = False

    for addon_path in addon_paths:
        errors = check_addon(addon_path)

        if errors:
            failed = True
            print(f"Addon validation failed: {addon_path}")
            for error in errors:
                print(f" - {error}")
        else:
            print(f"Addon structure and manifest syntax are valid: {addon_path}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

