---
name: fetch-api
description: A skill to fetch data from an API and return the response. Use when interacting with external APIs or retrieving data from web services.
---

## Usage

### Step 1: Fetch Data from APIs
You need to make python API calls to fetch data from the following URLs using async httpx: ["https://raw.githubusercontent.com/anshlambagit/AnshLambaYoutube/refs/heads/main/DBT_Masterclass/dim_customer.csv", "https://raw.githubusercontent.com/anshlambagit/AnshLambaYoutube/refs/heads/main/DBT_Masterclass/fact_sales.csv"]

### Step 2: Handle API Responses
After fetching the data, you need to create a directory having name with current date and time in the format "YYYY-MM-DD_HH-MM-SS" and save the fetch data as CSV files in that directory. The location of the directory should be ".claude/skills/fetch-api/data/". 

### Step 3: Logging
You need to create a log directory at ".claude/skills/fetch-api/logs/" with name current date and time in the format "YYYY-MM-DD_HH-MM-SS" and save the log file in that directory with the name "fetchAPI.log". The log file should contain information about the API calls made, including what APIs called, what were successful and what were not, and any errors encountered during the process.