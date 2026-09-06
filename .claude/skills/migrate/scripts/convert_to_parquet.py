"""
Script to convert CSV files from the latest folder in .claude/skills/fetchAPI/data
to parquet format and save them to .claude/skills/migrate/data.
The files are saved in a folder with the same datetime name as the source folder.
"""

import os
from pathlib import Path
import pandas as pd


def get_latest_folder(base_path: str) -> Path:
    """
    Get the latest folder based on datetime naming convention.

    Args:
        base_path: Path to the directory containing datetime-named folders

    Returns:
        Path to the latest folder

    Raises:
        FileNotFoundError: If path doesn't exist or contains no folders
    """
    base = Path(base_path)

    if not base.exists():
        raise FileNotFoundError(f"Source path does not exist: {base_path}")

    folders = [d for d in base.iterdir() if d.is_dir()]

    if not folders:
        raise FileNotFoundError(f"No folders found in {base_path}")

    return max(folders, key=lambda x: x.name)


def convert_csv_to_parquet(source_folder: Path, output_base: Path):
    """
    Convert all CSV files in source folder to parquet format.

    Args:
        source_folder: Path to folder containing CSV files
        output_base: Base output path where results will be saved
    """
    # Create output folder with same name as source folder
    output_folder = output_base / source_folder.name
    output_folder.mkdir(parents=True, exist_ok=True)

    # Find all CSV files
    csv_files = list(source_folder.glob("*.csv"))

    if not csv_files:
        print(f"⚠ No CSV files found in {source_folder}")
        return

    print(f"\n📁 Source: {source_folder}")
    print(f"📁 Output: {output_folder}")
    print(f"📊 Converting {len(csv_files)} file(s):\n")

    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file)
            parquet_path = output_folder / f"{csv_file.stem}.parquet"

            df.to_parquet(parquet_path, engine="pyarrow", index=False)

            size_kb = parquet_path.stat().st_size / 1024
            print(f"  ✓ {csv_file.name} → {parquet_path.name} ({size_kb:.2f} KB, {df.shape[0]} rows)")

        except Exception as e:
            print(f"  ✗ {csv_file.name}: {str(e)}")


def main():
    """Main function to orchestrate the conversion process."""
    # Define paths
    source_base = Path("./.claude/skills/fetch-api/data")
    output_base = Path("./.claude/skills/migrate/data")

    print("=" * 60)
    print("CSV to Parquet Converter")
    print("=" * 60)

    try:
        # Get latest source folder
        latest_folder = get_latest_folder(str(source_base))
        print(f"\n✓ Found latest folder: {latest_folder.name}")

        # Convert files
        convert_csv_to_parquet(latest_folder, output_base)

        print("\n" + "=" * 60)
        print("✓ Conversion completed!")
        print("=" * 60)

    except FileNotFoundError as e:
        print(f"\n✗ Error: {e}")
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")


if __name__ == "__main__":
    main()
