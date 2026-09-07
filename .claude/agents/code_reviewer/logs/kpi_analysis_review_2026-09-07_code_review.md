# Code Review: kpi_analysis.py
**Date:** 2026-09-07  
**Reviewer:** Claude Code  
**File:** `.claude/skills/visualize/kpi_analysis.py`  
**Effort Level:** High  

---

## Executive Summary
This KPI analysis script has solid visualization logic but suffers from critical gaps in error handling, type hints, documentation, and configuration management. The script lacks reproducibility (random seed), hardcoded paths will break portability, and there are no input validation mechanisms. The code does not comply with project standards defined in CLAUDE.md.

---

## Issues by Severity

### 🔴 CRITICAL (Must Fix)

#### 1. **Missing Type Hints on All Functions**
- **Location:** Lines 29, 37, 83, 111, 239, 253
- **Issue:** CLAUDE.md explicitly requires "type hints for all functions." None are present.
- **Impact:** Reduces code maintainability, makes it harder for LLMs and developers to understand function contracts.
- **Fix:**
  ```python
  def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
      """Load parquet files from DATA_DIR."""
  
  def create_dimension_tables(fact_sales: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
      """Create synthetic dimension tables for date, store, and product."""
  
  def calculate_kpis(fact_sales: pd.DataFrame, dim_customer: pd.DataFrame) -> dict[str, float]:
      """Calculate KPIs from sales and customer data."""
  
  def create_visualizations(
      fact_sales: pd.DataFrame,
      dim_date: pd.DataFrame,
      dim_store: pd.DataFrame,
      dim_product: pd.DataFrame,
      dim_customer: pd.DataFrame
  ) -> None:
      """Create all visualizations and save to disk."""
  
  def print_kpis(kpis: dict[str, float]) -> None:
      """Print KPIs in a formatted table."""
  
  def main() -> None:
      """Main execution function."""
  ```

#### 2. **No Error Handling Anywhere**
- **Location:** Lines 32-34, 115-118, 122-134, 138-176, and all file I/O
- **Issue:** The script has zero try-except blocks. Any failure (missing files, bad data, disk full, corrupt parquet) will crash with unhandled exceptions.
- **Impact:** Not production-safe; no graceful degradation; poor user experience.
- **Fix:** Add exception handling:
  ```python
  def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
      """Load parquet files from DATA_DIR."""
      try:
          if not os.path.exists(DATA_DIR):
              raise FileNotFoundError(f"Data directory not found: {DATA_DIR}")
          fact_sales = pd.read_parquet(os.path.join(DATA_DIR, "fact_sales.parquet"))
          dim_customer = pd.read_parquet(os.path.join(DATA_DIR, "dim_customer.parquet"))
          return fact_sales, dim_customer
      except FileNotFoundError as e:
          print(f"ERROR: {e}")
          raise
      except pd.errors.ParquetFileError as e:
          print(f"ERROR: Failed to read parquet file: {e}")
          raise
      except Exception as e:
          print(f"ERROR: Unexpected error loading data: {e}")
          raise
  ```
  - Wrap merge operations: `sales_enriched.merge()` could fail if keys are missing
  - Wrap `plt.savefig()` calls: disk might be full
  - Validate data after loading (null checks, schema)

#### 3. **Hardcoded Paths Break Portability**
- **Location:** Line 21-22
  ```python
  DATA_DIR = "./.claude/skills/migrate/data/2026-09-06_00-33-01/"
  OUTPUT_DIR = "./.claude/skills/visualize/figures/"
  ```
- **Issue:** 
  - `DATA_DIR` includes a hardcoded timestamp. Script will fail if this directory doesn't exist.
  - Paths are relative; breaks if script is run from a different directory.
  - Not configurable; violates project best practices for reproducibility.
- **Impact:** Script is not reusable; must manually edit for each data run.
- **Fix:** Use environment variables or command-line arguments:
  ```python
  import sys
  from pathlib import Path
  
  DATA_DIR = Path(os.getenv("KPI_DATA_DIR", "./.claude/skills/migrate/data/")).expanduser()
  OUTPUT_DIR = Path(os.getenv("KPI_OUTPUT_DIR", "./.claude/skills/visualize/figures/")).expanduser()
  
  if not DATA_DIR.exists():
      raise FileNotFoundError(f"DATA_DIR does not exist: {DATA_DIR}")
  ```

#### 4. **Non-Reproducible Random Choices (No Seed)**
- **Location:** Lines 67, 77, and in visualization (line 213)
- **Issue:** `np.random.choice()` called without seeding. Results vary every run, making analysis non-reproducible.
  ```python
  'region': np.random.choice(['North', 'South', 'East', 'West'], len(store_sks))
  'category': np.random.choice(categories, len(product_sks))
  ```
- **Impact:** Cannot reproduce results; breaks scientific rigor; makes debugging harder.
- **Fix:**
  ```python
  RANDOM_SEED = 42
  np.random.seed(RANDOM_SEED)
  # OR use a seeded random generator:
  rng = np.random.RandomState(RANDOM_SEED)
  'region': rng.choice(['North', 'South', 'East', 'West'], len(store_sks))
  ```

#### 5. **Incomplete/Placeholder KPI Calculation**
- **Location:** Line 94
  ```python
  kpis['Total_Returns'] = 0  # No explicit returns in data
  ```
- **Issue:** Returns are hardcoded to 0 with a comment. This is incomplete; should either calculate from data or remove from KPI list.
- **Impact:** Misleading metrics; suggests feature was never completed.
- **Fix:** Either calculate returns properly or remove from output:
  ```python
  # If you want to infer returns from negative amounts or special columns:
  negative_transactions = fact_sales[fact_sales['net_amount'] < 0]
  kpis['Total_Returns'] = abs(negative_transactions['net_amount'].sum())
  
  # Or remove it entirely if it doesn't apply to this data.
  ```

---

### 🟠 MAJOR (Should Fix)

#### 6. **Incomplete Docstrings (Not PEP 257 Compliant)**
- **Location:** Lines 29-30, 37-38, 83-84, 239-240
- **Issue:** Docstrings are one-liners and don't include:
  - Parameter descriptions
  - Return value descriptions
  - Exceptions raised
  - Usage examples where appropriate
- **Standard (PEP 257):**
  ```python
  def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
      """Load parquet files from the data directory.
      
      Reads fact_sales.parquet and dim_customer.parquet from DATA_DIR.
      
      Returns:
          tuple: (fact_sales DataFrame, dim_customer DataFrame)
          
      Raises:
          FileNotFoundError: If parquet files don't exist in DATA_DIR.
          pd.errors.ParquetFileError: If parquet files are corrupted.
      """
  ```
- **Impact:** Documentation is vague; future maintainers must read code to understand function contracts.
- **Fix:** Add comprehensive docstrings to all functions following PEP 257.

#### 7. **No Input Validation or Schema Checks**
- **Location:** After `load_data()` returns (line 260)
- **Issue:** No verification that loaded data has required columns.
  ```python
  # No checks like:
  required_cols = ['date_sk', 'store_sk', 'product_sk', 'customer_sk', 'net_amount']
  if not all(col in fact_sales.columns for col in required_cols):
      raise ValueError(f"Missing required columns in fact_sales")
  ```
- **Impact:** If columns are missing or renamed, the script crashes deep in the code with cryptic errors.
- **Fix:** Add validation after loading:
  ```python
  def validate_fact_sales(df: pd.DataFrame) -> None:
      """Validate that fact_sales has required columns and non-null values."""
      required = ['date_sk', 'store_sk', 'product_sk', 'customer_sk', 'net_amount', 'gross_amount', 'discount_amount']
      missing = [col for col in required if col not in df.columns]
      if missing:
          raise ValueError(f"Missing columns in fact_sales: {missing}")
      if df.isnull().any().any():
          print(f"WARNING: Null values found in fact_sales:\n{df.isnull().sum()}")
  ```

#### 8. **Date Calculation Logic is Fragile**
- **Location:** Lines 44-58
- **Issue:** Assumes `date_sk` is sequential starting from 1. If it's not (e.g., starts at 100), dates will be wrong.
  ```python
  base_date = datetime(2024, 1, 1)
  for sk in range(int(min_date_sk), int(max_date_sk) + 1):
      current_date = base_date + timedelta(days=sk - 1)  # Assumes sk starts at 1!
  ```
- **Impact:** Dates could be completely wrong if data uses a different date_sk scheme.
- **Fix:**
  ```python
  # Either: find a mapping in the source data
  # Or: create date_sk based on actual dates
  # Or: add a comment explaining the assumption + assert it:
  min_sk = int(fact_sales['date_sk'].min())
  assert min_sk == 1, f"date_sk must start at 1, but found {min_sk}"
  ```

#### 9. **Repeated Code Blocks (Low Maintainability)**
- **Location:** Lines 121-176 (visualizations)
- **Issue:** 7 similar visualization functions are repeated with minor variations:
  - Daily sales trend (lines 121-134)
  - Sales by store (lines 137-148)
  - Sales by product (lines 150-163)
  - Sales by customer (lines 165-176)
  - And 3 more for discounts...
- **Impact:** Hard to maintain; changes must be made in multiple places; error-prone.
- **Fix:** Refactor into a helper function:
  ```python
  def create_bar_chart(
      data: pd.Series,
      title: str,
      xlabel: str,
      ylabel: str,
      color: str,
      filename: str,
      kind: str = 'bar'
  ) -> None:
      """Create and save a bar or horizontal bar chart."""
      plt.figure(figsize=(12, 6))
      data.plot(kind=kind, color=color)
      plt.title(title, fontsize=16, fontweight='bold')
      plt.xlabel(xlabel, fontsize=12)
      plt.ylabel(ylabel, fontsize=12)
      plt.xticks(rotation=45, ha='right')
      plt.tight_layout()
      plt.savefig(os.path.join(OUTPUT_DIR, filename), dpi=300, bbox_inches='tight')
      plt.close()
  ```

#### 10. **Magic Numbers Hardcoded**
- **Location:** Lines 125, 140, 154, 169, 183, 198, 212, 227 (figsize), Line 133, 147, etc. (dpi=300)
- **Issue:** Figure sizes (14, 6), (12, 6), dpi=300, font sizes are hardcoded.
- **Impact:** Hard to adjust visualization standards; violates DRY principle.
- **Fix:** Define constants:
  ```python
  # At top of file
  FIGURE_SIZE_WIDE = (14, 6)
  FIGURE_SIZE_STANDARD = (12, 6)
  FIGURE_DPI = 300
  FONT_SIZE_TITLE = 16
  FONT_SIZE_LABEL = 12
  ```

#### 11. **Missing Logging**
- **Location:** Lines 31, 39, 85, 121, 137, etc.
- **Issue:** Uses `print()` statements for logging. Not appropriate for a reusable script.
- **Impact:** Can't easily suppress/redirect output; no log levels (info/warning/error).
- **Fix:** Use Python's `logging` module:
  ```python
  import logging
  
  logger = logging.getLogger(__name__)
  
  def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
      logger.info("Loading data from %s", DATA_DIR)
      # ...
      logger.debug(f"Loaded {len(fact_sales)} sales records")
  ```

---

### 🟡 MEDIUM (Good to Fix)

#### 12. **Unnecessary Data Frame Conversions**
- **Location:** Lines 122-123, 180-181
  ```python
  daily_sales = sales_enriched.groupby('date')['net_amount'].sum().reset_index()
  daily_sales = daily_sales.sort_values('date')  # Already a DataFrame
  ```
- **Issue:** Converting Series → DataFrame → sort is one extra step. Could be:
  ```python
  daily_sales = sales_enriched.groupby('date', as_index=False)['net_amount'].sum().sort_values('date')
  ```
- **Impact:** Minor performance issue; negligible for small datasets but adds complexity.

#### 13. **No Check for Empty Dimension Data**
- **Location:** Lines 62-78
- **Issue:** If fact_sales has no stores or products, unique() returns empty array, creating empty dimensions.
  ```python
  store_sks = fact_sales['store_sk'].unique()  # What if this is empty?
  ```
- **Impact:** Silently produces incorrect data.
- **Fix:**
  ```python
  store_sks = fact_sales['store_sk'].unique()
  if len(store_sks) == 0:
      logger.warning("No stores found in fact_sales")
  ```

#### 14. **Using deprecated isocalendar()[1] for week number**
- **Location:** Line 56
  ```python
  'week': current_date.isocalendar()[1]
  ```
- **Issue:** Deprecated in Python 3.9+. Should use `.isocalendar().week`.
- **Impact:** Will break in future Python versions.
- **Fix:**
  ```python
  'week': current_date.isocalendar().week  # Python 3.9+
  ```

#### 15. **Path Operations Could Use pathlib More**
- **Location:** Lines 21-22, 26, 32-33
- **Issue:** Mix of `os.path.join()` and relative paths. Inconsistent.
- **Impact:** Less portable and readable than consistent pathlib usage.
- **Fix:**
  ```python
  from pathlib import Path
  
  DATA_DIR = Path("./.claude/skills/migrate/data/2026-09-06_00-33-01/")
  OUTPUT_DIR = Path("./.claude/skills/visualize/figures/")
  OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
  
  fact_sales = pd.read_parquet(DATA_DIR / "fact_sales.parquet")
  ```

#### 16. **No Configuration Object**
- **Location:** Lines 15-26
- **Issue:** Global config variables scattered at top of file; not encapsulated.
- **Impact:** Hard to override settings; not testable; violates separation of concerns.
- **Fix:** Create a config class or use dataclass:
  ```python
  from dataclasses import dataclass
  
  @dataclass
  class Config:
      data_dir: Path = Path("./.claude/skills/migrate/data/2026-09-06_00-33-01/")
      output_dir: Path = Path("./.claude/skills/visualize/figures/")
      figure_dpi: int = 300
      random_seed: int = 42
      
      def __post_init__(self):
          self.output_dir.mkdir(parents=True, exist_ok=True)
  ```

---

### 🔵 MINOR (Nice to Have)

#### 17. **Hardcoded Base Date in create_dimension_tables()**
- **Location:** Line 44
  ```python
  base_date = datetime(2024, 1, 1)
  ```
- **Issue:** Assumes data is from 2024. Should either be extracted from fact_sales or made configurable.
- **Impact:** If data is from 2025, the dimension will be misaligned.
- **Fix:**
  ```python
  # Infer from data or accept as parameter
  min_date = fact_sales['date'].min() if 'date' in fact_sales else datetime(2024, 1, 1)
  ```

#### 18. **String Formatting for Output**
- **Location:** Line 255
  ```python
  print(f"\n{'=' * 60}")
  ```
- **Issue:** Works but could be clearer. Minor style note.
- **Alternative:**
  ```python
  print("\n" + "=" * 60)
  ```

#### 19. **No __all__ Export**
- **Location:** Module level
- **Issue:** If this becomes a reusable module, no indication of public API.
- **Fix:** Add `__all__` at top:
  ```python
  __all__ = ['load_data', 'calculate_kpis', 'create_visualizations', 'main']
  ```

#### 20. **Print Statements in Functions Called from main()**
- **Location:** Throughout (lines 31, 39, 85, etc.)
- **Issue:** Mixing I/O with business logic; makes functions less reusable.
- **Fix:** Return status info, let caller decide to print:
  ```python
  def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
      # ... load code ...
      logger.info(f"Loaded {len(fact_sales)} sales records and {len(dim_customer)} customers")
      return fact_sales, dim_customer
  ```

---

## Summary Table

| # | Issue | Severity | Type | Line(s) |
|---|-------|----------|------|---------|
| 1 | Missing type hints on all functions | CRITICAL | Standards | 29, 37, 83, 111, 239, 253 |
| 2 | No error handling anywhere | CRITICAL | Robustness | All file I/O and data operations |
| 3 | Hardcoded paths not portable | CRITICAL | Config | 21-22 |
| 4 | No random seed (non-reproducible) | CRITICAL | Best Practices | 67, 77, 213 |
| 5 | Incomplete KPI calculation | CRITICAL | Logic | 94 |
| 6 | Incomplete docstrings | MAJOR | Documentation | 29-30, 37-38, 83-84, 239-240 |
| 7 | No input validation | MAJOR | Robustness | After line 260 |
| 8 | Fragile date logic | MAJOR | Correctness | 44-58 |
| 9 | Repeated visualization code | MAJOR | Maintainability | 121-234 |
| 10 | Magic numbers hardcoded | MAJOR | Config | Multiple |
| 11 | Missing logging module | MAJOR | Best Practices | Throughout |
| 12 | Unnecessary DataFrame conversions | MEDIUM | Performance | 122-123, 180-181 |
| 13 | No empty dimension check | MEDIUM | Robustness | 62-78 |
| 14 | Deprecated isocalendar()[1] | MEDIUM | Compatibility | 56 |
| 15 | Inconsistent path handling | MEDIUM | Consistency | 21-22, 26, 32-33 |
| 16 | No configuration object | MEDIUM | Design | 15-26 |
| 17 | Hardcoded base date | MINOR | Config | 44 |
| 18 | String formatting style | MINOR | Style | 255 |
| 19 | No __all__ export | MINOR | API | Module level |
| 20 | Print statements in business logic | MINOR | Design | Throughout |

---

## Recommendations (Priority Order)

### Immediate (Blocking)
1. Add type hints to all functions
2. Add comprehensive error handling around file I/O and data operations
3. Make paths configurable (environment variables or CLI args)
4. Fix random seed for reproducibility
5. Complete the KPI calculations

### Short Term (Next Review)
6. Improve docstrings to PEP 257 compliance
7. Add input validation and schema checks
8. Refactor repeated visualization code into helper functions
9. Add logging instead of print statements
10. Create a configuration object or class

### Long Term (Polish)
11. Fix deprecated date operations
12. Consolidate magic numbers into constants
13. Use pathlib consistently
14. Add unit tests
15. Consider adding a CLI interface with argparse

---

## Project Standards Compliance

Against CLAUDE.md requirements:

- ❌ **Type hints** - MISSING (all functions)
- ❌ **PEP 257 docstrings** - INCOMPLETE
- ❌ **PEP 8 style** - MOSTLY OK, but refactoring needed
- ❌ **Specific exception handling** - MISSING ENTIRELY
- ❌ **Configuration management** - Hardcoded, not isolated
- ❌ **Error robustness** - Not production-safe

**Verdict:** Does not meet project standards. Requires refactoring before merging.

---

**End of Review**
