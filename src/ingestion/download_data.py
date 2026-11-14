
import subprocess
from pathlib import Path
from zipfile import ZipFile


# ==========================================
# CONFIGURATIONS
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

COMPETITION = "porto-seguro-safe-driver-prediction"

RAW_PATH = PROJECT_ROOT / "data" / "raw" / "porto_seguro"

EXPECTED_FILES = [
    "train.csv",
    "test.csv",
    "sample_submission.csv"
]


# ==========================================
# DOWNLOAD
# ==========================================

def download_data():
    """Download competition data using Kaggle CLI."""

    RAW_PATH.mkdir(parents=True, exist_ok=True)

    zip_path = RAW_PATH / f"{COMPETITION}.zip"

    if zip_path.exists():
        print("ZIP file already exists. Skipping download.")
        return zip_path

    command = [
        "kaggle",
        "competitions",
        "download",
        "-c", COMPETITION,
        "-p", str(RAW_PATH)
    ]

    print("Downloading competition data...")

    subprocess.run(command, check=True)

    if not zip_path.exists():
        raise FileNotFoundError(
            f"Download ZIP not found: {zip_path}"
        )

    print("Download completed!")

    return zip_path


# ==========================================
# EXTRACTION
# ==========================================

def extract_data(zip_path):
    """Extract downloaded competition files."""

    with ZipFile(zip_path, "r") as archive:
        archive.extractall(RAW_PATH)

    print("Extraction completed!")


# ==========================================
# VALIDATION
# ==========================================

def validate_data():
    """Validate downloaded dataset files."""

    missing_files = [
        filename
        for filename in EXPECTED_FILES
        if not (RAW_PATH / filename).is_file()
    ]

    if missing_files:
        raise FileNotFoundError(
            f"Missing files: {missing_files}"
        )

    print("\nFiles successfully validated:")

    for filename in EXPECTED_FILES:
        file_path = RAW_PATH / filename

        size_mb = file_path.stat().st_size / (1024 ** 2)

        print(f"{filename}: {size_mb:.2f} MB")


# ==========================================
# EXECUTION
# ==========================================

def main():

    zip_path = download_data()

    extract_data(zip_path)

    validate_data()

    print("\nProcess completed successfully!")


if __name__ == "__main__":
    main()
