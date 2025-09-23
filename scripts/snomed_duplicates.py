# Using pandas, 30K rows, output is a a panda csv file and a parquet csv file
import pandas as pd
from datetime import datetime
import os 
import gc

snomed = pd.read_csv('input/snomeddata.txt', sep='\t', nrows=100000)

print(f"\nSuccessfully \033[34;1;4mLOADED\033[0m  {len(snomed)} records from SNOMED data")

print(f"\nSNOMED \033[34;1;4mFILE INFO\033[0m\n") # basic info: range index, data columns (total columns, index, column headers, non-null count, dtype, memory usage)
snomed.info()

print(f"\n\033[34;1;4mFIRST FIVE ROWS (Raw SNOMED File):\033[0m\n:")
print(snomed.head())


snomed[['id', 'term']]
shortsnomed = snomed[['id', 'term']].copy()
shortsnomed['Last_updated'] = datetime.today().strftime('%m-%d-%Y')

shortsnomed = shortsnomed.rename(columns={
    'id': 'Code',
    'term': 'Description'
    })

print(f"\nCreated a copy with columns \033[34;1;4m'Code', 'Description' and 'Last_updated'\033[0m")

#### Remove duplicate rows
rows_before = len(shortsnomed)
shortsnomed_no_duplicates = shortsnomed.drop_duplicates()
rows_after = len(shortsnomed_no_duplicates)
duplicates_removed = rows_before - rows_after

print(f"\n\033[34;1;4mDuplicates removed: ??? \033[0m {duplicates_removed}")

#### Count null Descriptions
null_count = shortsnomed['Description'].isnull().sum()
print(f"\n\033[34;1;4mNumber of null Descriptions\033[0m: {null_count}")

#### Count empty strings
empty_count = (shortsnomed['Description'] == '').sum()
print(f"\n\033[34;1;4mNumber of empty Descriptions\033[0m: {empty_count}")

# Filter out empty or null descriptions
shortsnomed = shortsnomed[
    shortsnomed['Description'].notna() &
    (shortsnomed['Description'].str.strip() != "")
    ]
print(f"\n\033[34;1;4mSuccessfully PARSED:\033[0m {len(shortsnomed)} records from snomeddata.txt")

# Extract csv file with 'Code', 'Description' and 'Last_updated' columns
shortsnomed.to_csv("output/snomed/snomed_pd.csv", index=False)
shortsnomed.to_parquet("output/snomed/snomed_pq.csv", index=False)


print(f"\nSNOMED Dataset \033[34;1;4mSHAPE\033[0m: {shortsnomed.shape}")
print(f"\n\033[34;1;4mFIRST FIVE ROWS\033[0m (Extracted SNOMED File) ")
print(shortsnomed.head())

print(f"\n\033[34;1;4mSAVED\033[0m to {'output/snomed/snomed_pq.csv'}") 

# File size
file_size_bytes = os.path.getsize("output/snomed/snomed_pq.csv")
file_size_mb = file_size_bytes / (1024 * 1024)
print(f"\nExtracted SNOMED \033[34;1;4mFile size\033[0m: {file_size_mb:.2f} MB")

# Memory usage
print (f"\n\033[34;1;4mMemory usage (MB)\033[0m: {snomed.memory_usage(deep=True).sum() / 1024**2:.2f}\n") # different from polars

gc.collect() 