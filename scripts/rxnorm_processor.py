import pandas as pd
from datetime import datetime
from collections import Counter
import os
import gc
import time
# Start Timestamp
start_time_pandas = time.time()

# Input file path
inputfile_path = "input\RXNSAT.RRF"

pd.set_option('display.max_columns', None) # reset: pd.reset_option('display.max_columns')

rxnorm = pd.read_csv(inputfile_path, nrows=100000,
    sep="|",        # pipe-delimited in raw file
    header=None,    # no headers in raw file
    dtype=str)      # can also use e before file path above to identify raw string data

print(f"\n1>>> Successfully \033[34;1mLOADED\033[0m {len(rxnorm)} records")

print(f"\n>>> RxNorm Dataset \033[34;1mSHAPE:\033[0m {rxnorm.shape}")

print(f"\n2>>> RxNorm \033[33;1mFILE INFO\033[0m\n") # basic info: range index, data columns (total columns, index, column headers, non-null count, dtype, memory usage)
rxnorm.info() 

#  Print Unique data types and count of each dtype
dtype_counts = Counter(str(dtype) for dtype in rxnorm.dtypes)
print(f"\n      >>> \033[33;1mUnique data types and counts\033[0m: {dict(dtype_counts)}")

print(f"\n3>>> RxNorm \033[33;1mILOC\033[0m \n\n{rxnorm.iloc[0]}") # display contents of first column; snapshots row contents

print(f"\n4>>> \033[33;1mFIRST FIVE ROWS\033[0m Raw RxNorm File\n:")
print(rxnorm.head())

# Explore key columns by index
rxnorm[[0, 9]]

shortrxnorm = rxnorm[[0, 9]].copy() # Create a simplified DataFrame with selected columns
shortrxnorm['Last_updated'] = datetime.today().strftime('%m-%d-%Y') # Add new column with today's date

# Rename columns for clarity and consistency
shortrxnorm = shortrxnorm.rename(columns={
    0: 'Code',
    9: 'Description'
})

# pd.reset_option('display.max_columns') # disables > pd.set_option('display.max_columns', None)

# output file path
outputfile_path = 'output//rxnorm_short//rx_short.csv'

# Describe for descriptive stats
print(f"\n >>> \033[32;1mDescribe - Raw File ??? \033[0m\n{rxnorm.describe()}")

print("\n5>>>... \033[35;1mRaw RxNorm file transformed to Extracted file ...\033[0m\n with columns \033[33;1m'Code', 'Description' and 'Last_updated'\033[0m")

print(f"\n >>> \033[32;1mDescribe - Extracted File ???Control file.. Description??\033[0m\n{shortrxnorm.describe()}")

print(f"\n6>>> Successfully \033[33;1mPARSED:\033[0m {len(shortrxnorm)} records from RXNATOMARCHIVE.RRF")

# Remove duplicate rows
rows_before = len(shortrxnorm)
shortrxnorm_no_duplicates = shortrxnorm.drop_duplicates()
rows_after = len(shortrxnorm_no_duplicates)
duplicates_removed = rows_before - rows_after

print(f"\n      >>> \033[33;1mDuplicates removed: \033[0m {duplicates_removed}???")

#### Count null Descriptions
# null_count = shortrxnorm['9'].isnull().sum()
# print(f"Number of null Descriptions: {null_count}")

#### Count empty strings
# empty_count = (shortrxnorm['9'] == '').sum()
# print(f"Number of empty Descriptions: {empty_count}")

#removing empty descriptions or nulls or blanks 
# shortrxnorm = shortrxnorm[
#   shortrxnorm[9].notna() & 
#   (shortrxnorm[9].str.strip() != "")]

# Extract csv file with 'Code', 'Description' and 'Last_updated' columns
shortrxnorm.to_csv(outputfile_path, sep='\t', index=False, header=True)

print(f"\n7>>> RxNorm Dataset \033[33;1mSHAPE\033[0m: {shortrxnorm.shape}")
print(f"\n8>>> \033[33;1mFIRST FIVE ROWS\033[0m: Extracted RxNorm File\n")
print(shortrxnorm.head())

print(f"\n9>>> \033[33;1mSAVED\033[0m to {'output/rxnorm/rxnorm.csv'}") # \r conflicts, so use \\r or /r
# its better to create capture "input_path" and "output_path" in an object for reusability

# input file size
inputfile_size_bytes = os.path.getsize(inputfile_path)
inputfile_size_mb = inputfile_size_bytes / (1024 * 1024)
print(f"\n10>>> Raw RxNorm \033[33;1mFile size\033[0m: {inputfile_size_mb:.2f} MB")
# Raw Memory usage
print (f"\n     >>> Raw File \033[33;1mMemory usage\033[0m: {rxnorm.memory_usage(deep=True).sum() / 1024**2:.2f}MB") # different from polars

# extracted File size
file_size_bytes = os.path.getsize(outputfile_path)
file_size_mb = file_size_bytes / (1024 * 1024)
print(f"\n11>>> RxNorm \033[33;1mFile size\033[0m: {file_size_mb:.2f} MB")

# Extracted Memory usage
print (f"\n     >>> Extracted File \033[33;1mMemory usage\033[0m: {shortrxnorm.memory_usage(deep=True).sum() / 1024**2:.2f} MB\n") # different from polars

# End Timestamp
end_time_pandas = time.time()
# Elapsed Time
rxnorm_pandas = pd.read_csv(inputfile_path, nrows=10000, encoding_errors="ignore", on_bad_lines='skip')
elapsed_time_pandas = end_time_pandas - start_time_pandas
# Print total elapsed time
print(f" ------ \033[33;1mTotal Elapsed time:\033[0m \033[32;1m {elapsed_time_pandas:.3f} seconds \033[0m------\n")

gc.collect()