import pandas as pd
from datetime import datetime

# Define df / basic info / preview 
# Snomed ct data (tab-delimited, limited to 100,000)
snomed = pd.read_csv('input\snomeddata.txt',
    sep='\t', nrows=100000)
snomed.info()
print(snomed.head())

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

# Remove duplicate rows
shortsnomed = shortsnomed.drop_duplicates()

# Filter out empty or null descriptions
shortsnomed = shortsnomed[
    shortsnomed['Description'].notna() &
    (shortsnomed['Description'].str.strip() != "")
    ]

# Extract csv file with 'Code', 'Description' and 'Last_updated' columns
shortsnomed.to_csv("output\snomed\snomed.csv", index=False)

print(f"Successfully parsed {len(shortsnomed)} records from snomeddata.txt")
print(f"Saved to {'output\snomed\snomed.csv'}") 
print(f"Dataset shape: {shortsnomed.shape}")
print(f"\nFirst 5 rows:")
print(shortsnomed.head())