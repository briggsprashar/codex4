# Using pandas explored and transformed input raw xlsx data file to output as a.csv file.
# to see raw file, to make raw file readable, and to extract needed columns from raw file
# Multiindex issue ## Parsing done separately

import pandas as pd 
from datetime import datetime
import openpyxl as pxl
from collections import Counter
import os
import gc
import time

# Start Timestamp
start_time_pandas = time.time()

# input file path
inputfile_path = "input\\icd10cm_2025.txt"

# output file path
outputfile_path = "output\\icd10cm\\icd10cm3.csv"

# cols not truncated
pd.set_option('display.max_columns', None)

# Ignore BAD LINES
bad_lines_count = 0
def bad_line_handler(bad_line):
    global bad_lines_count
    bad_lines_count += 1
    # Return None to skip the bad line
    return None

# Dataframe using engine='python' to call "on_bad_lines"
icd10cm_df = pd.read_csv(inputfile_path, dtype=str, sep=r'\s+', engine='python', on_bad_lines=bad_line_handler) # Multi index output!!

# print bad lines count
print(f"\n>>> Number of ICD10US \033[33;1mBad Lines Skipped\033[0m: {bad_lines_count}")

# save raw file to explore
# icd10cm_df = pd.read_csv(inputfile_path, sep=r'\s+', dtype=str, engine='python')

# Columns not truncated
pd.set_option('display.max_columns', None)

# Dataframe
# icd10cm_df = pd.read_csv(inputfile_path, dtype=str, sep='...', on_bad_lines='warn')

print(f"\n1>>> Successfully \033[33;1mLOADED\033[0m {len(icd10cm_df)} ICD10US records")

print(f"\n2>>> ICD10US Dataset \033[33;1mSHAPE:\033[0m {icd10cm_df.shape}")

# Total columns
num_columns = icd10cm_df.shape[1]
print(f"      >>> \033[33;1mCOLUMNS\033[0m: {num_columns}")

# Total rows
num_rows = icd10cm_df.shape[0]
print(f"      >>> \033[33;1mROWS\033[0m: {num_rows}")

print(f"\n3>>> ICD10US\033[33;1m FILE INFO\033[0m\n") # basic info: range index, data columns (total columns, index, column headers, non-null count, dtype, memory usage)
icd10cm_df.info() # (show_counts=True)

#  Print Unique data types and count of each dtype
dtype_counts = Counter(str(dtype) for dtype in icd10cm_df.dtypes)
print(f"\n      >>>\033[33;1mUnique data types and counts\033[0m: {dict(dtype_counts)}")

print(f"\n4>>> ICD10US Raw File \033[33;1m ILOC\033[0m \n\n{icd10cm_df.iloc[0]}") # display contents of first column; snapshots row contents
# icd10cm_df.info(verbose=True, show_counts=True)

print("\n5>>> ICD10US Raw File \033[33;1mFIRST 5 ROWS\033[0m\n")
print(icd10cm_df.head())   # preview first 5 rows with truncated column snapshot; 5 rows and x columns

icd10cm_df.to_csv("output\\icd10cm\\icd10cm.csv") # explore raw file 
icd10cm_df.to_csv("output\\icd10cm\\icd10cm1.csv", index=False, sep='\t') # w.o index, tab separated

# Explore the csv as a fwf file, with headers
icd10cm_df = pd.read_fwf(inputfile_path, header=None,
    names=['Number', 'Code', 'Level', 'Description', 'Description2'])

# Identify 4 key columns named above to explore/extract
icd10cm_df[['Number', 'Code', 'Level', 'Description']]
print("\n5.1>>> ICD10US \033[33;1mFIRST 5 ROWS with Columns Named\033[0m\n")
print(icd10cm_df.head())

shorticd10cm = icd10cm_df[['Code', 'Description']].copy() # Extract 2 columns to new df; "copy()" to create a copy from original file with the selected columns
shorticd10cm['Last_updated'] = datetime.today().strftime('%Y-%m-%d') # Add new column with today's date

pd.reset_option('display.max_columns') # disables > pd.set_option('display.max_columns', None)

# Describe for descriptive stats
print(f"\n >>> \033[32;1mDescribe - Raw File ??? \033[0m\n{icd10cm_df.describe()}")
print("\n6>> ... \033[35;1m Raw ICD10US file transformed and extracted\033[0m  ...\nwith columns \033[33;1m'Code', 'Description' and 'Last_updated'\033[0m")
print(f"\n >>> \033[32;1mDescribe - Extracted File ??? \033[0m\n{shorticd10cm.describe()}")

# Remove empty/blank/NaN "Description" entries 
shorticd10cm_df = shorticd10cm[                   
    shorticd10cm['Description'].notna() & 
    (shorticd10cm['Description'].str.strip() != '')
    ]

#### Count null Descriptions
null_count = shorticd10cm['Description'].isnull().sum()
print(f"\from nose.tools import set_trace; set_trace()    >>> Number of null Descriptions: {null_count}")

#### Count empty strings
empty_count = (shorticd10cm['Description'] == '').sum()
print(f"    >>> Number of empty Descriptions: {empty_count}")

print(f"\n  >>> Number of ICD10US \033[33;1mBad Lines Skipped\033[0m: {bad_lines_count}")

# Remove duplicate rows if any keeping the first occurrence
shorticd10cm_df = shorticd10cm.drop_duplicates()    

print(f"\n7>>> Successfully \033[33;1mPARSED\033[0m {len(shorticd10cm_df)} ICD10US records from {inputfile_path}")

shorticd10cm.to_csv(outputfile_path, sep='\t', index=False) # Extract to a csv file with 3 columns

print(f"\n8>>> ICD10US Extracted File \033[33;1mSAVED\033[0m to {outputfile_path}") 
print(f"\n9>>> ICD10US Dataset \033[33;1mSHAPE:\033[0m {shorticd10cm_df.shape}")
print(f"\n10>>> \033[33;1mPreview First few Rows\033[0m (Extracted ICD10US File) \n\n {shorticd10cm.head()}")

# Input file size
inputfile_size_bytes = os.path.getsize(inputfile_path)
inputfile_size_mb = inputfile_size_bytes / (1024 * 1024)
print(f"\n11>>> Raw ICD10US \033[33;1mFile size\033[0m: {inputfile_size_mb:.2f} MB")

# Raw File Memory usage
print (f"\n     >>> \033[33;1mMemory usage\033[0m: {icd10cm_df.memory_usage(deep=True).sum() / 1024**2:.2f} MB\n") # different from polars

# Extracted file size
file_size_bytes = os.path.getsize(outputfile_path)
file_size_mb = file_size_bytes / (1024 * 1024)
print(f"12>>> Extracted ICD10US \033[33;1mFile size\033[0m: {file_size_mb:.2f} MB")

# Extracted File Memory usage
print (f"\n     >>> \033[33;1mMemory usage\033[0m: {shorticd10cm_df.memory_usage(deep=True).sum() / 1024**2:.2f} MB\n") # different from polars

# End Timestamp
end_time_pandas = time.time()
# Elapsed Time
icd10cm_df_pandas = pd.read_csv(inputfile_path, nrows=10000, encoding_errors="ignore", on_bad_lines='skip')
elapsed_time_pandas = end_time_pandas - start_time_pandas
# Print total elapsed time
print(f" ------ \033[33;1mTotal Elapsed time:\033[0m \033[32;1m {elapsed_time_pandas:.3f} seconds \033[0m------\n")

gc.collect()