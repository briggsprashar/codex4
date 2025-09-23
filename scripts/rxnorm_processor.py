import pandas as pd
from datetime import datetime
import os
import gc

rxnorm = pd.read_csv("input\\RXNSAT.RRF", nrows=100000,
    sep="|",        # pipe-delimited in raw file
    header=None,    # no headers in raw file
    dtype=str)      # can also use e before file path above to identify raw string data

print(f"\nSuccessfully \033[34;1;4mLOADED\033[0m {len(rxnorm)} records")

print(f"\nRxNorm \033[34;1;4mFILE INFO\033[0m\n") # basic info: range index, data columns (total columns, index, column headers, non-null count, dtype, memory usage)
rxnorm.info() 

print(f"\nRxNorm \033[34;1;4mILOC\033[0m \n\n{rxnorm.iloc[0]}") # display contents of first column; snapshots row contents

print(f"\n\033[34;1;4mFIRST FIVE ROWS (Raw RxNorm File):\033[0m\n:")
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

print(f"\nCreated a copy with columns \033[34;1;4m'Code', 'Description' and 'Last_updated'\033[0m")

print(f"\n\033[34;1;4mSuccessfully PARSED:\033[0m {len(shortrxnorm)} records from RXNATOMARCHIVE.RRF")

# Remove duplicate rows
rows_before = len(shortrxnorm)
shortrxnorm_no_duplicates = shortrxnorm.drop_duplicates()
rows_after = len(shortrxnorm_no_duplicates)
duplicates_removed = rows_before - rows_after

print(f"\n\033[34;1;4mDuplicates removed: ??? \033[0m {duplicates_removed}")

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
shortrxnorm.to_csv(r'output\rxnorm_short\rx_short.csv', sep='\t', index=False, header=True)

print(f"\nRxNorm Dataset \033[34;1;4mSHAPE\033[0m: {shortrxnorm.shape}")
print(f"\n\033[34;1;4mFIRST FIVE ROWS\033[0m: (Extracted RxNorm File)\n")
print(shortrxnorm.head())

print(f"\n\033[34;1;4mSAVED\033[0m to {'output/rxnorm/rxnorm.csv'}") # \r conflicts with another function, so use \\r or /r
# its better to create capture "input_path" and "output_path" in an object for reusability

# File size
file_size_bytes = os.path.getsize(r"output\rxnorm_short\rx_short.csv")
file_size_mb = file_size_bytes / (1024 * 1024)
print(f"\nRxNorm \033[34;1;4mFile size\033[0m: {file_size_mb:.2f} MB")

# Memory usage
print (f"\n\033[34;1;4mMemory usage (MB)\033[0m: {rxnorm.memory_usage(deep=True).sum() / 1024**2:.2f}\n") # different from polars

gc.collect()