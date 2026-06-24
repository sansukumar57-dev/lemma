"""Package the Microsoft Teams app manifest bundle."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest-dir",
        type=Path,
        default=Path("manifests/teams"),
        help="Directory containing manifest.json and referenced icon files.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output zip path. Defaults to <manifest-dir>/lemma-teams.zip.",
    )
    parser.add_argument(
        "--app-short-name",
        help="Override manifest name.short in the packaged zip only.",
    )
    parser.add_argument(
        "--app-full-name",
        help="Override manifest name.full in the packaged zip only.",
    )
    parser.add_argument(
        "--color-icon",
        type=Path,
        help="Override the packaged color icon file.",
    )
    parser.add_argument(
        "--outline-icon",
        type=Path,
        help="Override the packaged outline icon file.",
    )
    return parser.parse_args()


def _manifest_bytes(
    manifest_path: Path,
    *,
    app_short_name: str | None,
    app_full_name: str | None,
) -> bytes:
    if app_short_name is None and app_full_name is None:
        return manifest_path.read_bytes()

    manifest = json.loads(manifest_path.read_text())
    name = manifest.setdefault("name", {})
    if app_short_name is not None:
        name["short"] = app_short_name
    if app_full_name is not None:
        name["full"] = app_full_name
    return (json.dumps(manifest, indent=2) + "\n").encode()


def main() -> None:
    args = _parse_args()
    manifest_dir = args.manifest_dir
    manifest_path = manifest_dir / "manifest.json"
    output_path = args.output or manifest_dir / "lemma-teams.zip"

    manifest = json.loads(manifest_path.read_text())
    icons = [
        (args.color_icon or manifest_dir / manifest["icons"]["color"], manifest["icons"]["color"]),
        (
            args.outline_icon or manifest_dir / manifest["icons"]["outline"],
            manifest["icons"]["outline"],
        ),
    ]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output_path, "w", compression=ZIP_DEFLATED) as archive:
        archive.writestr(
            "manifest.json",
            _manifest_bytes(
                manifest_path,
                app_short_name=args.app_short_name,
                app_full_name=args.app_full_name,
            ),
        )
        for icon_path, archive_name in icons:
            archive.write(icon_path, archive_name)

    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
