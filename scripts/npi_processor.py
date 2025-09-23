import polars as pl
from tabulate import tabulate # first pip install tabulate
from collections import Counter
import os
import gc 

npi_file_path = "input/npidata.csv"
npi = pl.read_csv(npi_file_path, n_rows=100000)

print(f"\nSuccessfully \033[34;1;4mLOADED\033[0m {len(npi)} records from NPI data")
print(f"\nDataset \033[34;1;4mSHAPE\033[0m {npi.shape}")

####
# Total columns
num_columns = npi.width
print(f"\n\033[34;1;4mCOLUMNS\033[0m: {num_columns}")
# Total rows
num_rows = npi.height
print(f"\033[34;1;4mROWS\033[0m: {num_rows}")

#####
# Define Unique data types
all_dtypes = npi.dtypes 
unique_dtypes = (set(all_dtypes))

#  Print Unique data types and count of each dtype
dtype_counts = Counter(str(dtype) for dtype in npi.dtypes)
print(f"\n\033[34;1;4mUnique data types and counts\033[0m: {dict(dtype_counts)}")

# with Describe give stats
print(f"\n\033[34;1;4mDescribe\033[0m, {npi.describe()}")

# print(f"Columns: {npi.columns}") ... prints a cluttered column list
# print(tabulate([npi.columns], tablefmt='grid')) ... no good

# Print columns vertically (one-per-line): to help in selecting columns for npi_small below
print(f"\n\033[34;1;4mCOLUMNS\033[0m from NPI data\n")

##### 
# print truncated column header list
for col in npi.columns [:20]:
    print(col)

print(f"\n\033[34;1;4mFirst 5 Rows\033[0m Raw NPI File\n")
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
output_path = "output/npi_small.csv"
npi_small.write_csv(output_path)

print(f"\nCreated a copy with columns \033[34;1;4m'Code', 'Description' and 'Last_updated'\033[0m")

### Make Parquet file to decrease file size for big data sets
npi_small.write_parquet("output/npi_small.parquet")

print(f"\n\033[34;1;4mFirst 5 Rows\033[0m (Extracted NPI File) \n")
print(npi_small.head())

# File size
file_size_bytes = os.path.getsize("output/npi_small.parquet")
file_size_mb = file_size_bytes / (1024 * 1024)
print(f"\nExtracted NPI \033[34;1;4mFILE SIZE\033[0m: {file_size_mb:.2f} MB")

# Memory usage
print(f"\n\033[34;1;4mMemory usage (MB)\033[0m: {npi.estimated_size() / 1024**2:.2f}\n") # different from pandas

gc.collect()