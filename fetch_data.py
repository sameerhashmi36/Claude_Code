#!/usr/bin/env python3
"""
Fetch CSV data from GitHub repositories and save with logging.
"""

import asyncio
import httpx
import os
from datetime import datetime
from pathlib import Path
import logging
from typing import List, Tuple


# URLs to fetch
URLS = [
    "https://raw.githubusercontent.com/anshlambagit/AnshLambaYoutube/refs/heads/main/DBT_Masterclass/dim_customer.csv",
    "https://raw.githubusercontent.com/anshlambagit/AnshLambaYoutube/refs/heads/main/DBT_Masterclass/fact_sales.csv",
]

# Base directories
BASE_DATA_DIR = Path(".claude/skills/fetch-api/data")
BASE_LOG_DIR = Path(".claude/skills/fetch-api/logs")


def setup_directories() -> Tuple[Path, Path]:
    """Create timestamped directories for data and logs."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    data_dir = BASE_DATA_DIR / timestamp
    log_dir = BASE_LOG_DIR / timestamp

    data_dir.mkdir(parents=True, exist_ok=True)
    log_dir.mkdir(parents=True, exist_ok=True)

    return data_dir, log_dir, timestamp


def setup_logger(log_dir: Path) -> logging.Logger:
    """Configure logger for the fetch API operation."""
    logger = logging.getLogger("fetchAPI")
    logger.setLevel(logging.INFO)

    log_file = log_dir / "fetchAPI.log"
    handler = logging.FileHandler(log_file)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Also log to console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


async def fetch_csv(client: httpx.AsyncClient, url: str, logger: logging.Logger) -> Tuple[str, bytes | None]:
    """Fetch a single CSV file from URL."""
    try:
        logger.info(f"Fetching API: {url}")
        response = await client.get(url, timeout=30.0)
        response.raise_for_status()
        logger.info(f"Successfully fetched: {url} (Status: {response.status_code})")
        return url, response.content
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP Error for {url}: {e.response.status_code} - {e.response.reason_phrase}")
        return url, None
    except httpx.TimeoutException:
        logger.error(f"Timeout error while fetching: {url}")
        return url, None
    except Exception as e:
        logger.error(f"Unexpected error fetching {url}: {type(e).__name__} - {str(e)}")
        return url, None


async def fetch_all_csvs(logger: logging.Logger) -> dict:
    """Fetch all CSV files concurrently."""
    results = {}
    async with httpx.AsyncClient() as client:
        tasks = [fetch_csv(client, url, logger) for url in URLS]
        responses = await asyncio.gather(*tasks)

        for url, content in responses:
            results[url] = content

    return results


def save_csv_files(data_dir: Path, results: dict, logger: logging.Logger) -> None:
    """Save fetched CSV files to the data directory."""
    for url, content in results.items():
        if content is not None:
            filename = url.split("/")[-1]
            filepath = data_dir / filename
            filepath.write_bytes(content)
            logger.info(f"Saved: {filepath}")
        else:
            filename = url.split("/")[-1]
            logger.warning(f"Skipped saving {filename} - fetch failed")


async def main():
    """Main function to orchestrate the fetch process."""
    # Setup directories
    data_dir, log_dir, timestamp = setup_directories()
    logger = setup_logger(log_dir)

    logger.info("=" * 60)
    logger.info("Starting API Fetch Process")
    logger.info(f"Timestamp: {timestamp}")
    logger.info(f"Data directory: {data_dir}")
    logger.info(f"Log directory: {log_dir}")
    logger.info("=" * 60)

    # Fetch all CSVs
    results = await fetch_all_csvs(logger)

    # Save files
    save_csv_files(data_dir, results, logger)

    # Summary
    successful = sum(1 for content in results.values() if content is not None)
    failed = len(results) - successful

    logger.info("=" * 60)
    logger.info(f"Fetch Process Complete")
    logger.info(f"Total APIs: {len(URLS)}")
    logger.info(f"Successful: {successful}")
    logger.info(f"Failed: {failed}")
    logger.info("=" * 60)

    print(f"\n✅ Fetch completed! Data saved to: {data_dir}")
    print(f"📝 Log saved to: {log_dir / 'fetchAPI.log'}")


if __name__ == "__main__":
    asyncio.run(main())
