# Codex 4
### Medical Codex Pipeline Development

## Tags
* ETL pipeline development 
* Data quality validation 
* File format optimization 
* Production-ready code practices
* Workflow explanation

## Objective
From identified medical codexes (7 different medical codex types; collectively codexes), create a data pipeline using automated processes and tools that move raw data to local machines for ETL tasks, with the reproducible scripts available on a public Github repository for version control. The aim is to load the transformed data to be available for data wrangling. Proof of concept would be reproducibility from scripts and accompanying files loaded to Github, from where the repository can be cloned and the tasks reproduced. 

---

## Tech-stack
- Python 3.13.7
- IDE: Visual Code Studio
- Github (version control and code hosting/sharing)

<br />
<details>
  <summary>Data Sources</summary>  
<br />

- <a href="https://www.cms.gov/medicare/coding-billing/healthcare-common-procedure-system/quarterly-update"> HCPCS (US) </a>
- <a href="https://www.cms.gov/medicare/coding-billing/icd-10-codes"> ICD-10-CM (US) </a>
- <a href="https://icdcdn.who.int/icd10/index.html"> ICD-10 (WHO) </a>
- <a href="https://loinc.org/downloads/"> LOINC (US) </a>
- <a href="https://download.cms.gov/nppes/NPI_Files.html"> NPI (US) </a>
- <a href="https://www.nlm.nih.gov/research/umls/rxnorm/docs/rxnormfiles.html"> RxNorm (US) </a>
- <a href="https://www.nlm.nih.gov/healthit/snomedct/archive.html"> SNOMED (US) </a>
</details>

## Workflow

<br />
<details>
  <summary>Setup</summary>  
<br />

**Basics**
  - Create Github Repo 
  - Clone it to VSCode on local machine  
  - Optimize VSCode with extensions
  - VSCode folder structure 

**Folder structure**

```
medical-codex-pipeline/
├── scripts/
│   ├── hcpcs_processor.py
│   ├── icd10cm_processor.py
│   ├── icd10who_processor.py
│   ├── loinc_processor.py
│   ├── npi_processor.py 
│   ├── rxnorm_processor.py
│   └── snomed_processor.py
├── .gitignore
├── README.md
└── requirements.txt
```
**Requirements.txt and additional dependencies** 
  - Pandas
  - Polars
  - Tabulate
  - Openpyxl
  - Rich
  - Requests    
  - Pyarrow
  - Fastparaquet
  - Wheel
  - PyPi

**Data for Pipeline development**

- Download raw data files identified in Data Sources above 
- For ICD-10(US), LOINC and HCPC datasets, get validated first by signing up at [NIM UMLS](https://www.uts.nlm.nih.gov/uts/signup-login)
- From the downloaded files/folders, upload identified suitable raw datafiles to the Input folder of the cloned project repository in VSCode.

</details>

## **Now, Code Away!**

> ### There are many routes to Dublin! Take any!
> **This is the route I took.....**

<br />
<details>
  <summary>Raw Data Files</summary>  
<br />

  - Extract the compressed Downloaded Codex folders for codex package with raw data files, schema, etc.
    
  - Identify files with relevant codex data (.txt, .cvs, .xml, .xlsx and other file types) by opening these files in popular relevant applications e.g., Notepad, Spreadsheets, and even optimized browsers.
  
  - Identify appropriately sized files (codex files are large; smaller files can be ignored from extracted data folders), and alternatively opened with python script within VSCode and explored within VSCode.
  
  - Pipe-delimited text files such as those from UMLS Metathesaurus or RxNorm, are in Rich Release Format (RRF), typically very large, and intended to be loaded into a relational database system for processing rather than directly opening in simple text editors. 
  
  - The sole RRF file contents were visible only as an output file or in terminal as a preview, etc.
  
  - Reading relevant data from a PDF or similar file type not included in this code.
</details>
<br />
<details>
  <summary>Project data outputs</summary>  
<br />

  - Raw data downloaded using compliant methods and protocols.
    
  - Raw data file ingested via VSCode with output in .CSV file type.
    
  - 2 columns extracted from each processed codex data file (using a unique identifier and a descriptor e.g., 'Code', 'Description', or 'Last_Name'), where necessary renamed.  
    
  - 1 column added to the output file with the date of last update (e.g.,'Last_updated')

  - VSCode configurations in requirements.txt has dependencies and configuration settings
    
  - Used Pandas and Polars to explore file ingestion of files of different sizes
    
  - Code validated by running code snippets in the terminal and previewing output files. 
    
  - Generated a .csv for each raw data file using pandas, polars or parquet.
    
  - Documentation in the code and via README.md and the code.

  - Will try and add Logging to the code
    
  - Reproducibility via Github repository
</details>
<br />
<details>
  <summary> Push to Github</summary>  
<br />

Files/folders to be pushed to Github 

```
medical-codex-pipeline/
├── scripts/
│   ├── hcpcs_processor.py
│   ├── icd10cm_processor.py
│   ├── icd10who_processor.py
│   ├── loinc_processor.py
│   ├── npi_processor.py 
│   ├── rxnorm_processor.py
│   └── snomed_processor.py
├── .gitignore
├── README.md
└── requirements.txt
```
</details>
<br />
<details>
  <summary>Validate reproducibility</summary>  
<br />

- Push to Github repository
- Clone (copy) the code in a new local VSCode folder 
- Reproduce the results from copied local folder for validation and to test reproducibility 
- Identify bugs and issues in reproducibility noted in an issue log. 
- Try and identify if the issues are because of environment/dependencies or script, and resolve. 
- List unresolved issues
</details>
<br />

## Remember there are many ways to get to Dublin!

<br />

<details>
  <summary>Clean up local machine</summary>  
<br />

- After validating the cloned files and testing reproducibility (identifying issues in an issue log for further improvement), archive the project folder on your machine, noting the raw data file download process so it can be repeated. The raw data files can be deleted from the local machine.
- Record key learning in whichever way you deem fit. The important thing is to learn and understand the concepts and process.
- Move on to the next project! But after understanding the concepts not just hacking out the output files through "vibe coding". 
</details

<br />

<details>
  <summary>Outcome and limitations</summary>  
<br />

- This repo explore code from the repo medical-codex-pipeline by using some different modules.
- All scripts have been standardized to explore pretty much the same data elements using similar code. 
- Common functions (used in repo medical-codex-pipeline) could have made the code much efficient. 
</details>
<br />

<details>
  <summary>Learnings and insights</summary>  
<br />

- The complexity level of the sample starter codes was incremental in difficulty, exploring different types of data processing techniques with each sample code. 
- Sample codes exposed different techniques, and as a result, tools and dependencies, to process data and create data pipelines using basic Python code, VSCode dependencies, environment creation, and Github integration.
- The use of LLM supported coding also exposed many other ways to process the data to create data pipelines than shared in the sample code blocks. 
- LLM use gave exposure to the sheer expanse of coding in data analytics.
- Various dependencies: Inbuilt Python modules, Python libraries and 3rd party modules. (Tabular, Datetime, Path, Wheel, Openpyxl, Fastparquet, Pyarrow.)
- Python code workflow using VSCode integrating to Github.
</details>

---
## ✨ 📊 To many more data pipelines, smooth data flows and insightful analytics ahead! 📊

