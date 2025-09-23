# Using pandas explored and transformed input raw xlsx data file to output as 3 .csv files
# to see raw file, to make raw file readable, and to extract needed columns from raw file plus adding a column
import pandas as pd
from datetime import datetime
import openpyxl as pxl
import os
import gc

file_path = "input\\HCPC2025_OCT_ANWEB.xlsx" # Define Filepath

pd.set_option('display.max_columns', None)

hcpc_df = pd.read_excel(file_path) # Define df

print(f"\nSuccessfully \033[34;1;4mLOADED\033[0m {len(hcpc_df)} HCPC records")

print(f"\n\033[34;1;4mHCPC FILE INFO\033[0m\n") # basic info: range index, data columns (total columns, index, column headers, non-null count, dtype, memory usage)
hcpc_df.info()

print("\n\033[34;1;4mHCPC FIRST 5 ROWS (Raw File)\033[0m\n")
print(hcpc_df.head())   # preview first 5 rows with truncated column snapshot; 5 rows and x columns

print(f"\n\033[34;1;4mHCPC ILOC\033[0m \n\n{hcpc_df.iloc[0]}") # display contents of first column; snapshots row contents
print(hcpc_df.iloc[0]) # displays contents of first column; snapshots row contents

hcpc_df.to_csv("output\\hcpc\\hcpc.csv") # Explore raw file as csv file > raw file has headers and is comma separated (cluttered)

hcpc_df.to_csv("output\\hcpc\\hcpc2.csv", sep='\t', index=False, header=True) # Explore as tab separated csv file

hcpc_df[['HCPC', 'LONG DESCRIPTION','SHORT DESCRIPTION']] # Identify 3 columns to extract/explore 

shorthcpc = hcpc_df[['HCPC', 'LONG DESCRIPTION']].copy() # Extract 2 columns to new df; "copy()" to create a copy from original file with the selected columns
shorthcpc = shorthcpc.rename(columns={'HCPC': 'Code', 'LONG DESCRIPTION': 'Description'}) # Rename columns: 'Code', 'Description' and 'Last_updated'
shorthcpc['Last_updated'] = datetime.today().strftime('%Y-%m-%d') # Add new column with today's date

# Remove duplicate rows
shorthcpc = hcpc_df.drop_duplicates()

shorthcpc.to_csv("output\\hcpc\\hcpc3.csv", sep='\t', index=False, header=True) # Extract to a csv file with 3 columns

print(f"\nCreated copy with columns \033[34;1;4m'?', '?' and '?'\033[0m")

print(f"\nSuccessfully \033[34;1;4mPARSED\033[0m {len(hcpc_df)} HCPC records from {file_path}")
# This line of code is printing a message indicating that the HCPC dataset has been saved to a
# specific file path. The formatting used in the message is for visual enhancement. Here's a breakdown
# of the message:
print(f"\nHCPC \033[34;1;4mSAVED\033[0m to {'output\\hcpc\\hcpc3.csv'}") 
print(f"\nHCPC Dataset \033[34;1;4mSHAPE:\033[0m {hcpc_df.shape}")

pd.reset_option('display.max_columns') # disabled > pd.set_option('display.max_columns', None)

print(f"\n\033[34;1;4mFIRST 20 ROWS (Extracted HCPC File):\033[0m\n {hcpc_df.head(20)}")

# bold text: \033[1m
# underline text: \033[4m
# rest formatting: \033[0m

# file size
file_size_bytes = os.path.getsize("output\\hcpc\\hcpc3.csv")
file_size_mb = file_size_bytes / (1024 * 1024)
print(f"\nExtracted HCPC \033[34;1;4mFile size\033[0m: {file_size_mb:.2f} MB")
# Memory usage
print (f"\n\033[34;1;4mMemory usage (MB)\033[0m: {hcpc_df.memory_usage(deep=True).sum() / 1024**2:.2f}\n") # different from polars

gc.collect()