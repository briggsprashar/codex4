import pandas as pd 
from datetime import datetime
import openpyxl as pxl
import os
import gc

file_path = "input\icd10who2019.txt"

icd10who_df = pd.read_csv(file_path, header=None, sep=';')
icd10who_df.info()
print(icd10who_df.head())

print(f"Successfully loaded {len(icd10who_df)} records")

icd10who_df.to_csv("output\icd10who\icd10who1.csv") # Output Explore raw file as csv to view

columns = ['level', 'type', 'usage', 'sort', 'parent', 'code', 'display_code',  'icd10_code', 'title_en', 'parent_title', 'detailed_title', 
           'definition', 'mortality_code', 'morbidity_code1', 'morbidity_code2', 'morbidity_code3', 'morbidity_code4'
           ]

icd10who_df = pd.read_csv(file_path, header=None, sep=';', names=columns)
icd10who_df.info()
print(icd10who_df.head())


# Remove duplicate rows if any keeping the first occurrence
icd10who_df = icd10who_df.drop_duplicates()

# Explore processed raw file with column headers and no index
icd10who_df.to_csv("output\icd10who\icd10who2.csv", index=False)

# CREATE a trimmed DataFrame with selected columns and assign it to a new VARIABLE
    # use of double square brackets to select multiple columns
    # use of copy() to create a copy of the selected columns
shorticd10who = icd10who_df[['display_code', 'detailed_title']].copy()

shorticd10who['last_updated'] = datetime.today().strftime('%m-%d-%Y') # Add new column with today's date

# REMOVE empty descriptions/blanks/NaN values 
shorticd10who = shorticd10who[
    shorticd10who['detailed_title'].notna() & 
    (shorticd10who['detailed_title'].str.strip() != '')
    ]
print(f"Successfully parsed {len(shorticd10who)} records from {file_path}")
print(f"Saved to {"output_folder"}")
print(f"Dataset shape: {shorticd10who.shape}")
print(f"\nFirst 5 rows:")
print(icd10who_df.head())

# Extract csv file with 'display_code', 'detailed_title' and 'last_updated' columns
shorticd10who.to_csv("output\icd10who\icd10who3.csv", index=False)

# File size
file_size_bytes = os.path.getsize("output\icd10who\icd10who3.csv")
file_size_mb = file_size_bytes / (1024 * 1024)
print(f"File size: {file_size_mb:.2f} MB")

# Memory usage
print (f"\nMemory usage (MB): {icd10who_df.memory_usage(deep=True).sum() / 1024**2:.2f}") # different from polars

gc.collect()