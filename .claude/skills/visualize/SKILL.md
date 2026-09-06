---
name: visualize
description: Visualizes data using various libraries and tools. 
---

## Usage

### Step 1: Pick the python environment
Before you start, ensure you have the correct Python environment selected in your IDE or terminal. You can run/install dependencies using my '.venv' environment which is located at "/home/sameer/Documents/Claude_Code/.venv"

### Step 2: Use pandas to build KPIs
- You need to read the parquet files stored in ".claude/skills/migrate/data/".
- After reading the data, you need to use pandas to build following KPIs:
  - Total Sales
  - Total Returns
  - Net Sales
  - Average Sales per Store
  - Average Sales per Product
  - Average Sales per Customer

### Step 3: Visualize the KPIs using matplotlib/seaborn
- After building the KPIs, you need to visualize them using matplotlib/seaborn:
    - Sales Trend over Time
    - Sales by Store
    - Sales by Product
    - Sales by Customer
    - Returns Trend Over Time
    - Returns by Store
    - Returns by Product
    - Returns by Customer
  - Also you need to save the visualizations as PNG files in the folder with the same name as source folder (datetime) "./claude/skills/visualize/figures/" using plt.savefig() function.