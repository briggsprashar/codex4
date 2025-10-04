# Using pandas, 30K rows, output is a a panda csv file and a parquet csv file
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
outputfile_path = "output/snomed/snomed_pq.csv"
outputfilepd_path = "output/snomed/snomed_pd.csv"
outputfilepq_path = "output/snomed/snomed_pq.csv"

pd.set_option('display.max_columns', None)

# Define df / basic info / preview 
# Snomed ct data (tab-delimited, limited to 100,000)
snomed = pd.read_csv(inputfile_path, sep='\t', nrows=100000)
# dtype=pl.Utf8

print(f"\n1>>> Successfully \033[33;1mLOADED\033[0m {len(snomed)} SNOMED records")

print(f"\n2>>> SNOMED Dataset \033[33;1mSHAPE\033[0m: {snomed.shape}\n")

# Total columns
num_columns = snomed.shape[1]
print(f"      >>> \033[33;1mCOLUMNS\033[0m: {num_columns}")

# Total rows
num_rows = snomed.shape[0]
print(f"      >>> \033[33;1mROWS\033[0m: {num_rows}")

print(f"\n3>>> SNOMED \033[33;1mFILE INFO\033[0m\n") # basic info: range index, data columns (total columns, index, column headers, non-null count, dtype, memory usage)
snomed.info()

#  Print Unique data types and count of each dtype
dtype_counts = Counter(str(dtype) for dtype in snomed.dtypes)
print(f"\n      >>> \033[33;1mUnique data types and counts\033[0m: {dict(dtype_counts)}")

row = snomed.iloc[10]  # get the row as Series
print(f"\n4>>> SNOMED \033[33;1mILOC\033[0m \n\n{row[:10]}\n")

print(f"\n5>>> SNOMED (Raw File) \033[33;1mFIRST 5 ROWS  \033[0m\n:")
print(snomed.head())

# commands with polars
# snomed = pl.read_csv('input\snomeddata.txt', separator='\t', n_rows=10000, truncate_ragged_lines=True, ignore_errors=True)
# print(snomed.schema) # shows column names and their data types
# print(snomed.shape) # shows number of rows and columns
# print(snomed.head(n=5)) # shows first 5 rows

# Explore key columns
snomed['id']
snomed['term']

# CREATE a trimmed DataFrame with selected columns and assign it to a new VARIABLE
    # use of double square brackets to select multiple columns
    # use of copy() to create a copy of the selected columns
shortsnomed = snomed[['id', 'term']].copy()

# ADD a timestamp column for tracking updates with today's date in 'MM-DD-YYYY' format instead of a hardcoded timestamp
shortsnomed['Last_updated'] = datetime.today().strftime('%m-%d-%Y')

# Rename columns for clarity and consistency
shortsnomed = shortsnomed.rename(columns={
    'id': 'Code',
    'term': 'Description'
    })

# Describe for descriptive stats
print(f"\n >>> \033[32;1mDescribe - Raw File ??? \033[0m\n{snomed.describe()}")

print("\n6>>>... \033[35;1mRaw SNOMED file transformed and extracted ...\033[0m\nwith columns \033[33;1m'Code', 'Description' and 'Last_updated'\033[0m")

print(f"\n >>> \033[32;1mDescribe - Extracted File ??? \033[0m\n{shortsnomed.describe()}")

# Remove duplicate rows
shortsnomed = shortsnomed.drop_duplicates()

# Filter out empty or null descriptions
shortsnomed = shortsnomed[
    shortsnomed['Description'].notna() &
    (shortsnomed['Description'].str.strip() != "")
    ]

#### Count null Descriptions
null_count = shortsnomed['Description'].isnull().sum()
print(f"    >>> Number of null Descriptions: {null_count}")

#### Count empty strings
empty_count = (shortsnomed['Description'] == '').sum()
print(f"    >>> Number of empty Descriptions: {empty_count}")

# Ignore BAD LINES
bad_lines_count = 0
def bad_line_handler(bad_line):
    global bad_lines_count
    bad_lines_count += 1
    # Return None to skip the bad line
    return None
# Use engine='python' when using a callable for on_bad_lines
# snomed = pd.read_csv(file_path, dtype=str, sep=r'\s+', engine='python', on_bad_lines=bad_line_handler) # Multi index output!!
#print(f"\n  >>> Number of ICD10US\033[34;1;4mBad Lines Skipped\033[0m: {bad_lines_count}")

print(f"\n7>>> Successfully \033[33;1mPARSED:\033[0m {len(shortsnomed)} records from Raw file")

# Extract csv file with 'Code', 'Description' and 'Last_updated' columns
shortsnomed.to_csv(outputfilepd_path, index=False)
shortsnomed.to_parquet(outputfilepq_path, index=False)

print(f"\n      >>> Extracted as a \033[33;1mPARQUET File:\033[0m")

print(f"\n8>>> \033[33;1mSAVED\033[0m to {'outputfilepq_path'}") 
print(f"\n9>>> Dataset \033[33;1mSHAPE:\033[0m {shortsnomed.shape}")
print(f"\n10>>> \033[33;1mPreview First few Rows\033[0m (Extracted SNOMED File) \n\n {shortsnomed.head()}")

# input file size
inputfile_size_bytes = os.path.getsize(inputfile_path)
inputfile_size_mb = inputfile_size_bytes / (1024 * 1024)
print(f"\n11>>> Raw HCPC \033[33;1mFile size\033[0m: {inputfile_size_mb:.2f} MB")

# Memory usage
print(f"\n      >>> Raw File \033[33;1mMemory usage\033[0m: {snomed.memory_usage(deep=True).sum() / 1024**2:.2f} MB") # different from polars

# extractedFile size
file_size_bytes = os.path.getsize(outputfilepq_path)
file_size_mb = file_size_bytes / (1024 * 1024)
print(f"\n12>>> Extracted \033[33;1mFile size\033[0m: {file_size_mb:.2f} MB")

# Memory usage
print(f"\n      >>> Extracted File \033[33;1mMemory usage (MB)\033[0m: {shortsnomed.memory_usage(deep=True).sum() / 1024**2:.2f} MB\n") # different from polars

print(f"      >>> \033[33;1mActive Terms\033[0m count: {snomed[snomed['active'] == 1].shape[0]}\n")
print(f"      >>> \033[33;1mLanguage\033[0m codes: {snomed['languageCode'].unique().tolist()}\n")


# End Timestamp
end_time_pandas = time.time()
# Elapsed Time
hcpc_df_pandas = pd.read_csv(inputfile_path, nrows=10000, encoding_errors="ignore", on_bad_lines='skip')
elapsed_time_pandas = end_time_pandas - start_time_pandas

# Print total elapsed time
print(f">>>>>> \033[33;1mTotal Elapsed time:\033[0m \033[32;1m {elapsed_time_pandas:.3f} seconds \033[0m<<<<<<\n")

snomed = None
del snomed  
shortsnomed = None
del shortsnomed

gc.collect()