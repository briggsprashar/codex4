import polars as pl
from tabulate import tabulate # first pip install tabulate
from collections import Counter
import os
import gc 

import time
# Start Timestamp
start_time_pandas = time.time()

inputfile_path = "input/npidata.csv"
outputfile_path = "output/npi_small.parquet"
npi = pl.read_csv(inputfile_path, n_rows=100000)

print(f"\n1>>> Successfully \033[33;1mLOADED\033[0m {len(npi)} records from NPI data")

print(f"\n2>>> Dataset \033[33;1mSHAPE\033[0m {npi.shape}")

####
# Total columns
num_columns = npi.width
print(f"      >>> \033[33;1mCOLUMNS\033[0m: {num_columns}")
# Total rows
num_rows = npi.height
print(f"      >>> \033[33;1mROWS\033[0m: {num_rows}")

#####
# Define Unique data types
all_dtypes = npi.dtypes 
unique_dtypes = (set(all_dtypes))

#  Print Unique data types and count of each dtype
dtype_counts = Counter(str(dtype) for dtype in npi.dtypes)
print(f"\n>>> \033[33;1mUnique data types and counts\033[0m: {dict(dtype_counts)}")

# print(f"Columns: {npi.columns}") ... prints a cluttered column list
# print(tabulate([npi.columns], tablefmt='grid')) ... no good

# Print columns vertically (one-per-line): to help in selecting columns for npi_small below
print(f"\n>>> \033[33;1mCOLUMNS\033[0m from NPI data\n")

##### 
# print truncated column header list
for col in npi.columns [:20]:
    print(col)

print(f"\n>>> \033[33;1mFirst 5 Rows\033[0m Raw NPI File\n")
print(npi.head())

# Select columns
npi_small = npi.select([
    'NPI', 
    'Provider Last Name (Legal Name)'
    ])

# Rename columns
npi_small = npi_small.with_columns(
    pl.lit('2025-09-17').alias('Last_updated')
    )

npi_small = npi_small.rename({
    'NPI': 'Code',
    'Provider Last Name (Legal Name)': 'Description',
    })

# Extract parsed file
npi_small.write_csv(outputfile_path)

# Describe for descriptive stats
print(f"\n>>> \033[32;1mDescribe - Raw File ???\033[0m, {npi.describe()}")

print(f"\n>>> ... \033[35;1m Raw NPI file transformed and extracted ...\033[0m  \nwith columns \033[33;1m'Code', 'Description' and 'Last_updated'\033[0m")

print(f"\n>>> \033[32;1mDescribe - Extracted File ???\033[0m, {npi_small.describe()}")

print(f"\n>>> Successfully \033[33;1mPARSED\033[0m {npi.height} LOINC records from {inputfile_path}")

print(f"\n>>> Dataset \033[33;1mSHAPE\033[0m {npi_small.shape}")

print(f"\n>>> \033[33;1mFIRST 5 ROWS (Extracted LOINC File):\033[0m\n")
print(npi_small.head())

### Make Parquet file to decrease file size for big data sets
npi_small.write_parquet("output/npi_small.parquet")

# input file size
inputfile_size_bytes = os.path.getsize(inputfile_path)
inputfile_size_mb = inputfile_size_bytes / (1024 * 1024)
print(f"\n>>> Raw NPI \033[33;1mFile size\033[0m: {inputfile_size_mb:.2f} MB")

# Input Memory usage
print(f"\n      >>> \033[33;1mMemory usage\033[0m: {npi.estimated_size() / 1024**2:.2f} MB\n") # different from pandas

# extracted File size
file_size_bytes = os.path.getsize(outputfile_path)
file_size_mb = file_size_bytes / (1024 * 1024)
print(f">>> Extracted NPI \033[33;1mFILE SIZE\033[0m: {file_size_mb:.2f} MB")

# Extracted Memory usage
print(f"\n      >>> \033[33;1mMemory usage\033[0m: {npi_small.estimated_size() / 1024**2:.2f} MB\n") # different from pandas

print(f"\nMemory usage (MB): {df.estimated_size() / 1024**2:.2f}")

# End Timestamp
end_time_pandas = time.time()
# Elapsed Time
# npi_pandas = pl.read_csv(inputfile_path, n_rows=10000) # encoding_errors="ignore", on_bad_lines='skip')
elapsed_time_pandas = end_time_pandas - start_time_pandas
# Print total elapsed time
print(f" ------ \033[33;1mTotal Elapsed time:\033[0m \033[32;1m {elapsed_time_pandas:.3f} seconds \033[0m------\n")

npi = None
del npi
npi_small = None
del npi_small

gc.collect()