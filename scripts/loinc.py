import pandas as pd 
from datetime import datetime

file_path="input\Loinc.csv"

# Define df / basic info / preview 

loinc = pd.read_csv(file_path, dtype=object, sep=',', quotechar='"')
loinc.info()
print(loinc.head())

# Explore raw file as csv to view
#loinc.to_csv("output\loinc\loinc1.csv") 

# Explore key columns (use dot or bracket notation)
loinc['LOINC_NUM']
loinc['LONG_COMMON_NAME']
loinc['SHORTNAME']
loinc['DisplayName']
loinc['DefinitionDescription']

loinc = pd.read_csv(file_path, header=None, names=['LOINC_NUM', 'LONG_COMMON_NAME'])

# CREATE a trimmed DataFrame with selected columns and assign it to a new VARIABLE
    # use of double square brackets to select multiple columns
    # use of copy() to create a copy of the selected columns
shortloinc = loinc['LOINC_NUM', 'LONG_COMMON_NAME'].copy()

# ADD a timestamp column for tracking updates with today's date in 'MM-DD-YYYY' format instead of a hardcoded timestamp
shortloinc['Last_updated'] = datetime.today().strftime('%m-%d-%Y')

# Explore shortloinc  with 3 column headers from above
shortloinc.to_csv("output\loinc\loinc2.csv", index=False)

# Rename columns for clarity and consistency
shortloinc = shortloinc.rename(columns={
            'LOINC_NUM': 'Code',
            'LONG_COMMON_NAME': 'Description'
            })

# REMOVE empty descriptions/blanks/NaN values 
shortloinc = shortloinc[
    shortloinc['detailed_title'].notna() & 
    shortloinc['detailed_title'].str.strip() != '']

# Extract csv file with 'display_code', 'detailed_title' and 'last_updated' columns
# shortloinc.to_csv("output\loinc\loinc3.csv", index=False)