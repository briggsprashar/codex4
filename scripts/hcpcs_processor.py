# Using pandas explored and transformed input raw xlsx data file to output as a.csv file.
# to see raw file, to make raw file readable, and to extract needed columns from raw file and add a column to final extracted file
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
inputfile_path = "input\\HCPC.xlsx"

# output file path
outputfile_path = "output\\hcpc\\hcpc_final.csv"

# cols not truncated
# pd.set_option('display.max_columns', None)

# Dataframe
hcpc_df = pd.read_excel(inputfile_path) # Define df

# Loaded
print(f"\n1>>> Successfully \033[33;1mLOADED\033[0m {len(hcpc_df)} HCPC records")

# raw file Shape
print(f"\n2>>> HCPC Dataset \033[33;1mSHAPE:\033[0m {hcpc_df.shape}")

# Total columns
num_columns = hcpc_df.shape[1]
print(f"      >>> \033[33;1mCOLUMNS\033[0m: {num_columns}")

# Total rows
num_rows = hcpc_df.shape[0]
print(f"      >>> \033[33;1mROWS\033[0m: {num_rows}")

# print info()
print(f"\n3>>> HCPC \033[33;1mFILE INFO\033[0m\n") # basic info: range index, data columns (total columns, index, column headers, non-null count, dtype, memory usage)
hcpc_df.info()

# Unique data types and count
dtype_counts = Counter(str(dtype) for dtype in hcpc_df.dtypes)
print(f"\n      >>> \033[33;1mUnique data types and counts\033[0m: {dict(dtype_counts)}")

# ILOC
# get custom no of row as series
row = hcpc_df.iloc[30]  
print(f"\n4>>> HCPC Customizable\033[33;1mILOC\033[0m \n\n{row[:10]}") 
# get all rows as series
print(f"\n      >>>> HCPC WHole \033[34;1;4m ILOC\033[0m \n\n{hcpc_df.iloc}")
print(hcpc_df.iloc[0]) 

# First 5 row preview
print("\n5>>> HCPC (Raw File) \033[33;1mFIRST 5 ROWS \033[0m\n")
print(hcpc_df.head())   # preview first 5 rows with truncated column snapshot; 5 rows and x columns

# save raw file to explore
# HCPC RAW
hcpc_df.to_csv("output\\hcpc\\hcpc_raw1.csv") # raw file has headers and is comma separated (cluttered)
# HCPC2 RAW tab separated
hcpc_df.to_csv("output\\hcpc\\hcpc_raw2.csv", sep='\t', index=False, header=True) # Explore as tab separated csv file

# identify columns
hcpc_df[['HCPC', 'LONG DESCRIPTION','SHORT DESCRIPTION']] # Identify 3 columns to extract/explore 

# alt "colspecs" not done

# create copy, rename, add column
shorthcpc = hcpc_df[['HCPC', 'LONG DESCRIPTION']].copy() # Extract 2 columns to new df; "copy()" to create a copy from original file with the selected columns
shorthcpc = shorthcpc.rename(columns={'HCPC': 'Code', 'LONG DESCRIPTION': 'Description'}) # Rename columns: 'Code', 'Description' and 'Last_updated'
shorthcpc['Last_updated'] = datetime.today().strftime('%Y-%m-%d') # Add new column with today's date

# disable columns not truncated
pd.reset_option('display.max_columns') # disables line 14> pd.set_option('display.max_columns', None)

# Describe raw file
print(f"\n >>> \033[32;1mDescribe - Raw File ???\033[0m\n{hcpc_df.describe()}")

# print message 
print("\n6>>> ... \033[35;1m Raw HCPC file transformed to extracted\033[0m  ...\nwith columns \033[33;1m'Code', 'Description' and 'Last_updated'\033[0m")

# Describe extracted file
print(f"\n >>> \033[32;1mDescribe - Extracted File ???\033[0m\n{shorthcpc.describe()}")

# Remove duplicate rows
# shorthcpc = hcpc_df.drop_duplicates()

# Filter out empty or null descriptions
shorthcpc = shorthcpc[
    shorthcpc['Description'].notna() &
    (shorthcpc['Description'].str.strip() != "")
    ]
print(f"\n7>>> Successfully \033[33;1mPARSED\033[0m {len(hcpc_df)} HCPC records from {inputfile_path}")

# HCPC3 final file Extracted
shorthcpc.to_csv(outputfile_path, sep='\t', index=False, header=True) # Extract to a csv file with 3 columns
print(f"\n8>>> HCPC Extracted file \033[33;1mSAVED\033[0m to {outputfile_path}") 

# extracted file Shape
print(f"\n9>>> HCPC Dataset \033[33;1mSHAPE:\033[0m {shorthcpc.shape}")

print(f"\n10>>> \033[33;1mPreview First few Rows\033[0m (Extracted HCPC File) \n\n {shorthcpc.head()}")

# pd.reset_option('display.max_columns') # disables > pd.set_option('display.max_columns', None)

# input file size
inputfile_size_bytes = os.path.getsize(inputfile_path)
inputfile_size_mb = inputfile_size_bytes / (1024 * 1024)
print(f"\n11>>> Raw HCPC \033[33;1mFile size\033[0m: {inputfile_size_mb:.2f} MB")

# Memory usage
print (f"\n     >>>Raw File \033[33;1mMemory usage \033[0m: {hcpc_df.memory_usage(deep=True).sum() / 1024**2:.2f} MB\n") # different from polars

# extracted file size
file_size_bytes = os.path.getsize(outputfile_path)
file_size_mb = file_size_bytes / (1024 * 1024)
print(f"12>>> Extracted HCPC \033[33;1mFile size\033[0m: {file_size_mb:.2f} MB")

# Memory usage
print (f"\n     >>> Extracted File \033[33;1mMemory usage\033[0m: {shorthcpc.memory_usage(deep=True).sum() / 1024**2:.2f} MB\n") # different from polars

# End Timestamp
end_time_pandas = time.time()

# Elapsed Time
# hcpc_df_pandas = pd.read_csv(inputfile_path, nrows=10000, encoding_errors="ignore", on_bad_lines='skip')
elapsed_time_pandas = end_time_pandas - start_time_pandas

# Print total elapsed time
print(f" ------ \033[33;1mTotal Elapsed time:\033[0m \033[32;1m {elapsed_time_pandas:.3f} seconds \033[0m------\n")

hcpc_df = None
del hcpc_df
shorthcpc = None    
del shorthcpc

gc.collect()

# print("hcpc_df.isnull().sum()\n")
# print(shorthcpc.isnull().sum())
# print(hcpc_df.describe(include='all'))
# print(shorthcpc.describe(include='all'))
# print(f"\033[33;1mActive Terms\033[0m count: {shorthcpc[shorthcpc['Code'] == 1].shape[0]}\n")
# print(f"\033[33;1mLanguage\033[0m codes: {hcpc_df['LONG DESCRIPTION'].unique().tolist()}\n")
# print(shorthcpc['Code'].str.len().describe())