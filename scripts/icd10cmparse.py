## this script parses icd10cm raw file
import pandas as pd 
from datetime import datetime
import openpyxl as pxl
from collections import Counter
import os
import gc
# Import "re" library (built-in Python module) to work with regular expressions (RegEx)
# "re" provides various functions to search, match, split, and replace text based on patterns
import re 
import time

# Start Timestamp
start_time_pandas = time.time()

# define file paths
inputfile_path= 'input/icd10cm_2025.txt'
outputfile_path = 'output/icd10cm/icd10cm_parsed.xlsx'
finaloutputfile_path = 'output/icd10cm/icd10cm_parsed.csv'

# Initialize a blank list to hold parsed icd10 US codes (in rows) tp create an empty list variable codes which 
# will later hold multiple parsed code entries extracted from the raw file
codes = []

# OPEN the raw file in read mode ('r') with UTF-8 encoding, iterating through the file line by line
with open(inputfile_path, 'r', encoding='utf-8') as file:
    for line in file:     
        line = line.rstrip('\n\r') # Remove trailing newline and carriage return characters 
        if len(line) < 15: # Skip any lines shorter than 15 characters as these will be too short to contain valid icd10cm records
            continue # "With", "for", "if", "continue" need to be indented

# Slice fields based on fixed-length format with correct indexing. 
        order_num = line[0:5].strip() # Characters at positions 0–5, trimmed of spaces. This is the sequence or order number
        code = line[6:14].strip()     # Characters at positions 6–13, trimmed, representing the diagnosis code 
        level = line[14:15].strip()   # Character at position 14, level indicator (0 or 1), indicating hierarchy
        remaining_text = line[16:].strip()    # Extract everything after position 16 as a string (description)

# Split remaining_text by four or more consecutive spaces.
        parts = re.split(r'\s{4,}', remaining_text, 1) 
    # The assumption is that the first part is a short description and the second part is a longer/detailed description 
        description = parts[0].strip() if len(parts) > 0 else "" # short description
        description_detailed = parts[1].strip() if len(parts) > 1 else "" # detailed description if available, otherwise empty

# Append the parsed data to the codes list
        codes.append({
    # 'order_num': order_num,
            'code': code,
    # 'level': level,
            'description': description,
    # 'description_detailed': description_detailed
    })

# Debug output to verify each parsed line's fields
# print(f"line: {line}")
# print(f"order_num: '{order_num}', code: '{code}', level: '{level}'")
# print(f"description: '{description}'")
# print(f"description_detailed: '{description_detailed}'")
# print('-' * 40)

# dataframe / basic info / preview from the parsed codes preserving column order
icd10cm_df = pd.DataFrame(codes) ## Create a DataFrame from the parsed codes, calling list to the dataframe
    # Alt code:
    # # icd10cm_df = pd.DataFrame(codes, columns=['order_num', 'code', 'level', 'description', 'description_detailed'])

# add column with today's date
icd10cm_df['last_updated'] = datetime.today().strftime('%Y-%m-%d')

# Loaded
print(f"\n1>>> Successfully \033[33;1mLOADED\033[0m {len(icd10cm_df)} ICD10US records")

# raw file Shape
print(f"\n2>>> Dataset \033[33;1mSHAPE:\033[0m {icd10cm_df.shape}")

# Total columns
num_columns = icd10cm_df.shape[1]
print(f"      >>> \033[33;1mCOLUMNS\033[0m: {num_columns}")

# Total rows
num_rows = icd10cm_df.shape[0]
print(f"      >>> \033[33;1mROWS\033[0m: {num_rows}")

print(f"\n3>>> ICD10US \033[33;1mFILE INFO\033[0m\n") # basic info: range index, data columns (total columns, index, column headers, non-null count, dtype, memory usage)
icd10cm_df.info()

# Unique data types and count
dtype_counts = Counter(str(dtype) for dtype in icd10cm_df.dtypes)
print(f"\n      >>> \033[33;1mUnique data types and counts\033[0m: {dict(dtype_counts)}")

# ILOC
# get custom no of row as series
row = icd10cm_df.iloc[30]  
print(f"\n4>>> ICD10US \033[33;1mILOC\033[0m \n\n{row[:30]}") 
# get all rows as series
print(f"\n>>>>>>>> \033[33;1m ILOC\033[0m \n\n{icd10cm_df.iloc}")
print(icd10cm_df.iloc[0]) 


# icd10cm_df.to_csv(outputfile_path, sep='\t', index=False) # columns misaligned as it is a csv
icd10cm_df.to_excel(outputfile_path, index=False)

output = pd.read_excel(outputfile_path)
output.to_csv(finaloutputfile_path)

print("\n>>> ICD10US \033[33;1mFIRST 5 ROWS \033[0m Extracted File\n")
print(output.head())

# Describe raw file
print(f"\n >>> \033[32;1mDescribe - Raw File ???\033[0m\n{icd10cm_df.describe()}")

# print message 
print("\n6>>> ... \033[35;1m Raw ICD10US file transformed to extracted\033[0m  ...\nwith columns \033[33;1m'Code', 'Description' and 'Last_updated'\033[0m")

# Describe extracted file
print(f"\n >>> \033[32;1mDescribe - Extracted File ???\033[0m\n{output.describe()}")

print(f"\n>>> Successfully \033[33;1mPARSED\033[0m {len(icd10cm_df)} ICD10US records from {inputfile_path}")

# input file size
inputfile_size_bytes = os.path.getsize(inputfile_path)
inputfile_size_mb = inputfile_size_bytes / (1024 * 1024)
print(f"\n11>>> Raw ICDUS10 \033[33;1mFile size\033[0m: {inputfile_size_mb:.2f} MB")

# Memory usage
print (f"\n     >>> Raw File \033[33;1mMemory usage \033[0m: {icd10cm_df.memory_usage(deep=True).sum() / 1024**2:.2f} MB\n") # different from polars

# extracted file size
file_size_bytes = os.path.getsize(finaloutputfile_path)
file_size_mb = file_size_bytes / (1024 * 1024)
print(f"12>>> Extracted ICD10US \033[33;1mFile size\033[0m: {file_size_mb:.2f} MB")

# Memory usage
print (f"\n     >>> Extracted File \033[33;1mMemory usage\033[0m: {output.memory_usage(deep=True).sum() / 1024**2:.2f} MB\n") # different from polars

# End Timestamp
end_time_pandas = time.time()
# Elapsed Time
icd10cm_df_pandas = pd.read_csv(inputfile_path, nrows=10000, encoding_errors="ignore", on_bad_lines='skip')
elapsed_time_pandas = end_time_pandas - start_time_pandas
# Print total elapsed time
print(f" ------ \033[33;1mTotal Elapsed time:\033[0m \033[32;1m {elapsed_time_pandas:.3f} seconds \033[0m------\n")

gc.collect()
