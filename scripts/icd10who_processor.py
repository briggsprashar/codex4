import pandas as pd 
from datetime import datetime
import openpyxl as pxl
from collections import Counter
import os
import gc
import time

# Start Timestamp
start_time_pandas = time.time()

# Input file path
inputfile_path = "input/icd10who.txt"

# output file path
outputfile_path = "output\\icd10who\\icd10who_final.csv"

pd.set_option('display.max_columns', None)

icd10who_df = pd.read_csv(inputfile_path, header=None, sep=';')
print(f"\n>>> \033[33;1mRaw csv length\033[0m: {len(icd10who_df)}")

#################
# Ignore BAD LINES
bad_lines_count = 0
def bad_line_handler(bad_line):
    global bad_lines_count
    bad_lines_count += 1
    # Return None to skip the bad line
    return None

# Dataframe using engine='python' to call "on_bad_lines"
icd10who2_df = pd.read_csv(inputfile_path, dtype=str, sep=r'\s+', engine='python', on_bad_lines=bad_line_handler) # Multi index output!!
print(f"\n>>> length after \033[33;1mBad line removed\033[0m: {len(icd10who2_df)}")

# print bad lines count
print(f"\n>>> Number of ICD10WHO \033[33;1mBad Lines Skipped\033[0m: {bad_lines_count}")
#################

print(f"\n1>>> Successfully \033[33;1mLOADED\033[0m {len(icd10who_df)} ICD10WHO records")

print(f"\n2>>> ICD10WHO Dataset \033[33;1mSHAPE:\033[0m {icd10who_df.shape}")

# Total columns
num_columns = icd10who_df.shape[1]
print(f"      >>> \033[33;1mCOLUMNS\033[0m: {num_columns}")

# Total rows
num_rows = icd10who_df.shape[0]
print(f"      >>> \033[33;1mROWS\033[0m: {num_rows}")

# Info*()
print(f"\n2>>> ICD10WHO Dataset \033[33;1mFILE INFO\033[0m\n") # basic info: range index, data columns (total columns, index, column headers, non-null count, dtype, memory usage)
icd10who_df.info()

#  Print Unique data types and count of each dtype
dtype_counts = Counter(str(dtype) for dtype in icd10who_df.dtypes)
print(f"\n        >>>\033[33;1m Unique data types and counts\033[0m: {dict(dtype_counts)}")

# ILOC
print(f"\n4>>> ICD10WHO Raw File \033[33;1m ILOC\033[0m \n\n{icd10who_df.iloc[0]}") # display contents of first column; snapshots row contents
# icd10cm_df.info(verbose=True, show_counts=True)

# preview 2st 5 rows raw file
print("\n3>>> ICD10WHO \033[33;1mFIRST 5 ROWS (Raw File)\033[0m\n")
print(icd10who_df.head())

# Output raw file as csv to view
icd10who_df.to_csv("output\\icd10who\\icd10who_raw1.csv") 

columns = ['level', 'type', 'usage', 'sort', 'parent', 'code', 'display_code',  'icd10_code', 'title_en', 'parent_title', 'detailed_title', 
           'definition', 'mortality_code', 'morbidity_code1', 'morbidity_code2', 'morbidity_code3', 'morbidity_code4'
           ]

icd10who_df = pd.read_csv(inputfile_path, header=None, sep=';', names=columns)

# preview 2st 5 rows after renaming columns
print("\n4.1>>> ICD10WHO \033[33;1mFIRST 5 ROWS (Columns Renamed)\033[0m\n")
print(icd10who_df.head())

pd.reset_option('display.max_columns') # disables > pd.set_option('display.max_columns', None)

# Describe raw file
print(f"\n >>> \033[32;1mDescribe - Raw File ??? \033[0m\n{icd10who_df.describe()}")

# Remove duplicate rows if any keeping the first occurrence
icd10who_df = icd10who_df.drop_duplicates()

# Explore processed raw file with column headers and no index
icd10who_df.to_csv("output\\icd10who\\icd10who_raw2.csv", index=False)

# CREATE a trimmed DataFrame with selected columns and assign it to a new VARIABLE
    # use of double square brackets to select multiple columns
    # use of copy() to create a copy of the selected columns
shorticd10who = icd10who_df[['display_code', 'detailed_title']].copy()

# add column last updated
shorticd10who['Last_updated'] = datetime.today().strftime('%m-%d-%Y') # Add new column with today's date

# Rename columns for clarity and consistency
shorticd10who= shorticd10who.rename(columns={
            "display_code": 'Code',
            "detailed_title": 'Description'
            })

# print message
print("\n5>>>... \033[33;1mRaw ICD10WHO file transformed to Extracted file ...\033[0m\n with columns \033[33;1m'Code', 'Description' and 'Last_updated'\033[0m")

# Describe extracted file
print(f"\n >>> \033[32;1mDescribe - Extracted File ??? \033[0m\n{shorticd10who.describe()}")

# REMOVE empty descriptions/blanks/NaN values   PRINT EMPTY REMOVED --------------
shorticd10who = shorticd10who[
    shorticd10who['Description'].notna() & 
    (shorticd10who['Description'].str.strip() != '')
    ]

# preview 2st 5 rows of extracted file
print(f"\n6>>> Preview \033[33;1mFIRST few ROWS (Extracted ICD10WHO File):\033[0m\n")
print(shorticd10who.head(20))

# parsed msg
print(f"\n7>>> Successfully \033[33;1mPARSED\033[0m {len(shorticd10who)} ICD10WHO records from {inputfile_path}")

# Extract csv file with 'display_code', 'detailed_title' and 'last_updated' columns
shorticd10who.to_csv(outputfile_path, index=False)

# extracted file output location
print(f"\n8>>> \033[33;1mSAVED\033[0m to {"outputfile_path"}")

# extracted file Shape
print(f"\n9>>> ICD10WHO Dataset \033[33;1mSHAPE:\033[0m {shorticd10who.shape}")

# Input file size
inputfile_size_bytes = os.path.getsize("input/icd10who.txt")
inputfile_size_mb = inputfile_size_bytes / (1024 * 1024)
print(f"\n10>>> Raw HCPC \033[33;1mFile size\033[0m: {inputfile_size_mb:.2f} MB")

# Input File Memory usage
print (f"\n     >>> \033[33;1mMemory usage\033[0m: {icd10who_df.memory_usage(deep=True).sum() / 1024**2:.2f} MB\n") # different from polars

# Extracted file size
file_size_bytes = os.path.getsize(outputfile_path)
file_size_mb = file_size_bytes / (1024 * 1024)
print(f"11>>> Extracted ICD10WHO\033[33;1mFile size\033[0m: {file_size_mb:.2f} MB")

# Extracted File Memory usage
print (f"\n     >>> \033[33;1mMemory usage\033[0m: {shorticd10who.memory_usage(deep=True).sum() / 1024**2:.2f} MB\n") # different from polars

# End Timestamp
end_time_pandas = time.time()
# Elapsed Time
icd10who_df_pandas = pd.read_csv(inputfile_path, nrows=10000, encoding_errors="ignore", on_bad_lines='skip')
elapsed_time_pandas = end_time_pandas - start_time_pandas
# Print total elapsed time
print(f" ------ \033[33;1mTotal Elapsed time:\033[0m \033[32;1m {elapsed_time_pandas:.3f} seconds \033[0m------\n")

gc.collect()