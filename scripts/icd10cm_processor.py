## Parsing done separately
# Multiindex issue
import pandas as pd 
from datetime import datetime
import openpyxl as pxl
import os
import gc

file_path = "input\\icd10cm_2025.txt"

# pd.set_option('display.max_columns', None)

# icd10cm_df = pd.read_csv(file_path, dtype=str, sep='...', on_bad_lines='warn')

# Ignore BAD LINES
bad_lines_count = 0
def bad_line_handler(bad_line):
    global bad_lines_count
    bad_lines_count += 1
    # Return None to skip the bad line
    return None

# Use engine='python' when using a callable for on_bad_lines
icd10cm_df = pd.read_csv(file_path, dtype=str, sep=r'\s+', engine='python', on_bad_lines=bad_line_handler) # Multi index output!!

# icd10cm_df = pd.read_csv(file_path, sep=r'\s+', dtype=str, engine='python')

print(f"\nICD10US\033[34;1;4m FILE INFO\033[0m\n") # basic info: range index, data columns (total columns, index, column headers, non-null count, dtype, memory usage)
icd10cm_df.info() # (show_counts=True)

print(f"\nICD10US033[34;1;4m ILOC\033[0m \n\n{icd10cm_df.iloc[0]}") # display contents of first column; snapshots row contents
# icd10cm_df.info(verbose=True, show_counts=True)

print("\nICD10US \033[34;1;4mFIRST 5 ROWS (Raw File)\033[0m\n")
print(icd10cm_df.head())   # preview first 5 rows with truncated column snapshot; 5 rows and x columns

icd10cm_df.to_csv("output\\icd10cm\\icd10cm.csv") # explore raw file 
icd10cm_df.to_csv("output\\icd10cm\\icd10cm1.csv", index=False, sep='\t') # w.o index, tab separated

# Explore the csv as a fwf file, with headers
icd10cm_df = pd.read_fwf(file_path, header=None,
    names=['Number', 'Code', 'Level', 'Description', 'Description2'])

# Identify 4 key columns named above to explore/extract
icd10cm_df[['Number', 'Code', 'Level', 'Description']]
print("\n\033[34;1;4mICD10US ROW 1 CONTENT\033[0m\n")
print(icd10cm_df.head())

shorticd10cm = icd10cm_df[['Code', 'Description']].copy() # Extract 2 columns to new df; "copy()" to create a copy from original file with the selected columns
shorticd10cm['Last_updated'] = datetime.today().strftime('%Y-%m-%d') # Add new column with today's date

print(f"\nCreated a copy with columns \033[34;1;4m'Code', 'Description' and 'Last_updated'\033[0m\n")

#### Count null Descriptions
null_count = shorticd10cm['Description'].isnull().sum()
print(f"Number of null Descriptions: {null_count}")

#### Count empty strings
empty_count = (shorticd10cm['Description'] == '').sum()
print(f"Number of empty Descriptions: {empty_count}")

shorticd10cm_df = shorticd10cm[                     # Remove empty/blank/NaN "Description" entries 
    shorticd10cm['Description'].notna() & 
    (shorticd10cm['Description'].str.strip() != '')
    ]

shorticd10cm_df = shorticd10cm.drop_duplicates()    # Remove duplicate rows if any keeping the first occurrence

shorticd10cm.to_csv("output\\icd10cm\\icd10cm3.csv", sep='\t', index=False) # Extract to a csv file with 3 columns

print(f"\nSuccessfully \033[34;1;4mLOADED\033[0m {len(icd10cm_df)} ICD10US records")
print(f"\nNumber of ICD10US\033[34;1;4mBad Lines Skipped\033[0m: {bad_lines_count}")
print(f"\nSuccessfully \033[34;1;4mPARSED\033[0m {len(shorticd10cm_df)} ICD10US records from {file_path}")
print(f"\n\033[34;1;4mSAVED\033[0m to {'output\\icd10cm\\icd10cm3.csv'}") 
print(f"\nICD10US Dataset \033[34;1;4mSHAPE:\033[0m {shorticd10cm_df.shape}")
print(f"\n\033[34;1;4mFIRST FIVE ROWS (Extracted ICD10US File)\033[0m\n")
print(shorticd10cm_df.head())

# File size
file_size_bytes = os.path.getsize("output\\icd10cm\\icd10cm3.csv")
file_size_mb = file_size_bytes / (1024 * 1024)
print(f"\nExtracted ICD10US \033[34;1;4mFile size\033[0m: {file_size_mb:.2f} MB")

# Memory usage
print (f"\n\033[34;1;4mMemory usage (MB)\033[0m: {icd10cm_df.memory_usage(deep=True).sum() / 1024**2:.2f}\n") # different from polars

gc.collect()