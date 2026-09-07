"""
Script to fetch CSV data from remote URLs using async httpx.
Saves the fetched data to timestamped folders with detailed logging.
"""

import asyncio
import httpx
from pathlib import Path
from datetime import datetime
import logging
from typing import List, Dict, Tuple


async def fetch_csv_data(urls: List[str]) -> Tuple[Dict[str, str], Dict[str, str]]:
    """
    Fetch CSV data from multiple URLs using async httpx.

    Args:
        urls: List of URLs to fetch data from

    Returns:
        Tuple of (success_data, error_data) where:
        - success_data: Dict with filename as key and CSV content as value
        - error_data: Dict with URL as key and error message as value
    """
    success_data = {}
    error_data = {}

    async with httpx.AsyncClient(timeout=30.0) as client:
        for url in urls:
            try:
                logging.info(f"Fetching data from: {url}")
                response = await client.get(url)
                response.raise_for_status()

                # Extract filename from URL
                filename = url.split('/')[-1]
                success_data[filename] = response.text
                logging.info(f"✓ Successfully fetched: {filename} ({len(response.text)} bytes)")

            except httpx.HTTPError as e:
                error_msg = f"HTTP Error: {str(e)}"
                error_data[url] = error_msg
                logging.error(f"✗ Failed to fetch {url}: {error_msg}")

            except Exception as e:
                error_msg = f"Unexpected error: {str(e)}"
                error_data[url] = error_msg
                logging.error(f"✗ Failed to fetch {url}: {error_msg}")

    return success_data, error_data


def save_csv_files(data: Dict[str, str], output_folder: Path) -> None:
    """
    Save CSV data to files in the output folder.

    Args:
        data: Dictionary with filename as key and CSV content as value
        output_folder: Path to save the files
    """
    output_folder.mkdir(parents=True, exist_ok=True)

    for filename, content in data.items():
        try:
            filepath = output_folder / filename
            filepath.write_text(content)
            logging.info(f"✓ Saved: {filename}")
        except Exception as e:
            logging.error(f"✗ Failed to save {filename}: {str(e)}")


def setup_logging(log_folder: Path, timestamp: str) -> None:
    """
    Setup logging to file and console.

    Args:
        log_folder: Path to save log files
        timestamp: Timestamp for the log folder name
    """
    log_folder.mkdir(parents=True, exist_ok=True)
    log_file = log_folder / "fetchAPI.log"

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )


def create_log_summary(success_data: Dict[str, str], error_data: Dict[str, str]) -> str:
    """
    Create a summary of the fetch operation.

    Args:
        success_data: Dictionary of successfully fetched data
        error_data: Dictionary of errors

    Returns:
        Summary string
    """
    summary = f"""
{'='*60}
FETCH API SUMMARY
{'='*60}
Timestamp: {datetime.now().isoformat()}
{'='*60}

SUCCESSFUL FETCHES: {len(success_data)}
"""
    for filename in success_data:
        summary += f"  ✓ {filename}\n"

    if error_data:
        summary += f"\nFAILED FETCHES: {len(error_data)}\n"
        for url, error in error_data.items():
            summary += f"  ✗ {url}\n     Error: {error}\n"
    else:
        summary += f"\nFAILED FETCHES: 0\n"

    summary += f"{'='*60}\n"
    return summary


def main():
    """Main function to orchestrate the fetch operation."""
    # Define URLs to fetch
    urls = [
        "https://raw.githubusercontent.com/anshlambagit/AnshLambaYoutube/refs/heads/main/DBT_Masterclass/dim_customer.csv",
        "https://raw.githubusercontent.com/anshlambagit/AnshLambaYoutube/refs/heads/main/DBT_Masterclass/fact_sales.csv"
    ]

    # Create timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Define paths
    data_base = Path("./.claude/skills/fetch-api/data")
    log_base = Path("./.claude/skills/fetch-api/logs")

    data_folder = data_base / timestamp
    log_folder = log_base / timestamp

    # Setup logging
    setup_logging(log_folder, timestamp)

    print(f"\n📥 Fetch API Data Pipeline")
    print(f"   Timestamp: {timestamp}\n")

    logging.info("="*60)
    logging.info("Starting Fetch API Data Pipeline")
    logging.info("="*60)
    logging.info(f"Number of URLs to fetch: {len(urls)}")

    # Fetch data
    success_data, error_data = asyncio.run(fetch_csv_data(urls))

    # Save data
    if success_data:
        save_csv_files(success_data, data_folder)
        logging.info(f"✓ Data saved to: {data_folder}")

    # Create summary
    summary = create_log_summary(success_data, error_data)
    print(summary)
    logging.info(summary)

    logging.info("="*60)
    logging.info("Fetch API Data Pipeline Completed")
    logging.info("="*60)


if __name__ == "__main__":
    main()
