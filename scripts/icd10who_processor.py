import pandas as pd 
from datetime import datetime
import openpyxl as pxl
import os
import gc

file_path = "input\\icd10who2019.txt"

pd.set_option('display.max_columns', None)

icd10who_df = pd.read_csv(file_path, header=None, sep=';')

print(f"\nICD10WHO\033[34;1;4mFILE INFO\033[0m\n") # basic info: range index, data columns (total columns, index, column headers, non-null count, dtype, memory usage)
icd10who_df.info()

print("\nICD10WHO\033[34;1;4mFIRST 5 ROWS (Raw File)\033[0m\n")
print(icd10who_df.head())

icd10who_df.to_csv("output\\icd10who\\icd10who1.csv") # Output Explore raw file as csv to view

columns = ['level', 'type', 'usage', 'sort', 'parent', 'code', 'display_code',  'icd10_code', 'title_en', 'parent_title', 'detailed_title', 
           'definition', 'mortality_code', 'morbidity_code1', 'morbidity_code2', 'morbidity_code3', 'morbidity_code4'
           ]

print(f"\nICD10WHO\033[34;1;4mILOC\033[0m \n\n{icd10who_df.iloc[0]}") # display contents of first column; snapshots row contents
# df.info(verbose=True, show_counts=True)

icd10who_df = pd.read_csv(file_path, header=None, sep=';', names=columns)
print("\nICD10WHO\033[34;1;4mFIRST 5 ROWS (Columns Renamed)\033[0m\n")
print(icd10who_df.head())

# Remove duplicate rows if any keeping the first occurrence
icd10who_df = icd10who_df.drop_duplicates()

# Explore processed raw file with column headers and no index
icd10who_df.to_csv("output\\icd10who\\icd10who2.csv", index=False)

# CREATE a trimmed DataFrame with selected columns and assign it to a new VARIABLE
    # use of double square brackets to select multiple columns
    # use of copy() to create a copy of the selected columns
shorticd10who = icd10who_df[['display_code', 'detailed_title']].copy()

shorticd10who['Last_updated'] = datetime.today().strftime('%m-%d-%Y') # Add new column with today's date

# Rename columns for clarity and consistency
shorticd10who= shorticd10who.rename(columns={
            "display_code": 'Code',
            "detailed_title": 'Description'
            })

print(f"\nCreated a copy with columns \033[34;1;4m'Code', 'Description' and 'Last_updated'\033[0m")

# REMOVE empty descriptions/blanks/NaN values 
shorticd10who = shorticd10who[
    shorticd10who['Description'].notna() & 
    (shorticd10who['Description'].str.strip() != '')
    ]

print(f"\nSuccessfully \033[34;1;4mLOADED\033[0m {len(icd10who_df)} ICD10WHO records")
print(f"\nSuccessfully \033[34;1;4mPARSED\033[0m {len(shorticd10who)} ICD10WHO records from {file_path}")
print(f"\n\033[34;1;4mSAVED\033[0m to {"output\\icd10who\\icd10who3.csv"}")
print(f"\nICD10WHO Dataset \033[34;1;4mSHAPE:\033[0m {shorticd10who.shape}")
print(f"\n\033[34;1;4mFIRST 20 ROWS (Extracted ICD10WHO File):\033[0m\n")
print(shorticd10who.head(20))

# Extract csv file with 'display_code', 'detailed_title' and 'last_updated' columns
shorticd10who.to_csv("output\\icd10who\\icd10who3.csv", index=False)

# File size
file_size_bytes = os.path.getsize("output\\icd10who\\icd10who3.csv")
file_size_mb = file_size_bytes / (1024 * 1024)
print(f"\nExtracted ICD10WHO\033[34;1;4mFile size\033[0m: {file_size_mb:.2f} MB")

# Memory usage
print (f"\n\033[34;1;4mMemory usage (MB)\033[0m: {icd10who_df.memory_usage(deep=True).sum() / 1024**2:.2f}\n") # different from polars

gc.collect()