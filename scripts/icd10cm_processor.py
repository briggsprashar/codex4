## Parsing done separately

import pandas as pd 
from datetime import datetime
import openpyxl as pxl
import os
import gc

file_path = "input\icd10cm_2025.txt"

icd10cm_df = pd.read_csv(file_path, delimiter='\t', dtype=str)
icd10cm_df.info()

print(f"Successfully loaded {len(icd10cm_df)} records")

icd10cm_df.to_csv("output\icd10cm\icd10cm.csv") # explore raw file 
icd10cm_df.to_csv("output\icd10cm\icd10cm1.csv", index=False, sep='\t') # w.o index, tab separated

# Explore the csv as a fwf file, with headers
icd10cm_df = pd.read_fwf(file_path, header=None,
    names=['Number', 'Code', 'Level', 'Description', 'Description2'])

# Identify 4 key columns named above to explore/extract
icd10cm_df[['Number', 'Code', 'Level', 'Description']]
print(icd10cm_df.head())

shorticd10cm = icd10cm_df[['Code', 'Description']].copy() # Extract 2 columns to new df; "copy()" to create a copy from original file with the selected columns
shorticd10cm['Last_updated'] = datetime.today().strftime('%Y-%m-%d') # Add new column with today's date

shorticd10cm_df = shorticd10cm[                     # Remove empty/blank/NaN "Description" entries 
    shorticd10cm['Description'].notna() & 
    (shorticd10cm['Description'].str.strip() != '')
    ]

shorticd10cm_df = shorticd10cm.drop_duplicates()    # Remove duplicate rows if any keeping the first occurrence

shorticd10cm.to_csv("output\icd10cm\icd10cm3.csv", sep='\t', index=False) # Extract to a csv file with 3 columns

print(f"Successfully parsed {len(shorticd10cm_df)} records from {file_path}")
print(f"Saved to {'output_folder'}") 
print(f"Dataset shape: {shorticd10cm_df.shape}")
print(f"\nFirst 5 rows:")
print(shorticd10cm_df.head())

# File size
file_size_bytes = os.path.getsize("output\icd10cm\icd10cm3.csv")
file_size_mb = file_size_bytes / (1024 * 1024)
print(f"File size: {file_size_mb:.2f} MB")

# Memory usage
print (f"\nMemory usage (MB): {icd10cm_df.memory_usage(deep=True).sum() / 1024**2:.2f}") # different from polars

gc.collect()