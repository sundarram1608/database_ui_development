# UI Developemnt for Northwind Database
**Course Work "INFO 531 Data Warehousing & Analytics in Cloud"**

## Project Overview <br>
This project presents the design and development of a comprehensive Data Management and Analytics System powered by MySQL and Python Streamlit and built on the Northwind dataset, that has been modified to suit academic nature of the project. The primary objective of the project was to transform a traditional transactional database into a fully interactive platform capable of performing seamless data management operations (CRUD) and providing actionable business insights (Analytics). The system integrates a well-structured backend, a robust relational database, and an intuitive front-end interface to support a complete analytical workflow, including data ingestion, validation, CRUD operations, and visualization.

## System Architecture: <br>
•	Database layer - integrating MySQL for data storage<br>
•	Backend layer - Python for backend logic <br>
•	UI Layer  - Streamlit for the user interface<br>

## Project Structure: <br>
The repo consists of 3 folders:<br>
> app<br>
> database_creation_mysql<br>
> reports <br>

**app**<br>
- This folder contains the folder named `pages`, that contains the python files `1_Data_Management_CRUD.py` & `2_Analytics_Dashboard.py`. These are the two pages of the UI<br>
- This folder contains other 3 python files namely `Home.py`, `helpers.py` & `interface.py`. `Home.py` is the main app file, that should be initialized to get the frontend up and running. `helpers.py` contains all the custom userdefined functinos that are necessary to run the CRUD and analytics dashboards. `interface.py` organizes the helper functions in `helpers.py` to be called in a sequential order for application to run successfully.<br>
- There is another `test_files_for_validation.zip` file that contains all the test cases to validate the functions of the application.<br>

**database_creation_mysql** <br>
- This folder contains `database_creation.sql` that contains the MYSQL code for creation of modified northwind database.<br>

**reports** <br>
- This folder contains the final project report. 

## How to use this repository? <br>
Follow the steps below, to experiment with my code:<br>
- Fork the repository <br>
- Run the following commands in your terminal.<br>
- Clone your forked repo to your local <br>
```bash
git clone
```

It is recommended to use a virtual environment. <br>

**Usage:**<br>
Ensure that German_bank.csv and code_file.ipynb are in the same directory.<br>
The Jupyter Notebook is optimised to work in any Notebook IDE after installation of the required packages.
