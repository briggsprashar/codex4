import pandas as pd
from datetime import datetime
import os
import gc

rxnorm = pd.read_csv("input\RXNSAT.RRF", nrows=50000,
    sep="|",        # pipe-delimited in raw file
    header=None,    # no headers in raw file
    dtype=str)      # can also use e before file path above to identify raw string data
rxnorm.info()
print(rxnorm.head())

# Explore key columns by index
rxnorm[[0, 9]]


shortrxnorm = rxnorm[[0, 9]].copy() # Create a simplified DataFrame with selected columns
shortrxnorm['Last_updated'] = datetime.today().strftime('%m-%d-%Y') # Add new column with today's date

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

# File size
file_size_bytes = os.path.getsize(r"output\rxnorm_short\rx_short.csv")
file_size_mb = file_size_bytes / (1024 * 1024)
print(f"File size: {file_size_mb:.2f} MB")

# Memory usage
print (f"\nMemory usage (MB): {rxnorm.memory_usage(deep=True).sum() / 1024**2:.2f}") # different from polars

gc.collect()