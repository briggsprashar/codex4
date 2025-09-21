import polars as pl
from tabulate import tabulate # first pip install tabulate
import os
import gc 

npi_file_path = "input/npidata.csv"
npi = pl.read_csv(npi_file_path, n_rows=100000)
#npi.describe()

print(f"Successfully loaded {len(npi)} records from NPI data")

# print(f"Columns: {npi.columns}") ... prints a cluttered column list
# print(tabulate([npi.columns], tablefmt='grid')) ... no good

# Print columns vertically (one-per-line): best to select whihc columns to select for npi_small below
for col in npi.columns:
    print(col)

print(f"\nDataset shape: {npi.shape}")
print(f"\nFirst 5 rows:")
print(npi.head())

npi_small = npi.select([
    'NPI', 
    'Provider Last Name (Legal Name)'
])

npi_small = npi_small.with_columns(
    pl.lit('2025-09-17').alias('last_updated')
)

npi_small = npi_small.rename({
    'NPI': 'Code',
    'Provider Last Name (Legal Name)': 'Description',
    'last_updated': 'Last_updated'
})
output_path = "output/npi_small.csv"
npi_small.write_csv(output_path)

### Make Parquet file to decrease file size for big data sets
npi_small.write_parquet("output/npi_small.parquet")

# File size
file_size_bytes = os.path.getsize("output/npi_small.parquet")
file_size_mb = file_size_bytes / (1024 * 1024)
print(f"File size: {file_size_mb:.2f} MB")

# Memory usage
print(f"\nMemory usage (MB): {npi.estimated_size() / 1024**2:.2f}") # different from pandas

gc.collect()