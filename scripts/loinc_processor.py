import pandas as pd 
from datetime import datetime
import openpyxl as pxl
import os
import gc

file_path="input\Loinc.csv"

loinc= pd.read_csv(file_path,low_memory=False,sep=',')
loinc.info()
print(loinc.head())

print(f"Successfully loaded {len(loinc)} records")

loinc.to_csv("output\loinc\loinc1.csv") # Explore raw file as csv to view

# CREATE a trimmed DataFrame with selected columns and assign it to a new VARIABLE
    # use of double square brackets to select multiple columns
    # use of copy() to create a copy of the selected columns
shortloinc = loinc[["LOINC_NUM", "LONG_COMMON_NAME"]].copy()

shortloinc['Last_updated'] = datetime.today().strftime('%m-%d-%Y')  # Add new column with today's date

# Explore shortloinc  with 3 column headers from above
shortloinc.to_csv("output\loinc\loinc2.csv", index=False)

# Rename columns for clarity and consistency
shortloinc = shortloinc.rename(columns={
            "LOINC_NUM": 'Code',
            "LONG_COMMON_NAME": 'Description'
            })

# REMOVE empty descriptions/blanks/NaN values 
shortloinc = shortloinc[
    shortloinc['Description'].notna() & 
    shortloinc['Description'].str.strip() != '']

print(f"Successfully parsed {len(shortloinc)} records from {file_path}")
print(f"Saved to {'output_folder'}") 
print(f"Dataset shape: {shortloinc.shape}")
print(f"\nFirst 5 rows:")
print(shortloinc.head())

# Extract csv file with 'Code', 'Description' and 'Last_updated' columns
shortloinc.to_csv("output\loinc\loinc3.csv", index=False)

# File size
file_size_bytes = os.path.getsize("output\loinc\loinc3.csv")
file_size_mb = file_size_bytes / (1024 * 1024)
print(f"File size: {file_size_mb:.2f} MB")

# Memory usage
print (f"\nMemory usage (MB): {loinc.memory_usage(deep=True).sum() / 1024**2:.2f}") # different from polars

gc.collect()