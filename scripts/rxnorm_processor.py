import pandas as pd
from datetime import datetime

# Define df / basic info / preview 
# RxNorm dataset (pipe-delimited, no headers in source file)
rxnorm = pd.read_csv("input\RXNSAT.RRF", nrows=1000000,
    sep="|",
    header=None,
    dtype=str)
rxnorm.info()
print(rxnorm.head())

# Explore key columns by index
rxnorm[0]
rxnorm[9]

# Create a simplified DataFrame with selected columns
shortrxnorm = rxnorm[[0, 9]].copy()

# Add timestamp column for tracking updates
shortrxnorm['Last_updated'] = datetime.today().strftime('%m-%d-%Y')

# Rename columns for clarity and consistency
shortrxnorm = shortrxnorm.rename(columns={
    0: 'Code',
    9: 'Description'
})

#removing empty descriptions or nulls or blanks 
shortrxnorm = shortrxnorm[
    shortrxnorm['Description'].notna() & 
    (shortrxnorm['Description'].str.strip() != "")]

# Extract csv file with 'Code', 'Description' and 'Last_updated' columns
shortrxnorm.to_csv(r'output\rxnorm_short\rx_short.csv', sep='\t', index=False, header=True)

print(f"Successfully parsed {len(shortrxnorm)} records from RXNATOMARCHIVE.RRF")
print(f"Saved to {'output\rxnorm_short\rx_short.csv'}") # output is jumbled up letters
print(f"Dataset shape: {shortrxnorm.shape}")
print(f"\nFirst 5 rows:")
print(shortrxnorm.head())
