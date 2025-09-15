## This code does not parse the data file. Have done parsing separately in icd10cmparse.py

import pandas as pd 
from datetime import datetime
import openpyxl as pxl

file_path = "input\icd10cm_2025.txt"

# Define df / basic info / preview 
icd10cm_df = pd.read_csv(file_path, delimiter='\t', dtype=str)
icd10cm_df.info()

# Explore raw file as csv to view
icd10cm_df.to_csv("output\icd10cm\icd10cm.csv")

# File does not have headers or index

# Explore the csv file as a tab separated file
icd10cm_df.to_csv("output\icd10cm\icd10cm1.csv", index=False, sep='\t')

# Explore the csv as a fwf file, with headers
icd10cm_df = pd.read_fwf(file_path, header=None,
    names=['Number', 'Code', 'Level', 'Description', 'Description2'])

# Identify 4 key columns named above to explore/extract
icd10cm_df['Number']
icd10cm_df['Code']
icd10cm_df['Level']
icd10cm_df['Description']

print(icd10cm_df.head())

# Extract 2 columns from above to new dataframe and add column with today's date
## use of copy() to create a copy of the selected columns
shorticd10cm = icd10cm_df[['Code', 'Description']].copy()
shorticd10cm['Last_updated'] = datetime.today().strftime('%Y-%m-%d')

# Remove empty/blank/NaN "Description" entries 
shorticd10cm_df = shorticd10cm[
    shorticd10cm['Description'].notna() & 
    (shorticd10cm['Description'].str.strip() != '')
    ]

# Remove duplicate rows if any keeping the first occurrence
shorticd10cm_df = shorticd10cm.drop_duplicates()

print(shorticd10cm_df.head())

# Extract csv file with 'Code', 'Description' and 'Last_updated' columns
shorticd10cm.to_csv("output\icd10cm\icd10cm3.csv", sep='\t', index=False)

