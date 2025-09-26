# Using pandas, 100K rows, output is a a panda csv file and a parquet csv file
import pandas as pd
from datetime import datetime
from collections import Counter
import os 
import gc

import time
# Start Timestamp
start_time_pandas = time.time()

# input file path
inputfile_path = "input/snomeddata.txt"

# output file path
outputfile_path = "output/snomed/snomed.csv"
outputfilepd_path = "output/snomed/snomed_pd.csv"
outputfilepq_path = "output/snomed/snomed_pq.csv"

pd.set_option('display.max_columns', None)

snomed = pd.read_csv(inputfile_path, sep='\t', nrows=100000)

snomed.to_csv("output/snomed/snomed_raw.csv", index=False)

print(f"\n1>>> Successfully \033[33;1mLOADED\033[0m  {len(snomed)} records from SNOMED data")

print(f"\n2>>> SNOMED Dataset \033[33;1mSHAPE\033[0m: {snomed.shape}")

print(f"\n3>>> SNOMED \033[33;1mFILE INFO\033[0m\n") # basic info: range index, data columns (total columns, index, column headers, non-null count, dtype, memory usage)
snomed.info()

#  Print Unique data types and count of each dtype
dtype_counts = Counter(str(dtype) for dtype in snomed.dtypes)
print(f"\n      >>> \033[33;1mUnique data types and counts\033[0m: {dict(dtype_counts)}")

print(f"\n4>>> SNOMED \033[33;1mILOC\033[0m \n\n{snomed.iloc[0]}") # display contents of first column; snapshots row contents

print(f"\n5>>> \033[33;1mFIRST FIVE ROWS\033[0m Raw SNOMED File\n:")
print(snomed.head())

snomed[['id', 'term']]
shortsnomed = snomed[['id', 'term']].copy()
shortsnomed['Last_updated'] = datetime.today().strftime('%m-%d-%Y')

shortsnomed = shortsnomed.rename(columns={
    'id': 'Code',
    'term': 'Description'
    })

# Describe for descriptive stats
print(f"\n >>> \033[32;1mDescribe - Raw File ??? \033[0m\n{snomed.describe()}")

print("\n6>>>... \033[35;1mRaw SNOMED file transformed to Extracted file ...\033[0m\n with columns \033[33;1m'Code', 'Description' and 'Last_updated'\033[0m")

# Describe for descriptive stats
print(f"\n >>> \033[32;1mDescribe - Extracted File ??? \033[0m\n{shortsnomed.describe()}")

#### Remove duplicate rows
rows_before = len(shortsnomed)
shortsnomed_no_duplicates = shortsnomed.drop_duplicates()
rows_after = len(shortsnomed_no_duplicates)
duplicates_removed = rows_before - rows_after

print(f"\n      >>> \033[33;1mDuplicates removed: ??? \033[0m {duplicates_removed}")

# Filter out empty or null descriptions
shortsnomed = shortsnomed[
    shortsnomed['Description'].notna() &
    (shortsnomed['Description'].str.strip() != "")
    ]

#### Count null Descriptions
null_count = shortsnomed['Description'].isnull().sum()
print(f"\n      >>> \033[33;1mNumber of null Descriptions\033[0m: {null_count}")

#### Count empty strings
empty_count = (shortsnomed['Description'] == '').sum()
print(f"\n      >>> \033[33;1mNumber of empty Descriptions\033[0m: {empty_count}")

print(f"\n7>>> Successfully \033[33;1mPARSED:\033[0m {len(shortsnomed)} records from Raw file")

# Extract csv file with 'Code', 'Description' and 'Last_updated' columns
shortsnomed.to_csv(outputfilepd_path, index=False)
shortsnomed.to_parquet(outputfilepq_path, index=False)

print(f"\n      >>> Transformed as a \033[33;1mPARQUET File:\033[0m")

print(f"\n8>>> SNOMED Extracted file \033[33;1mSAVED\033[0m to{'outputfilepq_path'}") 

print(f"\n9>>> SNOMED Dataset \033[33;1mSHAPE\033[0m: {shortsnomed.shape}")

print(f"\n10>>> \033[33;1mFIRST FIVE ROWS\033[0m Extracted SNOMED File ")
print(shortsnomed.head())

# input file size
inputfile_size_bytes = os.path.getsize(inputfile_path)
inputfile_size_mb = inputfile_size_bytes / (1024 * 1024)
print(f"\n11>>> Raw SNOMED \033[33;1mFile size\033[0m: {inputfile_size_mb:.2f} MB")

# Input file Memory usage 
print (f"\n     >>> Raw File \033[33;1mMemory usage\033[0m: {snomed.memory_usage(deep=True).sum() / 1024**2:.2f} MB") # different from polars

# extracted File size
file_size_bytes = os.path.getsize("output/snomed/snomed_pq.csv")
file_size_mb = file_size_bytes / (1024 * 1024)
print(f"\n12>>> Extracted SNOMED \033[33;1mFile size\033[0m: {file_size_mb:.2f} MB")

# Extracted file Memory usage
print (f"\n     >>> Extracted File \033[33;1mMemory usage\033[0m: {shortsnomed.memory_usage(deep=True).sum() / 1024**2:.2f} MB\n") # different from polars

# End Timestamp
end_time_pandas = time.time()
# Elapsed Time
snomed_pandas = pd.read_csv(inputfile_path, nrows=10000, encoding_errors="ignore", on_bad_lines='skip')
elapsed_time_pandas = end_time_pandas - start_time_pandas
# Print total elapsed time
print(f" ------ \033[33;1mTotal Elapsed time:\033[0m \033[32;1m {elapsed_time_pandas:.3f} seconds \033[0m------\n")

gc.collect() 