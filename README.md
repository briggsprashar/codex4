# Medical Codex Data Pipeline

## Tags
- ETL pipeline development 
- Data quality validation 
- File format optimization 
- Production-ready code practices
- Workflow explanation

## Objective
From identified medical codexes (7 different medical codex types; collectively codexes), create a data pipeline using automated processes and tools that move raw data to local machines for ETL tasks, with the reproducible scripts available on a public Github repository for version control. The aim is to load the transformed data to be available for data wrangling. Proof of concept would be reproducibility from scripts and accompanying files loaded to Github, from where the repository can be cloned and the tasks reproduced. 

---

## Tech-stack
- Python 3.13.7
- Visual Code Studio (recommended editor)
- Github (version control and code hosting)
 
---

## Data Sources
7 Medical codex datasets 
- <a href="https://www.cms.gov/medicare/coding-billing/healthcare-common-procedure-system/quarterly-update"> HCPCS (US) </a>
- <a href="https://www.cms.gov/medicare/coding-billing/icd-10-codes"> ICD-10-CM (US) </a>
- <a href="https://icdcdn.who.int/icd10/index.html"> ICD-10 (WHO) </a>
- <a href="https://loinc.org/downloads/"> LOINC (US) </a>
- <a href="https://download.cms.gov/nppes/NPI_Files.html"> NPI (US) </a>
- <a href="https://www.nlm.nih.gov/research/umls/rxnorm/docs/rxnormfiles.html"> RxNorm (US) </a>
- <a href="https://www.nlm.nih.gov/healthit/snomedct/archive.html"> SNOMED (US) </a>

---
## Workflow
1. Setup
    - Create Github Repo 
    - Clone it to VSCode on local machine  
    - Optimize VSCode with extensions
        - Python, Gitlens, 
2. VSCode folder structure 
```
medical-codex-pipeline/
├── input/
├── scripts/
│   ├── snomed_processor.py
│   ├── icd10cm_processor.py
│   ├── icd10who_processor.py
│   ├── hcpcs_processor.py
│   ├── loinc_processor.py
│   ├── rxnorm_processor.py
│   └── npi_processor.py
├── output/
│   ├── csv/
├── utils/
│   └── common_functions.py
├── requirements.txt
├── README.md
└── .gitignore
```
3. VSCode environment based on Requirements.txt and additional dependencies 
    - Pandas
    - Polars
    - Requests       
    - Pyarrow
    - Fastparaquet
    - Wheel
    - Tabulate
    - PiPy
    - Openpyxl

4. Data Pipeline development
    - Download raw data files for ICD-10(WHO) NPI, RxNorm and SNOMED from identified under Data Sources above 
    - For ICD-10(US), LOINC and HCPC get validated by signing up at <a href="https://uts.nlm.nih.gov/uts/signup-login"> NIH-UMLS.</a>
    - From the downloaded data folders, upload identified suitable raw datafiles to the Input folder of the cloned project repository in VSCode.

## **Now, Code Away!**

> ### There are many routes to Dublin! Take any!
> **I took this route.....**
#### Raw data files
    - Codex data downloads are compressed files that need to be extracted. The folders will have many files that make the codex package that not only have raw data files, but also schema and other information to help understand, use and decode the medical codex data.
    - Identify files with relevant codex data. With .txt, .cvs, .xml, or .xlsx and other common file types, this can be done by opening these files in popular relevant applications e.g., Notepad, Spreadsheets, and even optimized browsers.
    - Alternatively, appropriately sized files (codex files are large; smaller files can be ignored from extracted data folders), can be opened with python script within VSCode and explored within VSCode.
    - Medical codex files such as those from UMLS Metathesaurus or RxNorm, are in Rich Release Format (RRF). These files are pipe-delimited text files, typically very large, and intended to be loaded into a relational database system for processing rather than directly opened in simple text editors due to size. For this project the contents of the sole RRF file were visible only as an output file or in terminal as a preview '.head()'.
    - This project does not include reading relevant data from a PDF or similar file type,
#### Project data outputs
    - Raw data downloads using compliant methods and protocols.
    - Raw data file to be ingested via VSCode with output in .CSV file type.
    - 2 columns extracted from each processed codex data file (some sort of unique identifier and a descriptor e.g., 'Code', 'Description', or 'Last_Name'), where necessary renamed.  
    - 1 column needs to be added to the output file with the date of last update (e.g.,'Last_updated')
    - Dependencies and configuration setting for Github repository via VSCode configurations reflected in Requirements.txt
    - Explore file ingestion of files of different sises using Pandas and Polars.
    - Code validation via running code snippets in the terminal and previewing output files. 
    - Generating a .csv for each raw data file using pandas, polars or parquet.
    - Documentation and logging embedded in the code and via README.md and the code.
    - Reproducibility via Github repository

### 1. HCPCS medical codex data-pipeline

#### Create environment
import pandas and openpyxl, `from datetime import datetime`

#### Prepare and explore file
define filepath  > create data frame to read file from defined file path > `df.info()` > `print(df.head())` > explore raw file for raw data structure `df.to.csv("filepath")`> further explore tab-separated by adding `sep'\t'`, `index=False`, `header=True` > identify 2 columns > put the 2 columns in dfs: df['column1'], df['column2']

#### Extract relevant columns, rename, add a 3rd column
extract these 2 copy them in a separate short_df `short_df = df[['column1', 'column2']].copy()` > rename the 2 columns in this short_df `short_df = short_df.rename(columns={'column1':Code, 'column2': Description'})` > add a 3rd column ``short_df[column3] = datetime.today().strftime('%Y-%m-%d')` 

#### Extract output
`short_df.to_csv("output_file_path.csv", sep'\t', index=False, header=True)`

### 2. ICD-10-CM (US) Medical codex data-pipeline
#### 

### 3. ICD-10 (WHO) medical codex data-pipeline
#### 

### 4. LOINC medical codex data-pipeline
#### 

### 5. NPI medical codex data-pipeline
#### 

### 6. RxNorm medical codex data-pipeline
#### 

### 7. SNOMED codex data-pipeline
#### 

## Push to Github
Files/folders from cloned repository in VSCode to be pushed to Github 
```
medical-codex-pipeline/
├── scripts/
│   ├── snomed_processor.py
│   ├── icd10cm_processor.py
│   ├── icd10who_processor.py
│   ├── hcpcs_processor.py
│   ├── loinc_processor.py
│   ├── rxnorm_processor.py
│   └── npi_processor.py
├── utils/
│   └── common_functions.py
├── requirements.txt
├── README.md
└── .gitignore
```
## Validate reproducibility
After the final push to Github repository, clone the code in a new local VSCode folder, and reproduce the results for validation and to test reproducibility, and identify bugs and issues in reproducibility noted in an issue log. In case of issues try and identify if the issues are because of environment/dependencies or script, and resolve. 

Remember there are many ways to Dublin!

## Clean up local machine
Finally, after validating the cloned files and testing reproducibility (identifying issues in an issue log for further improvement), archive the project folder on your machine, noting the raw data file download process so it can be repeated. The raw data files can be deleted from the local machine.

Record key learning in whichever way you deem fit. The important thing is to learn and understand the concepts and process.

Move on to the next project, but after understanding the concepts not just hacking out output files through vibe coding. 

## Learnings and insights
- The complexity level of the sample starter codes was incremental in difficulty, exploring different types of data processing techniques with each sample code. 
- Sample codes exposed different techniques, and as a result, tools and dependencies, to process data and create data pipelines using basic Python code, VSCode dependencies, environment creation, and Github integration.
- The use of LLM supported coding also exposed many other ways to process the data to create data pipelines than shared in the sample code blocks. 
- LLM use gave exposure to the sheer expanse of coding in data analytics.
- Various dependencies: Inbuilt Python modules, Python libraries and 3rd party modules. (Tabular, Datetime, Path, Wheel, Openpyxl, Fastparquet, Pyarrow.)
- Python code workflow using VSCode integrating to Github.


---
## ✨ 📊 To many more data pipelines, smooth data flows and insightful analytics ahead! 📊 ✨


