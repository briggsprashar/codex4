import pandas as pd
from datetime import datetime
import openpyxl as pxl

file_path = "input\HCPC2025_OCT_ANWEB.xlsx"

# Define df / basic info / preview 
hcpc_df = pd.read_excel(file_path)
hcpc_df.info()
print(hcpc_df.head())

# Explore raw file as csv to view
hcpc_df.to_csv("output\hcpc\hcpc.csv")

# File has headers and is comma separated

# Explore the whole csv file as tab separated file
hcpc_df.to_csv("output\hcpc\hcpc2.csv", sep='\t', index=False, header=True)

# Identify 3 columns to extract/explore 
hcpc_df['HCPC']
hcpc_df['LONG DESCRIPTION']
hcpc_df['SHORT DESCRIPTION']

# Extract 3 columns to new dataframe and rename columns and add new column with today's date
## use of copy() to create a copy of the selected columns
shorthcpc = hcpc_df[['HCPC', 'LONG DESCRIPTION']].copy()
shorthcpc = shorthcpc.rename(columns={'HCPC': 'Code', 'LONG DESCRIPTION': 'Description'})
shorthcpc['Last_updated'] = datetime.today().strftime('%Y-%m-%d')

# Extract csv file with 'Code', 'Description' and 'Last_updated' columns
shorthcpc.to_csv("output\hcpc\hcpc3.csv", sep='\t', index=False, header=True)