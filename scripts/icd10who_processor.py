import pandas as pd 
from datetime import datetime
import openpyxl as pxl

file_path = "input\icd10who2019.txt"

# Explore raw file as csv to view
icd10who_df = pd.read_csv(file_path, header=None, sep=';')
icd10who_df.info()
print(icd10who_df.head())

# Explore raw file as csv to view
icd10who_df.to_csv("output\icd10who\icd10who1.csv") 

columns = ['level', 'type', 'usage', 'sort', 'parent', 'code', 'display_code', 
           'icd10_code', 'title_en', 'parent_title', 'detailed_title', 
           'definition', 'mortality_code', 'morbidity_code1', 'morbidity_code2',
           'morbidity_code3', 'morbidity_code4']

# Define df / basic info / preview 
icd10who_df = pd.read_csv(file_path, header=None, sep=';', names=columns)
icd10who_df.info()
print(icd10who_df.head())

# Remove duplicate rows if any keeping the first occurrence
icd10who_df = icd10who_df.drop_duplicates()

# Explore raw file with column headers
icd10who_df.to_csv("output\icd10who\icd10who2.csv", index=False)

print(f"Successfully parsed {len(icd10who_df)} records from {file_path}")
print(f"Saved to {"output\icd10who\icd10who2.csv"}")
print(f"\nFirst 5 rows:")
print(icd10who_df.head())

# CREATE a trimmed DataFrame with selected columns and assign it to a new VARIABLE
    # use of double square brackets to select multiple columns
    # use of copy() to create a copy of the selected columns
shorticd10who = icd10who_df[['display_code', 'detailed_title']].copy()

# ADD a timestamp column for tracking updates with today's date in 'MM-DD-YYYY' format instead of a hardcoded timestamp
shorticd10who['last_updated'] = datetime.today().strftime('%m-%d-%Y')

# REMOVE empty descriptions/blanks/NaN values 
shorticd10who = shorticd10who[
    shorticd10who['detailed_title'].notna() & 
    (shorticd10who['detailed_title'].str.strip() != '')
    ]

# Extract csv file with 'display_code', 'detailed_title' and 'last_updated' columns
shorticd10who.to_csv("output\icd10who\icd10who3.csv", index=False)