import pandas as pd 
from datetime import datetime
from collections import Counter
import openpyxl as pxl
import os
import gc

import time
# Start Timestamp
start_time_pandas = time.time()

# input file path
inputfile_path= "input\\Loinc.csv"

# output file path
outputfile_path = "output\\loinc\\loinc_final.csv"

# pd.set_option('display.max_columns', None)

# dataframe 
loinc= pd.read_csv(inputfile_path,low_memory=False,sep=',')

print(f"\n1>>> Successfully \033[33;1mLOADED\033[0m {len(loinc)} LOINC records")

print(f"\n>>> LOINC Dataset \033[33;1mSHAPE:\033[0m {loinc.shape}")

print(f"\n2>>> LOINC \033[33;1mFILE INFO\033[0m\n") # basic info: range index, data columns (total columns, index, column headers, non-null count, dtype, memory usage)
loinc.info() 

#  Print Unique data types and count of each dtype
dtype_counts = Counter(str(dtype) for dtype in loinc.dtypes)
print(f"\n      >>> \033[33;1mUnique data types and counts\033[0m: {dict(dtype_counts)}")

# ILOC
print(f"\n3>>> LOINC \033[33;1mILOC\033[0m \n\n{loinc.iloc[0]}") # display contents of first column; snapshots row contents
# print("loinc.head()")

# 1st five row preview
print(f"\n4>>> LOINC \033[33;1mFIRST FIVE ROWS (Raw File):\033[0m\n:")
print(loinc.head())

loinc.to_csv("output\\loinc\\loinc_raw1.csv") # Explore raw file as csv to view
loinc.to_csv("output\\loinc\\loinc_raw2.csv", sep= '\t', header=True)

# CREATE a trimmed DataFrame with selected columns and assign it to a new VARIABLE
    # use of double square brackets to select multiple columns
    # use of copy() to create a copy of the selected columns
shortloinc = loinc[["LOINC_NUM", "LONG_COMMON_NAME"]].copy()

shortloinc['Last_updated'] = datetime.today().strftime('%m-%d-%Y')  # Add new column with today's date

# Rename columns for clarity and consistency
shortloinc = shortloinc.rename(columns={
            "LOINC_NUM": 'Code',
            "LONG_COMMON_NAME": 'Description'
            })

pd.reset_option('display.max_columns') # disables > pd.set_option('display.max_columns', None)

# Describe for raw file
print(f"\n >>> \033[32;1mDescribe - Raw file ??? \033[0m\n{loinc.describe()}")

print("\n5>>>... \033[35;1mRaw LOINC file transformed to Extracted file ...\033[0m\n with columns \033[33;1m'Code', 'Description' and 'Last_updated'\033[0m")

# Describe for extracted file
print(f"\n >>> \033[32;1mDescribe - Extracted File ??? \033[0m\n{shortloinc.describe()}")

# Remove duplicate rows
rows_before = len(shortloinc)
shortloinc_no_duplicates = shortloinc.drop_duplicates()
rows_after = len(shortloinc_no_duplicates)
duplicates_removed = rows_before - rows_after

print(f"\n        >>> \033[33;1mDuplicates Removed\033[0m {duplicates_removed}")

# REMOVE empty descriptions/blanks/NaN values 
shortloinc = shortloinc[
    shortloinc['Description'].notna() & 
    shortloinc['Description'].str.strip() != '']

print(f"\n6>>> Successfully \033[33;1mPARSED\033[0m {len(shortloinc)} LOINC records from {inputfile_path}")

print(f"\n7>>> \033[33;1mSAVED\033[0m to {outputfile_path}") 
print(f"\n8>>> LOINC Dataset \033[33;1mSHAPE:\033[0m {shortloinc.shape}")
print(f"\n9>>> \033[33;1mFIRST FIVE ROWS (Extracted LOINC File):\033[0m\n")
print(shortloinc.head())

# Extract csv file with 'Code', 'Description' and 'Last_updated' columns
shortloinc.to_csv(outputfile_path, index=False)

# input file size
inputfile_size_bytes = os.path.getsize(inputfile_path)
inputfile_size_mb = inputfile_size_bytes / (1024 * 1024)
print(f"\n10>>> Raw Loinc \033[33;1mFile size\033[0m: {inputfile_size_mb:.2f} MB")

# Input Memory usage
print (f"\n     >>> \033[33;1mMemory usage\033[0m: {loinc.memory_usage(deep=True).sum() / 1024**2:.2f} MB\n") # different from polars

# extracted file size
file_size_bytes = os.path.getsize(outputfile_path)
file_size_mb = file_size_bytes / (1024 * 1024)
print(f"11>>> LOINC \033[33;1mFile size\033[0m {file_size_mb:.2f} MB")

# Extracted Memory usage
print (f"\n     >>> \033[33;1mMemory usage\033[0m: {shortloinc.memory_usage(deep=True).sum() / 1024**2:.2f} MB\n") # different from polars

# End Timestamp
end_time_pandas = time.time()
# Elapsed Time
# loinc_pandas = pd.read_csv(inputfile_path, nrows=10000, encoding_errors="ignore", on_bad_lines='skip')
elapsed_time_pandas = end_time_pandas - start_time_pandas
# Print total elapsed time
print(f" ------ \033[33;1mTotal Elapsed time:\033[0m \033[32;1m {elapsed_time_pandas:.3f} seconds \033[0m------\n")

loinc = None
del loinc
shortloinc = None
del shortloinc

gc.collect()