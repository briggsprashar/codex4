# output in a csv from polars
# import pandas as pd  
import polars as pl
from pathlib import Path
from datetime import datetime

file_path = Path('input\snomeddata.txt')

snomed = pl.read_csv(
    file_path,
    separator='\t',
    has_header=True,
    quote_char=None,
    encoding='utf8-lossy',
    truncate_ragged_lines=True,
    dtypes={
        'id': pl.Utf8,
        'effectiveTime': pl.Utf8,
        'active': pl.Int32,
        'moduleId': pl.Utf8,
        'conceptId': pl.Utf8,
        'languageCode': pl.Utf8,
        'typeId': pl.Utf8,
        'term': pl.Utf8,
        'caseSignificanceId': pl.Utf8
    })

# Current date in YYYY-MM-DD format
today_date = datetime.today().strftime('%Y-%m-%d')

# Create a copy with required columns renamed and add last_updated column
copy_snomed = snomed.select([
    pl.col('id').alias('Code'),
    pl.col('term').alias('Description')]).with_columns(
    pl.lit(today_date).alias('Last_updated')
    )

copy_snomed.write_csv("output\snomed\snomed_pl.csv")

print(f"Created copy with columns 'Code', 'Description' and 'last_updated'")

print(f"Successfully parsed {len(snomed)} records from SNOMED CT file")
print(f"Saved to {"output\snomed\snomed_2.csv"}")
print(f"Dataset shape: {snomed.shape}")
print(f"\nColumn names: {snomed.columns}")
print(f"\nFirst 5 rows:")
print(snomed.head())
print(f"\nMemory usage (MB): {snomed.estimated_size() / 1024**2:.2f}")

print(f"\nActive terms count: {snomed.filter(pl.col('active') == 1).height}")
print(f"Language codes: {snomed['languageCode'].unique().to_list()}")