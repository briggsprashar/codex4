import pandas as pd 
from datetime import datetime
import openpyxl as pxl
import os
import gc

file_path="input\\Loinc.csv"

# pd.set_option('display.max_columns', None)

loinc= pd.read_csv(file_path,low_memory=False,sep=',')

print(f"\nSuccessfully \033[34;1;4mLOADED\033[0m {len(loinc)} LOINC records")

print(f"\nLOINC \033[34;1;4mFILE INFO\033[0m\n") # basic info: range index, data columns (total columns, index, column headers, non-null count, dtype, memory usage)
loinc.info() 

print(f"\nLOINC \033[34;1;4mILOC\033[0m \n\n{loinc.iloc[0]}") # display contents of first column; snapshots row contents
print("loinc.head()")

print(f"\nLOINC \033[34;1;4mFIRST FIVE ROWS (Raw File):\033[0m\n:")
print(loinc.head())

loinc.to_csv("output\\loinc\\loinc1.csv") # Explore raw file as csv to view

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

print(f"\nCreated a copy with columns \033[34;1;4m'Code', 'Description' and 'Last_updated'\033[0m")

# Explore shortloinc with 3 column headers from above
shortloinc.to_csv("output\\loinc\\loinc2.csv", index=False)

# Remove duplicate rows
rows_before = len(shortloinc)
shortloinc_no_duplicates = shortloinc.drop_duplicates()
rows_after = len(shortloinc_no_duplicates)
duplicates_removed = rows_before - rows_after
print(f"\n\033[34;1;4mDuplicates Removed\033[0m {duplicates_removed}")


# REMOVE empty descriptions/blanks/NaN values 
shortloinc = shortloinc[
    shortloinc['Description'].notna() & 
    shortloinc['Description'].str.strip() != '']


print(f"\nSuccessfully \033[34;1;4mPARSED\033[0m {len(shortloinc)} LOINC records from {file_path}")

print(f"\n\033[34;1;4mSAVED\033[0m to {'output\\loinc\\loinc3.csv'}") 
print(f"\nLOINC Dataset \033[34;1;4mSHAPE:\033[0m {shortloinc.shape}")
print(f"\n\033[34;1;4mFIRST FIVE ROWS (Extracted LOINC File):\033[0m\n:")
print(shortloinc.head())

# Extract csv file with 'Code', 'Description' and 'Last_updated' columns
shortloinc.to_csv("output\\loinc\\loinc3.csv", index=False)

# File size
file_size_bytes = os.path.getsize("output\\loinc\\loinc3.csv")
file_size_mb = file_size_bytes / (1024 * 1024)
print(f"\nLOINC \033[34;1;4mFile size\033[0m {file_size_mb:.2f} MB")

# Memory usage
print (f"\n\033[34;1;4mMemory usage (MB)\033[0m: {loinc.memory_usage(deep=True).sum() / 1024**2:.2f}") # different from polars

gc.collect()