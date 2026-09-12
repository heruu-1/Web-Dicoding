"""Run: python scripts/package_submission.py (standard library only)."""

from datetime import datetime
from pathlib import Path
import shutil
import tempfile
import zipfile


ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "submission-jelajah-lampung.zip"


def main():
    # Explicit allowlist: no Git files, scripts, backups, or nested ZIPs.
    files = [ROOT / "index.html"]
    for folder, extensions in (
        ("images", {".jpg", ".jpeg", ".png"}),
        ("styles", {".css"}),
        ("scripts", {".js"}),
    ):
        files.extend(sorted(
            path for path in (ROOT / "assets" / folder).iterdir()
            if path.is_file() and path.suffix.lower() in extensions
        ))
    expected = {path.relative_to(ROOT).as_posix() for path in files}
    assert "assets/styles/style.css" in expected
    assert "assets/scripts/main.js" in expected
    assert "assets/images/siger-primary.jpg" in expected
    assert "assets/images/siger-fallback.jpg" in expected

    with tempfile.TemporaryDirectory(prefix="submission-", dir=ROOT) as temp:
        candidate = Path(temp) / OUTPUT.name
        with zipfile.ZipFile(candidate, "w", zipfile.ZIP_DEFLATED) as archive:
            for path in files:
                # ZIP paths must use '/', regardless of the host OS.
                archive.write(path, arcname=path.relative_to(ROOT).as_posix())
        with zipfile.ZipFile(candidate) as archive:
            names = [entry.orig_filename for entry in archive.infolist()]
            assert set(names) == expected
            assert all("\\" not in name for name in names)
            assert sum(name.split("/")[-1] == "index.html" for name in names) == 1
            assert archive.testzip() is None
            for path in files:
                assert archive.read(path.relative_to(ROOT).as_posix()) == path.read_bytes()

        if OUTPUT.exists():
            backups = ROOT / ".review" / "backups"
            backups.mkdir(parents=True, exist_ok=True)
            stamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
            shutil.copy2(OUTPUT, backups / f"submission-{stamp}.zip")
        candidate.replace(OUTPUT)
    print(f"Verified {len(files)} files with portable ZIP paths: {OUTPUT}")


if __name__ == "__main__":
    main()
