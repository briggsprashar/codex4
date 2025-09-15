## this script parses icd10cm raw file
import pandas as pd 

# Import "re" library (built-in Python module) to work with regular expressions (RegEx)
# "re" provides various functions to search, match, split, and replace text based on patterns
import re 

file_path= 'input\icd10cm_2025.txt'

# Initialize a blank list to hold parsed icd10 US codes (in rows) tp create an empty list variable codes which 
# will later hold multiple parsed code entries extracted from the raw file
codes = []

# OPEN the raw file in read mode ('r') with UTF-8 encoding, iterating through the file line by line
with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:     
        line = line.rstrip('\n\r') # Remove trailing newline and carriage return characters 
        if len(line) < 15: # Skip any lines shorter than 15 characters as these will be too short to contain valid icd10cm records
            continue # "With", "for", "if", "continue" need to be indented

    # PARSE the fixed-length format with slicing based on pdf instructions. 
    order_num = line[0:5].strip() # Characters at positions 0–5, trimmed of spaces. This is the sequence or order number
    code = line[6:13].strip()     # Characters at positions 6–13, trimmed, representing the diagnosis code 
    level = line[14:15].strip()   # Character at position 14, level indicator (0 or 1), indicating hierarchy
    remaining_text = line[16:]    # Extract everything after position 16 as a string (description)

    parts = re.split(r'\s{4,}', remaining_text, 1) # Splits remaining_text by four or more consecutive spaces.
    # The assumption is that the first part is a short description and the second part is a longer/detailed description 

    description = parts[0].strip() if len(parts) > 0 else "" # short description
    description_detailed = parts[1].strip() if len(parts) > 1 else "" # detailed description if available, otherwise empty

# Append the parsed data to the codes list
codes.append({
    'order_num': order_num,
    'code': code,
    'level': level,
    'description': description,
    'description_detailed': description_detailed
    })
'''
# Debug output to verify each parsed line's fields
print(f"line: {line}")
print(f"order_num: '{order_num}', code: '{code}', level: '{level}'")
print(f"description: '{description}'")
print(f"description_detailed: '{description_detailed}'")
print('-' * 40)
'''

# Create a DataFrame from the parsed codes preserving column order
icd10cm_df = pd.DataFrame(codes) ## Create a DataFrame from the parsed codes, calling list to the dataframe
    # Alt code:
    # # icd10cm_df = pd.DataFrame(codes, columns=['order_num', 'code', 'level', 'description', 'description_detailed'])

icd10cm_df.to_csv("output\icd10cm\icd10cm_parsed.csv", sep='\t', index=False)

# The output file shows only the last row, and even that does not align with headers; need to fix this.
