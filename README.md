# MP1 Data Processing Pipeline

This project is a configurable data-processing pipeline that loads, validates, cleans, and saves structured data. The pipeline loads the input dataset and YAML configuration using the functions in `data_loaders.py`. The `data_validator.py` module checks required columns, removes invalid numeric values, and converts configured columns to numeric data types. The `data_processor.py` module removes duplicate rows, handles missing values, removes outliers, and creates a cleaning report. The `data_output.py` module creates the output directory and saves the cleaned DataFrame as a CSV file. Shared logging and file-validation functions are located in `utils.py`, while `pipeline.py` coordinates the complete workflow.

## Example Command

```bash
python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose

#Example output
Validation complete: 100 -> 98 rows
Processing complete: 98 -> 92 rows
Saved cleaned data to output/clean.csv

Cleaning report:
{'rows_before': 98, 'rows_after': 92, 'rows_removed': 6, 'columns_before': 5, 'columns_after': 5, 'columns_removed': 0}

Save it.

## 2. Confirm `.gitignore`

Make sure `.gitignore` includes:

```gitignore
output/