# Using polars output in a parquet csv and a >100mb 
# import pandas as pd  
import polars as pl
import os 
from pathlib import Path
from datetime import datetime
import gc

file_path = Path('input\\snomeddata.txt')

snomed = pl.read_csv(file_path)    # Explore raw file
snomed.write_csv("output\\snomed\\snomedraw.csv") 

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

today_date = datetime.today().strftime('%Y-%m-%d') # Add new column with today's date

# Create a copy with required columns renamed and add last_updated column
copy_snomed = snomed.select([
    pl.col('id').alias('Code'),
    pl.col('term').alias('Description')]).with_columns(
    pl.lit(today_date).alias('Last_updated')
    )

# copy_snomed.write_csv("output\snomed\snomed_pl.csv")
copy_snomed.write_parquet("output\\snomed\\snomed_polarspq.csv")

print(f"\nCreated copy with columns 'Code', 'Description' and 'last_updated'")

print(f"\nSuccessfully parsed {len(snomed)} records from SNOMED CT file")
print(f"\nSaved to {"output\\snomed\\snomed_2.csv"}")
print(f"\nDataset shape: {snomed.shape}")
print(f"\nColumn names: {snomed.columns}")
print(f"\nFirst 5 rows:")
print(snomed.head())
print(f"\nMemory usage (MB): {snomed.estimated_size() / 1024**2:.2f}")

print(f"\nActive terms count: {snomed.filter(pl.col('active') == 1).height}")
print(f"Language codes: {snomed['languageCode'].unique().to_list()}")

# File size
file_size_bytes = os.path.getsize("output\\snomed\\snomed_polarspq.csv")
file_size_mb = file_size_bytes / (1024 * 1024)
print(f"File size: {file_size_mb:.2f} MB")

# Memory usage
print(f"\nMemory usage (MB): {snomed.estimated_size() / 1024**2:.2f}") # different from pandas

gc.collect()