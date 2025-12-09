# UI Developemnt for Northwind Database
**Course Work "INFO 531 Data Warehousing & Analytics in Cloud"**

## Project Overview <br>
This project presents the design and development of a comprehensive Data Management and Analytics System powered by MySQL and Python Streamlit and built on the Northwind dataset, that has been modified to suit academic nature of the project. The primary objective of the project was to transform a traditional transactional database into a fully interactive platform capable of performing seamless data management operations (CRUD) and providing actionable business insights (Analytics). The system integrates a well-structured backend, a robust relational database, and an intuitive front-end interface to support a complete analytical workflow, including data ingestion, validation, CRUD operations, and visualization.

## System Architecture: <br>
•	Database layer - integrating MySQL for data storage<br>
•	Backend layer - Python for backend logic <br>
•	UI Layer  - Streamlit for the user interface<br>

## Project Structure: <br>
The repo consists of 3 folders & 2 files:<br>
> app<br>
> database_creation_mysql<br>
> reports <br>
> requirements.txt <br>
> README.md <br>


**app**<br>
- This folder contains the folder named `pages`, that contains the python files `1_Data_Management_CRUD.py` & `2_Analytics_Dashboard.py`. These are the two pages of the UI<br>
- This folder contains other 3 python files namely `Home.py`, `helpers.py` & `interface.py`. `Home.py` is the main app file, that should be initialized to get the frontend up and running. `helpers.py` contains all the custom userdefined functinos that are necessary to run the CRUD and analytics dashboards. `interface.py` organizes the helper functions in `helpers.py` to be called in a sequential order for application to run successfully.<br>
- There is another `test_files_for_validation.zip` file that contains all the test cases to validate the functions of the application.<br>

**database_creation_mysql** <br>
- This folder contains `database_creation.sql` that contains the MYSQL code for creation of modified northwind database.<br>

**reports** <br>
- This folder contains the final project report. 

**requirements.txt** <br>
- This file contains the libraries necessary for application creation.<br>

**README.md** <br>
- This current file you are reading containing all details. <br>

## How to use this repository? <br>
**Pre-Requisites** <br>
- MYSQL Server<br>
- MYSQL Workbench<br>

Follow the steps below, to experiment with my code:<br>
- Fork the repository <br>
- Run the following commands in your terminal.<br>
- Clone your forked repo to your local <br>
```bash
git clone https://github.com/sundarram1608/database_ui_development.git
```
- It is recommended to use a virtual environment. <br>
- Now create a virtual environment by running the following command in terminal. <br>
```bash
cd “path to directory“
```
```bash
python3 -m venv myenv
```
```bash
source myenv/bin/activate
``` 
```bash
pip install -r requirements.txt
```
<br>
- Now,  Start the MYSQL Server from your settings. <br>
- Open MYSQL Workbench and open the `database_creation.sql` and run all the codes.<br>
- Database is created. <br>
- Now, in the terminal, navigate to the folder containing `Home.py`.

```bash
cd "path to Home.py"
```
```bash
streamlit run Home.py
```
<br>
**The app is now up and running.**<br>

**Usage:**<br>
Ensure that the folder hierarchy in app is maintained for succesful running of the application and also database is created in the MYSQL server.
