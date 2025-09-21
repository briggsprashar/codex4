# Using pandas explored and transformed input raw xlsx data file to output as 3 .csv files
# to see raw file, to make raw file readable, and to extract needed columns from raw file plus adding a column
import pandas as pd
from datetime import datetime
import openpyxl as pxl
import os
import gc

file_path = "input\HCPC2025_OCT_ANWEB.xlsx" # Define Filepath

hcpc_df = pd.read_excel(file_path) # Define df
hcpc_df.info()          # basic info: range index, data columns (total columns, index, column headers, non-null count, dtype, memory usage)
print(hcpc_df.head())   # preview first 5 rows with truncated column snapshot; 5 rows and x columns

print(f"Successfully loaded {len(hcpc_df)} records")

hcpc_df.to_csv("output\hcpc\hcpc.csv") # Explore raw file as csv file > raw file has headers and is comma separated (cluttered)

hcpc_df.to_csv("output\hcpc\hcpc2.csv", sep='\t', index=False, header=True) # Explore as tab separated csv file

hcpc_df[['HCPC', 'LONG DESCRIPTION','SHORT DESCRIPTION']] # Identify 3 columns to extract/explore 

shorthcpc = hcpc_df[['HCPC', 'LONG DESCRIPTION']].copy() # Extract 2 columns to new df; "copy()" to create a copy from original file with the selected columns
shorthcpc = shorthcpc.rename(columns={'HCPC': 'Code', 'LONG DESCRIPTION': 'Description'}) # Rename columns: 'Code', 'Description' and 'Last_updated'
shorthcpc['Last_updated'] = datetime.today().strftime('%Y-%m-%d') # Add new column with today's date

shorthcpc.to_csv("output\hcpc\hcpc3.csv", sep='\t', index=False, header=True) # Extract to a csv file with 3 columns

print(f"Successfully parsed {len(hcpc_df)} records from {file_path}")
print(f"Saved to {'output_folder'}") 
print(f"Dataset shape: {hcpc_df.shape}")
print(f"\nFirst 5 rows:")
print(hcpc_df.head())

# file size
file_size_bytes = os.path.getsize("output\hcpc\hcpc3.csv")
file_size_mb = file_size_bytes / (1024 * 1024)
print(f"File size: {file_size_mb:.2f} MB")
# Memory usage
print (f"\nMemory usage (MB): {hcpc_df.memory_usage(deep=True).sum() / 1024**2:.2f}") # different from polars

gc.collect()