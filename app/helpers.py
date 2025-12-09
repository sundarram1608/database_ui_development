from __future__ import annotations
import streamlit as st
import os
import mysql.connector
import pandas as pd
import plotly.express as px
import io
import re
from pandas.api import types as pdt
import math
from mysql.connector import errorcode, IntegrityError
import numpy as np
import datetime
import altair as alt
##----------------------####----------------------####----------------------##

# MySQL Connection
def connect_db():
    """Function to connect to MySQL database"""
    password = os.getenv("MYSQL_PASSWORD")
    conn_object = mysql.connector.connect(
                                            host="localhost",  
                                            user="root",       
                                            password=password, 
                                            database="northwind"  
                                        )
    return conn_object
##----------------------####----------------------####----------------------##
################# FOR CRUD OPERATIONS & VALIDATIONS ################# 
##----------------------####----------------------####----------------------##

##----------------------##
## Common Functions ##
##----------------------##

# Show tables in the database
def get_tables():
    """Function to create tables list in the database"""
    conn = connect_db()
    query = f'''SELECT table_name 
                FROM information_schema.tables
                WHERE table_schema = 'northwind' 
                AND table_type = 'BASE TABLE';'''
    df = pd.read_sql(query, conn)
    tables_list = df['TABLE_NAME'].tolist()
    conn.close()
    # st.write("### List of Tables in Northwind Database")
    return tables_list

# Fetch columns of a table
def fetch_table_column_details(table_name):
    """Function to fetch columns of a table"""
    conn = connect_db()
    query = f"SHOW COLUMNS FROM {table_name};"
    df = pd.read_sql(query, conn)
    conn.close()
    # st.dataframe(df)
    return df

##----------------------##
## Read Tab Functions ##
##----------------------##

# View Tables in database based on query
def view_table(query):
    """Function to show tables in the database"""
    conn = connect_db()
    df = pd.read_sql(query, conn)
    conn.close()
    st.dataframe(df,use_container_width=True, hide_index=True)
    # st.write("### List of Tables in Northwind Database")
    return None

def create_query_and_display_table(selected_table):
    if selected_table == "Categories":
        query = f'''SELECT * FROM Categories;'''
        view_table(query)
        
    elif selected_table == "Customers":
        conn = connect_db()
        customerid_query = f'''select distinct(CustomerID) from northwind.Customers;'''
        country_query = f'''select distinct(Country) from northwind.Customers;'''
        city_query = f'''select distinct(City) from northwind.Customers;'''
        postalcode_query = f'''select distinct(PostalCode) from northwind.Customers;'''
        contacttitle_query = f'''select distinct(ContactTitle) from northwind.Customers;'''

        customerid_df = pd.read_sql(customerid_query, conn)
        country_df = pd.read_sql(country_query, conn)
        city_df = pd.read_sql(city_query, conn)
        postalcode_df = pd.read_sql(postalcode_query, conn)
        contacttitle_df = pd.read_sql(contacttitle_query, conn)

        customerid_list = customerid_df['CustomerID'].tolist()
        country_list = country_df['Country'].tolist()
        city_list = city_df['City'].tolist()
        postalcode_list = postalcode_df['PostalCode'].tolist()
        contacttitle_list = contacttitle_df['ContactTitle'].tolist()        

        options = ["CustomerID","Country", "City", "Postal Code", "Customer Title"]
        filter_selection = st.pills(":blue[Filter By]", options, selection_mode="single")
        if not filter_selection:
            query = "SELECT * FROM northwind.Customers"
        
        else:
            filters = []
            if "CustomerID" in filter_selection:
                selected_customerid = st.selectbox(":blue[Select CustomerID]", customerid_list)    
                filters.append(f"CustomerID = '{selected_customerid}'")
            if "Country" in filter_selection:
                selected_country = st.selectbox(":blue[Select Country]", country_list)
                filters.append(f"Country = '{selected_country}'")
            if "City" in filter_selection:
                selected_city = st.selectbox(":blue[Select City]", city_list)
                filters.append(f"City = '{selected_city}'")
            if "Postal Code" in filter_selection:
                selected_postalcode = st.selectbox(":blue[Select Postal Code]", postalcode_list)
                filters.append(f"PostalCode = '{selected_postalcode}'")
            if "Customer Title" in filter_selection:
                selected_contacttitle = st.selectbox(":blue[Select Customer Title]", contacttitle_list)
                filters.append(f"ContactTitle = '{selected_contacttitle}'")            

            #Base query
            query = "SELECT * FROM northwind.Customers"

            #Add WHERE clause only if filters exist
            if filters:
                query += " WHERE " + " AND ".join(filters)

        #Execute the query
        view_table(query)
        conn.close()
 
        #Filters for Employees by Country, City, Birth Month, Hire Date Custom range, PostalCode, Title
       
    elif selected_table == "Employees":
        conn = connect_db()
        employeeid_query = f'''select distinct(EmployeeID) from northwind.Employees;'''
        country_query = f'''select distinct(Country) from northwind.Employees;'''
        city_query = f'''select distinct(City) from northwind.Employees;'''
        postalcode_query = f'''select distinct(PostalCode) from northwind.Employees;'''
        title_query = f'''select distinct(Title) from northwind.Employees;'''

        employeeid_df = pd.read_sql(employeeid_query, conn)
        country_df = pd.read_sql(country_query, conn)
        city_df = pd.read_sql(city_query, conn)
        postalcode_df = pd.read_sql(postalcode_query, conn)
        title_df = pd.read_sql(title_query, conn)

        employeeid_list = employeeid_df['EmployeeID'].tolist()
        country_list = country_df['Country'].tolist()
        city_list = city_df['City'].tolist()
        postalcode_list = postalcode_df['PostalCode'].tolist()
        title_list = title_df['Title'].tolist()        

        options = ["EmployeeID","Country", "City", "Postal Code", "Title", "Birthday", "Hire Date"]
        filter_selection = st.pills(":blue[Filter By]", options, selection_mode="single")
        if not filter_selection:
            query = "SELECT * FROM northwind.Employees"
        
        else:
            filters = []
            if "EmployeeID" in filter_selection:
                selected_employeeid = st.selectbox(":blue[Select EmployeeID]", employeeid_list)    
                filters.append(f"EmployeeID = '{selected_employeeid}'")
            if "Country" in filter_selection:
                selected_country = st.selectbox(":blue[Select Country]", country_list)
                filters.append(f"Country = '{selected_country}'")
            if "City" in filter_selection:
                selected_city = st.selectbox(":blue[Select City]", city_list)
                filters.append(f"City = '{selected_city}'")
            if "Postal Code" in filter_selection:
                selected_postalcode = st.selectbox(":blue[Select Postal Code]", postalcode_list)
                filters.append(f"PostalCode = '{selected_postalcode}'")
            if "Title" in filter_selection:
                selected_title = st.selectbox(":blue[Select Title]", title_list)
                filters.append(f"Title = '{selected_title}'")            
            if "Birthday" in filter_selection:
                month_list = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
                month_map = {
                                "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4,
                                "May": 5, "Jun": 6, "Jul": 7, "Aug": 8,
                                "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
                            }
                selected_month = st.selectbox(":blue[Select Birth Month]", month_list)
                month_number = month_map[selected_month]
                filters.append(f"MONTH(BirthDate) = {month_number}")     
            if "Hire Date" in filter_selection:
                start_date, end_date = st.date_input(
                                                    ":blue[Select Hire Date Range]",value=(datetime.date(1990, 1, 1), datetime.date(2000, 12, 31))
                                                    )
                start_str = start_date.strftime("%Y-%m-%d")
                end_str = end_date.strftime("%Y-%m-%d")
                filters.append(f"HireDate BETWEEN '{start_str}' AND '{end_str}'")


            #Base query
            query = "SELECT * FROM northwind.Employees"

            #Add WHERE clause only if filters exist
            if filters:
                query += " WHERE " + " AND ".join(filters)

        view_table(query)
        conn.close()

    # - [ ] Filter for OrderDetails by Order ID            
    elif selected_table == "OrderDetails":
        conn = connect_db()
        orderid_query = f'''select distinct(OrderID) from northwind.OrderDetails;'''
        orderid_df = pd.read_sql(orderid_query, conn)
        orderid_list = orderid_df['OrderID'].tolist()
        options = ["All","Order ID"]
        filter_selection = st.pills(":blue[Filter]", options, selection_mode="single",default="All")
        if filter_selection == "All":
            query = "SELECT * FROM northwind.OrderDetails"   
        else:
            
            entered_orderid = st.number_input("Enter Order ID",format="%0.0f")
            entered_orderid = int(entered_orderid)
            
            if entered_orderid in orderid_list:
                query = f"SELECT * FROM northwind.OrderDetails WHERE OrderID = {entered_orderid}"

        try:
            view_table(query)
        except:
            pass
        
        conn.close()
        
    # - [ ] Filter for Orders by CustomerID, EmployeeID, OrderID, ShipCountry         
    elif selected_table == "Orders":
        conn = connect_db()
        customerid_query = f'''select distinct(CustomerID) from northwind.Orders;'''
        employeeid_query = f'''select distinct(EmployeeID) from northwind.Orders;'''
        orderid_query = f'''select distinct(OrderID) from northwind.Orders;'''
        shipcountry_query = f'''select distinct(ShipCountry) from northwind.Orders;'''
        
        customerid_df = pd.read_sql(customerid_query, conn)
        employeeid_df = pd.read_sql(employeeid_query, conn)
        orderid_df = pd.read_sql(orderid_query, conn)
        shipcountry_df = pd.read_sql(shipcountry_query, conn)
        
        customerid_list = customerid_df['CustomerID'].tolist()
        employeeid_list = employeeid_df['EmployeeID'].tolist()
        orderid_list = orderid_df['OrderID'].tolist()
        shipcountry_list = shipcountry_df['ShipCountry'].tolist()
        
        options = ["CustomerID", "EmployeeID", "OrderID", "ShipCountry", "OrderDate", "RequiredDate", "ShippedDate"]
        filter_selection = st.pills(":blue[Filter By]", options, selection_mode="single")
        if not filter_selection:
            query = "SELECT * FROM northwind.Orders"
        
        else:
            filters = []
            if "CustomerID" in filter_selection:
                selected_customerid = st.selectbox(":blue[Select CustomerID]", customerid_list)
                filters.append(f"CustomerID = '{selected_customerid}'")
            if "EmployeeID" in filter_selection:
                selected_employeeid = st.selectbox(":blue[Select EmployeeID]", employeeid_list)    
                filters.append(f"EmployeeID = '{selected_employeeid}'")
            if "OrderID" in filter_selection:
                selected_orderid = st.selectbox(":blue[Select OrderID]", orderid_list)
                filters.append(f"OrderID = '{selected_orderid}'")
            if "ShipCountry" in filter_selection:
                selected_shipcountry = st.selectbox(":blue[Select ShipCountry]", shipcountry_list)
                filters.append(f"ShipCountry = '{selected_shipcountry}'")
            if "OrderDate" in filter_selection:
                start_date, end_date = st.date_input(
                                                    ":blue[Select Order Date Range]",value=(datetime.date(1990, 1, 1), datetime.date(2000, 12, 31))
                                                    )
                start_str = start_date.strftime("%Y-%m-%d")
                end_str = end_date.strftime("%Y-%m-%d")
                filters.append(f"OrderDate BETWEEN '{start_str}' AND '{end_str}'")
            if "RequiredDate" in filter_selection:
                start_date, end_date = st.date_input(
                                                    ":blue[Select Required Date Range]",value=(datetime.date(1990, 1, 1), datetime.date(2000, 12, 31))
                                                    )
                start_str = start_date.strftime("%Y-%m-%d")
                end_str = end_date.strftime("%Y-%m-%d")
                filters.append(f"RequiredDate BETWEEN '{start_str}' AND '{end_str}'")
            if "ShippedDate" in filter_selection:
                start_date, end_date = st.date_input(
                                                    ":blue[Select Shipped Date Range]",value=(datetime.date(1990, 1, 1), datetime.date(2000, 12, 31))
                                                    )
                start_str = start_date.strftime("%Y-%m-%d")
                end_str = end_date.strftime("%Y-%m-%d")
                filters.append(f"ShippedDate BETWEEN '{start_str}' AND '{end_str}'")


            #Base query
            query = "SELECT * FROM northwind.Orders"

            #Add WHERE clause only if filters exist
            if filters:
                query += " WHERE " + " AND ".join(filters)

        view_table(query)
        conn.close()
    
    # - [ ] Filter for Products by SupplierID, CategoryID, Discontinued
    elif selected_table == "Products":
        conn = connect_db()
        supplierid_query = f'''select distinct(SupplierID) from northwind.Products;'''
        categoryid_query = f'''select distinct(CategoryID) from northwind.Products;'''
        discontinued_query = f'''select distinct(Discontinued) from northwind.Products;'''
        
        supplierid_df = pd.read_sql(supplierid_query, conn)
        categoryid_df = pd.read_sql(categoryid_query, conn)
        discontinued_df = pd.read_sql(discontinued_query, conn)
        
        supplierid_list = supplierid_df['SupplierID'].tolist()
        categoryid_list = categoryid_df['CategoryID'].tolist()
        discontinued_list = discontinued_df['Discontinued'].tolist()
        
        options = ["SupplierID", "CategoryID", "Discontinued"]
        filter_selection = st.pills(":blue[Filter By]", options, selection_mode="single")
        if not filter_selection:
            query = "SELECT * FROM northwind.Products"
        
        else:
            filters = []
            if "SupplierID" in filter_selection:
                selected_supplierid = st.selectbox(":blue[Select SupplierID]", supplierid_list)
                filters.append(f"SupplierID = '{selected_supplierid}'")
            if "CategoryID" in filter_selection:
                selected_categoryid = st.selectbox(":blue[Select CategoryID]", categoryid_list)    
                filters.append(f"CategoryID = '{selected_categoryid}'")
            if "Discontinued" in filter_selection:
                selected_discontinued = st.selectbox(":blue[Select Discontinued]", discontinued_list, index =1)
                filters.append(f"Discontinued = '{selected_discontinued}'")

            #Base query
            query = "SELECT * FROM northwind.Products"

            #Add WHERE clause only if filters exist
            if filters:
                query += " WHERE " + " AND ".join(filters)

        view_table(query)
        conn.close()
        
    # - [ ] Filters for Shippers by CompanyName
    elif selected_table == "Shippers":
        conn = connect_db()
        companyname_query = f'''select distinct(CompanyName) from northwind.Shippers;'''
        
        companyname_df = pd.read_sql(companyname_query, conn)
        
        companyname_list = companyname_df['CompanyName'].tolist()
        
        options = ["CompanyName"]
        filter_selection = st.pills(":blue[Filter By]", options, selection_mode="single")
        if not filter_selection:
            query = "SELECT * FROM northwind.Shippers"
        
        else:
            filters = []
            if "CompanyName" in filter_selection:
                selected_companyname = st.selectbox(":blue[Select CompanyName]", companyname_list)
                filters.append(f"CompanyName = '{selected_companyname}'")

            #Base query
            query = "SELECT * FROM northwind.Shippers"

            #Add WHERE clause only if filters exist
            if filters:
                query += " WHERE " + " AND ".join(filters)

        view_table(query)
        conn.close()
    
    # - [ ] Filters for Suppliers by Country, Company Name
    elif selected_table == "Suppliers":
        conn = connect_db()
        companyname_query = f'''select distinct(CompanyName) from northwind.Suppliers;'''
        country_query = f'''select distinct(Country) from northwind.Suppliers;'''
        
        companyname_df = pd.read_sql(companyname_query, conn)
        country_df = pd.read_sql(country_query, conn)
        
        companyname_list = companyname_df['CompanyName'].tolist()
        country_list = country_df['Country'].tolist()
        
        options = ["CompanyName", "Country"]
        filter_selection = st.pills(":blue[Filter By]", options, selection_mode="single")
        if not filter_selection:
            query = "SELECT * FROM northwind.Suppliers"
        
        else:
            filters = []
            if "CompanyName" in filter_selection:
                selected_companyname = st.selectbox(":blue[Select CompanyName]", companyname_list)
                filters.append(f"CompanyName = '{selected_companyname}'")
            if "Country" in filter_selection:
                selected_country = st.selectbox(":blue[Select Country]", country_list)
                filters.append(f"Country = '{selected_country}'")

            #Base query
            query = "SELECT * FROM northwind.Suppliers"

            #Add WHERE clause only if filters exist
            if filters:
                query += " WHERE " + " AND ".join(filters)

        view_table(query)
        conn.close()

##----------------------##
## Create Tab Functions ##
##----------------------##

def csv_instructions_create(selected_table):
    general_instructions = '''\n1. Follow the same column order as listed in the above table. \n2. Do not miss any column. \n3. Do not include extra columns that are not part of the table. \n4. Ensure data types in each column adhere to the specified data types. \n5. Ensure correct data in non null columns \n'''
    general_instructions_customers = '''\n1. Follow the same column order as listed in the above table. \n2. Do not miss any column. \n3. Do not include extra columns that are not part of the table. \n4. Ensure data types in each column adhere to the specified data types. \n5. Ensure correct data in non null columns \n 6. Ensure to use unique Customer IDs \n 7. Do not leave any value blank (add NA if unknown)'''
    general_instructions_employees = '''\n1. Follow the same column order as listed in the above table. \n2. Do not miss any column. \n3. Do not include extra columns that are not part of the table. \n4. Ensure data types in each column adhere to the specified data types. \n5. Ensure correct data in non null columns \n 6. Ensure data type of date columns in csv as Custom formatted to YYYY-MM-DD \n 7. Do not add any existing employee again'''

    if selected_table == "Categories":
        return general_instructions
    elif selected_table == "Customers":
        return general_instructions_customers
    elif selected_table == "Employees":
        return general_instructions_employees
    else:
        return general_instructions

def get_customer_ids():
    conn = connect_db()
    query = "SELECT DISTINCT CustomerID FROM northwind.Customers;"
    df = pd.read_sql(query, conn)
    customer_ids = df['CustomerID'].tolist()
    conn.close()
    return customer_ids

def get_employee_ids():
    conn = connect_db()
    query = "SELECT DISTINCT EmployeeID FROM northwind.Employees;"
    df = pd.read_sql(query, conn)
    employee_ids = df['EmployeeID'].tolist()
    conn.close()
    return employee_ids

def get_shipper_ids():
    conn = connect_db()
    query = "SELECT DISTINCT ShipperID FROM northwind.Shippers;"
    df = pd.read_sql(query, conn)
    shipper_ids = df['ShipperID'].tolist()
    conn.close()
    return shipper_ids

def get_supplier_ids():
    conn = connect_db()
    query = "SELECT DISTINCT SupplierID FROM northwind.Suppliers;"
    df = pd.read_sql(query, conn)
    supplier_ids = df['SupplierID'].tolist()
    conn.close()
    return supplier_ids

def get_category_ids():
    conn = connect_db()
    query = "SELECT DISTINCT CategoryID FROM northwind.Categories;"
    df = pd.read_sql(query, conn)
    category_ids = df['CategoryID'].tolist()
    conn.close()
    return category_ids

def get_existing_order_ids():
    conn = connect_db()
    query = "SELECT DISTINCT OrderID FROM northwind.Orders;"
    df = pd.read_sql(query, conn)
    order_ids = df['OrderID'].tolist()
    conn.close()
    return order_ids

def get_unit_price(product_id):
    conn = connect_db()
    query = f"SELECT UnitPrice FROM northwind.Products WHERE ProductID = {product_id};"
    df = pd.read_sql(query, conn)
    conn.close()

    if df.empty:
        st.error(f"Product ID {product_id} does not exist.")
        return None
    else:
        return float(df["UnitPrice"][0])

def create_new_order(customer_id,employee_id,order_date,required_date,shipped_date,ship_via,freight,ship_name,ship_address,ship_city,ship_region,ship_postal_code,ship_country):
    conn = connect_db()
    cursor = conn.cursor()

    sql = """
        INSERT INTO Orders (
            CustomerID, EmployeeID, OrderDate, RequiredDate, ShippedDate,
            ShipVia, Freight, ShipName, ShipAddress, ShipCity, ShipRegion,
            ShipPostalCode, ShipCountry
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    cursor.execute(sql, (customer_id,employee_id,order_date,required_date,shipped_date,ship_via,freight,ship_name,ship_address,ship_city,ship_region,ship_postal_code,ship_country))

    conn.commit()

    new_order_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return new_order_id

def create_new_product(product_name,supplier_id,category_id,quantity_per_unit,unit_price,units_in_stock,units_on_order,reorder_level,discontinued):
    conn = connect_db()
    cursor = conn.cursor()

    sql = """
            INSERT INTO Products
            (ProductName, SupplierID, CategoryID, QuantityPerUnit, UnitPrice,
            UnitsInStock, UnitsOnOrder, ReorderLevel, Discontinued)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

    cursor.execute(sql, (product_name,supplier_id,category_id,quantity_per_unit,unit_price,units_in_stock,units_on_order,reorder_level,discontinued))

    conn.commit()
    new_product_id = cursor.lastrowid 
    cursor.close()
    conn.close()

    return new_product_id

def check_for_primary_key_uniqueness(selected_table, uploaded_df):
    conn = connect_db()
    cur = conn.cursor()    

    # Step 1: Fetch table column details
    selected_table_df = fetch_table_column_details(selected_table)
    
    # Step 2: Identify the primary key column
    primary_key_col = selected_table_df.loc[selected_table_df['Key'] == 'PRI', 'Field'].values
    primary_key_col = primary_key_col[0]
    
    # Step 3: Fetch existing primary key values from the selected table
    existing_df = pd.read_sql(f"SELECT {primary_key_col} FROM {selected_table}", conn)
    conn.close()

    # Step 4: Take only that column from uploaded_df    
    uploaded_keys = uploaded_df[primary_key_col]

    # Step 5: Check for duplicates
    duplicates = uploaded_keys[uploaded_keys.isin(existing_df[primary_key_col])]

    if not duplicates.empty:
        return 0
    else:
        return 1

# def validate_df_against_schema(df_uploaded: pd.DataFrame, table_column_details: pd.DataFrame):
#     """Function to validate uploaded DataFrame against table schema"""
    
#     # Columns that should be ignored because database auto-handles them
#     system_cols = ("CreatedDate", "UpdatedDate")

#     # 1. Check for required columns (excluding system columns)
#     expected_cols = [
#         c for c in table_column_details["Field"].tolist()
#         if c not in system_cols
#     ]
    
#     # 1. Check for required columns
#     # expected_cols = table_column_details["Field"].tolist()
    
#     uploaded_cols = df_uploaded.columns.tolist()
#     # st.write(expected_cols)
#     # st.write(uploaded_cols) 

#     # Compare sets (exact, case-sensitive)
#     missing_cols = [c for c in expected_cols if c not in uploaded_cols]
#     # st.write(missing_cols)
#     if missing_cols:
#         st.error(f"Missing required columns:") 
#         st.write(missing_cols)
#     else:
#         required_cols_msg = 1
        
#     # 2. Check for NOT NULL constraints
#     not_null_columns = table_column_details.loc[table_column_details["Null"].str.upper() == "NO", "Field"].tolist()
#     # Identify columns that have NaN or empty string where they shouldn’t
#     columns_with_nulls = []
#     for col in not_null_columns:
#         if df_uploaded[col].isnull().sum()>0 or df_uploaded[col].isna().sum() or df_uploaded[col].eq("").sum()>0:
#             columns_with_nulls.append(col)
#     if columns_with_nulls:
#         st.error("The below columns have null values while they are not supposed to have null values:")
#         st.write(columns_with_nulls)
#     else:
#         not_null_msg = 1
    
#     return required_cols_msg, not_null_msg



def validate_df_against_schema(df_uploaded: pd.DataFrame, table_column_details: pd.DataFrame):
    """Function to validate uploaded DataFrame against table schema"""

    # Columns that should be ignored because database auto-handles them
    system_cols = ("CreatedDate", "UpdatedDate")

    # 1. Check for required columns (excluding system columns)
    expected_cols = [
        c for c in table_column_details["Field"].tolist()
        if c not in system_cols
    ]

    uploaded_cols = df_uploaded.columns.tolist()

    missing_cols = [c for c in expected_cols if c not in uploaded_cols]
    if missing_cols:
        st.error("Missing required columns:")
        st.write(missing_cols)
        required_cols_msg = 0
    else:
        required_cols_msg = 1

    # 2. Check for NOT NULL constraints (excluding system columns)
    not_null_columns = [
        c for c in table_column_details.loc[
            table_column_details["Null"].str.upper() == "NO", "Field"
        ].tolist()
        if c not in system_cols
    ]

    columns_with_nulls = []
    for col in not_null_columns:
        # Only validate columns ACTUALLY present in the uploaded CSV
        if col in df_uploaded:
            if (
                df_uploaded[col].isnull().sum() > 0
                or df_uploaded[col].isna().sum() > 0
                or df_uploaded[col].eq("").sum() > 0
            ):
                columns_with_nulls.append(col)

    if columns_with_nulls:
        st.error("The below columns have null values while they are NOT NULL in the database:")
        st.write(columns_with_nulls)
        not_null_msg = 0
    else:
        not_null_msg = 1

    return required_cols_msg, not_null_msg



##########################################################################################################################################################

def remove_existing_rows(df, table_name):
    """Return only rows whose key_cols combination does not exist in the table."""
    conn = connect_db()
    cur = conn.cursor()    
    key_cols = df.columns.tolist()
    # st.write(f"### Key Columns: {key_cols}")    
    keys = ", ".join(f"`{c}`" for c in key_cols)
    # st.write(f"### Key Columns: {keys}")
    query = f"SELECT {keys} FROM `{table_name}`"
    existing = pd.read_sql(query, conn)
    # st.write("### Existing Rows in Database")
    # st.dataframe(existing)
    # st.write(existing.dtypes)
    # st.write("### Uploaded DataFrame Rows")
    # # st.dataframe(df)
    # st.write(df.dtypes)
    conn.close()

    for col in key_cols:
        if existing[col].dtype == 'datetime64[ns]':
            df[col] = pd.to_datetime(df[col], errors='coerce')
            existing[col] = pd.to_datetime(existing[col], errors='coerce')
        else: 
           df[col] = df[col].astype(existing[col].dtype)
    
    
    # new_df = pd.concat([existing, df], ignore_index=True)
    # st.write("### Combined DataFrame for Duplicates Check")
    # st.dataframe(new_df)
    # duplicated_rows = new_df.duplicated().sum()
    # st.write(f"Number of Duplicated Rows based on all columns: {duplicated_rows}")
    # st.write("Datatypes converted")
    # st.write(existing.dtypes)
    try:
        # new_df = df[~df.apply(tuple, 1).isin(existing.apply(tuple, 1))]  
        new_df = pd.merge(existing, df, how='outer', indicator=True).query('_merge == "right_only"').drop('_merge',axis=1)

        # st.write("### New Rows after removing existing rows")
        # st.dataframe(new_df)
        return new_df 
    #     # Return in the same column order as original df
    #     new_df = new_df[df.columns]
    #     st.dataframe(new_df)
    except Exception as e:
        st.error(f"Error during concat-based filtering to find existing rows: {e}")
        return None  # If error, return original df

############################################################################################################################################

def insert_data_into_db(selected_table,table_column_details, df_uploaded):
    """Function to insert data into database"""
    conn = connect_db()
    cursor = conn.cursor()

    # 1. Drop any auto_increment column from the DataFrame and also the duplicated records    
    # Extract all columns and auto_increment ones
    # st.write(f"Connection Setup to Table: {selected_table}")
    all_cols = table_column_details["Field"].tolist()
    # st.write(f"All Columns in Table: {all_cols}")
    autoinc_cols = []
    for col_name in all_cols:
        if table_column_details.loc[table_column_details["Field"]==col_name, "Extra"].values[0].lower()=="auto_increment":
            autoinc_cols.append(col_name)
    # st.write(f"Auto-increment Columns to Exclude: {autoinc_cols}")
    df = df_uploaded.copy()
    for col in autoinc_cols:
        if col in df.columns:
            df = df.drop(columns=[col])
    # st.write("### DataFrame after dropping auto-increment columns")
    #st.dataframe(df,hide_index=True,use_container_width=True)

    # Drop any duplicated records:
    new_df = remove_existing_rows(df, selected_table)
    # st.write("Data to be created")
    # st.dataframe(new_df,hide_index=True,use_container_width=True)
    
    # Write the new_df to the selected table manually
    def _quote_ident_mysql(name: str) -> str:
        # Quote identifiers like table/column names for MySQL
        return "`" + str(name).replace("`", "``") + "`"

    try:
        # -- A. clean headers so we don't end up with 'nan' as a column name
        # trim header strings
        new_df.columns = [str(c).strip() for c in new_df.columns]
        # drop any blank/NaN headers
        bad_headers = [c for c in new_df.columns if pd.isna(c) or str(c).strip() == ""]
        if bad_headers:
            st.warning(f"Dropping columns with missing headers: {bad_headers}")
            new_df = new_df.drop(columns=bad_headers)

        # -- B. only keep columns that actually exist in the table
        # valid_cols = table_column_details["Field"].astype(str).tolist()
        valid_cols = [
                        col for col in table_column_details["Field"].astype(str).tolist()
                        if col not in ("CreatedDate", "UpdatedDate")
                    ]
        cols = [c for c in new_df.columns if c in valid_cols]
        if not cols:
            st.error("None of the DataFrame columns match the table columns.")
            return 0

        # -- C. build INSERT with quoted identifiers
        col_list = ", ".join(_quote_ident_mysql(c) for c in cols)
        placeholders = ", ".join(["%s"] * len(cols))
        insert_query = f"INSERT INTO {_quote_ident_mysql(selected_table)} ({col_list}) VALUES ({placeholders})"

        # st.write(f"Using columns: {cols}")
        # st.write(insert_query)

        # -- D. convert NaN/NaT to None in values (so DB receives NULL, not 'nan')
        def row_tuple(row):
            vals = []
            for c in cols:
                v = row[c]
                if (isinstance(v, (float, np.floating)) and np.isnan(v)) or pd.isna(v):
                    vals.append(None)
                else:
                    vals.append(v)
            return tuple(vals)

        data = [row_tuple(r) for _, r in new_df.iterrows()]
        # st.write(data[:5])  # preview a few rows

        # -- E. execute
        if not data:
            st.info("No rows to insert.")
            return 2

        cursor.executemany(insert_query, data)
        conn.commit()
        # st.success(f"Inserted {len(data)} new rows into {selected_table}.")
        return 1

    except IntegrityError as ie:
        conn.rollback()
        st.error(f"Integrity error: {ie}")
        return 0
    except mysql.connector.Error as db_err:
        conn.rollback()
        st.error(f"MySQL error: {db_err}")
        return 0
    finally:
        cursor.close()
        conn.close()          
        
        
 ## Update Tab Functions ##

def create_new_records(selected_table):
    # #Get tables to select from
    # tables_list = get_tables()
    # # all_tables = get_tables()
    # # master_tables = ["Categories","Employees","Customers","Suppliers","Shippers"]
    # # tables_list = [table for table in all_tables if table in master_tables]
    # selected_table = st.selectbox(":blue[Select Table to Create New Record]", tables_list)

    bulk_upload = ["Categories", "Customers", "Employees", "Shippers", "Suppliers"]
    if selected_table in bulk_upload:    
        # #Fetch columns of the selected table
        for table_name in bulk_upload:
            if selected_table == table_name:
                table_column_details = fetch_table_column_details(table_name)
                # column_constraint_df = pd.DataFrame(list(zip(columns, constraints, column_key, column_autoincr)), columns=['Column Header', 'Data Type', 'Key Details', 'Auto Increment'])

        # #Provide Instructions for CSV upload
        # Remove audit columns so they are not expected in CSV
        system_cols = ["CreatedDate", "UpdatedDate"]
        table_column_details = table_column_details[~table_column_details["Field"].isin(system_cols)]
        
        with st.popover("Data Upload Instructions"):
            st.warning(f"Ensure the {selected_table} data is in CSV format with the below listed details.")
            st.dataframe(table_column_details,hide_index=True,use_container_width=True)
            st.info(f'{csv_instructions_create(selected_table)}')
        
        # #File uploader for CSV    
        uploaded_file = st.file_uploader(":blue[Upload CSV File to be created]", type=["csv"], key ="create1")
        
        # #Process & verify the uploaded file
        if uploaded_file is not None:
            # #Read CSV safely
            try:
                df_uploaded = pd.read_csv(uploaded_file)
            except Exception as e:
                st.error(f"❌ Having problem with the file uploaded : {e}")
            else:
                # #Check for empty csv
                if df_uploaded.empty:
                    st.error("❌ The uploaded CSV file has no records. Please provide at least one row of data to insert or update.")
                else:
                    # #Proceed to validation only if data exists
                    # result = validate_df_against_schema(df_uploaded, table_column_details)
                    required_cols_msg, not_null_msg = validate_df_against_schema(df_uploaded, table_column_details)
                    if required_cols_msg == 1 and not_null_msg == 1:
                        if selected_table == "Customers":
                            primary_key_check_value = check_for_primary_key_uniqueness(selected_table,df_uploaded)
                            if primary_key_check_value == 1:
                                st.success("All required columns are present and there are no null values in NOT NULL columns.")
                                st.info(f"Below data would be created in {selected_table} table in the database, if there are no data type & duplication discrepancies")
                                st.dataframe(df_uploaded, hide_index=True, use_container_width=True)
                                insert_button = st.button("Insert Records into Database")
                            else:
                                st.error(f"Recheck Primary key allocation")

                        else:
                            st.success("All required columns are present and there are no null values in NOT NULL columns.")
                            st.info(f"Below data would be created in {selected_table} table in the database, if there are no data type & duplication discrepancies")
                            st.dataframe(df_uploaded, hide_index=True, use_container_width=True)
                            
                            insert_button = st.button("Insert Records into Database", key = "create")
                        
                        try:
                            if insert_button:
                                insert_value = insert_data_into_db(selected_table,table_column_details, df_uploaded)
                                if insert_value == 1:
                                    st.success(f"Successfully inserted data in to database")
                                elif insert_value == 2:
                                    st.info(f"No data created as there was no new data in the uploaded csv")
                                else:
                                    st.error(f"Error inserting data into database.")
                    
                        except Exception as e:
                            pass
                            # st.error(f"Error inserting data into database: {e}")
    elif selected_table == "OrderDetails":
        if "pending_order_lines" not in st.session_state:
            st.session_state.pending_order_lines = []

        with st.popover("Data Upload Instructions"):
            st.info(":green[You could create details of only one order at a time]")
            st.warning("Ensure OrderID is created in Orders table before creating OrderDetails for that OrderID.")
            
        order_id = st.number_input(":blue[Enter Valid Order ID]", format="%0.0f")
        order_id = int(order_id)
        existing_order_ids = get_existing_order_ids()
        if order_id in existing_order_ids:
            with st.expander(f"Click to enter Order Details of {order_id}"):
                product_id = st.number_input("Product ID", min_value=1)
                unit_price = None
                productidvalidty = 0
                if product_id:
                    unit_price = get_unit_price(product_id)

                if unit_price is not None:
                    st.success(f"Unit Price for Product {product_id}: **${unit_price:.2f}**")
                    productidvalidty = 1
                else:
                    # st.error("Product ID not found in Products table")
                    productidvalidty = 0
                if productidvalidty ==1:
                    quantity = st.number_input("Quantity", min_value=1)
                    discount = st.number_input("Discount (0 to 1)", min_value=0.0, max_value=1.0)
                    
                    add_button = st.button("Add Line Item")
                    st.info("Edit the existing input fields to add new line item and click Add Line Item again to append the details.")
                    if add_button:
                        st.session_state.pending_order_lines.append({
                                                                        "order_id": int(order_id),
                                                                        "product_id": int(product_id),
                                                                        "unit_price": float(unit_price),
                                                                        "quantity": int(quantity),
                                                                        "discount": float(discount)
                                                                    })
                    
                    if len(st.session_state.pending_order_lines) > 0:
                        st.subheader("Pending Line Items (Not Inserted Yet):")
                        st.table(st.session_state.pending_order_lines)
                    
                    insert_button = st.button("Insert OrderDetails into Database")
                    
                    try:
                        if insert_button:
                            connection = connect_db()
                            cursor = connection.cursor()

                            sql = """
                                        INSERT INTO northwind.OrderDetails (OrderID, ProductID, UnitPrice, Quantity, Discount)
                                        VALUES (%s, %s, %s, %s, %s)
                                    """
                            for item in st.session_state.pending_order_lines:
                                cursor.execute(sql, (
                                    item["order_id"],
                                    item["product_id"],
                                    item["unit_price"],
                                    item["quantity"],
                                    item["discount"]
                                ))
                            # cursor.execute(sql, (int(order_id), int(product_id), float(unit_price), int(quantity), float(discount)))
                            connection.commit()
                            cursor.close()
                            connection.close()
                            st.success(f"Order Detail created successfully with OrderID: {order_id}")
                            st.session_state.pending_order_lines = []

                    except Exception as e:
                        st.error(f"Error inserting data into database: {e}")
        else:
            st.error("Order ID not found in Orders table. Please enter a valid Order ID.")
            
    elif selected_table == "Orders":
        with st.popover("Data Upload Instructions"):

            st.info(":green[Fill the details to create a new order.]")
            st.warning("Ensure that the Customer ID, Employee ID, and Shipper ID exist in their respective tables before creating a new order.")

        with st.expander("Click to Create a new order"):
            # Foreign Key Inputs
            customerid_list = get_customer_ids()
            employeeidlist = get_employee_ids()
            shipvia_list = get_shipper_ids()
            
            customer_id = st.text_input("Customer ID") 
            # st.selectbox("Customer ID", customerid_list)
            employee_id = st.selectbox("Employee ID", employeeidlist)
            ship_via = st.selectbox("Shipper ID", shipvia_list)

            #Date Inputs
            order_date = st.date_input("Order Date")
            required_date = st.date_input("Required Date")
            shipped_date = st.date_input("Shipped Date")

            #Convert dates to proper string for MySQL
            order_date = str(order_date) if order_date else None
            required_date = str(required_date) if required_date else None
            shipped_date = str(shipped_date) if shipped_date else None

            # Other fields
            freight = st.number_input("Freight", min_value=0.0, format="%.2f")
            ship_name = st.text_input("Ship Name")
            ship_address = st.text_input("Ship Address")
            ship_city = st.text_input("Ship City")
            ship_region = st.text_input("Ship Region")
            ship_postal_code = st.text_input("Ship Postal Code")
            ship_country = st.text_input("Ship Country")

            
            insert_button = st.button("Insert Order into Database")
            if (customer_id is not None):
                if customer_id not in customerid_list:
                    customer_id = "NULL"
                    st.warning("Customer ID not found in Customers table. Please enter a valid Customer ID.")
                    # insert_button = False
            
            
            if insert_button:
                try:
                    new_order_id = create_new_order(
                                                        customer_id,
                                                        employee_id,
                                                        order_date,
                                                        required_date,
                                                        shipped_date,
                                                        ship_via,
                                                        freight,
                                                        ship_name,
                                                        ship_address,
                                                        ship_city,
                                                        ship_region,
                                                        ship_postal_code,
                                                        ship_country
                                                    )

                    st.success(f"Order {new_order_id} created successfully!")

                except Exception as e:
                    st.error(f"Error creating order: {e}")
        
    else:
        with st.popover("Data Upload Instructions"):
            st.info(":green[Fill the details to create a new product.]")
            st.warning("Ensure the Supplier ID and Category ID exist in their corresponding tables before creating a product.")

        with st.expander("Click to enter Product Details"):

            supplier_list = get_supplier_ids()      
            category_list = get_category_ids()      
            
            product_name = st.text_input("Product Name")
            supplier_id = st.selectbox("Supplier ID", supplier_list)
            category_id = st.selectbox("Category ID", category_list)

            quantity_per_unit = st.text_input("Quantity Per Unit")

            unit_price = st.number_input("Unit Price", min_value=0.0, format="%.2f")
            units_in_stock = st.number_input("Units In Stock", min_value=0, step=1)
            units_on_order = st.number_input("Units On Order", min_value=0, step=1)
            reorder_level = st.number_input("Reorder Level", min_value=0, step=1)

            discontinued = st.selectbox("Discontinued?", [0, 1])  # 0 = No, 1 = Yes

            insert_button = st.button("Insert Product into Database")

            if insert_button:
                if not product_name:
                    st.error("Product Name cannot be empty.")
                elif discontinued is None:
                    st.error("Please select if the product is discontinued or not.")
                else:
                    try:
                        new_product_id = create_new_product(product_name,supplier_id,category_id,quantity_per_unit,unit_price,units_in_stock,units_on_order,reorder_level,discontinued)

                        st.success(f"Product created successfully! ProductID = {new_product_id}")

                    except Exception as e:
                        st.error(f"Error creating product: {e}")
 
##----------------------##
## Update Tab Functions ##
##----------------------## 

def csv_instructions_update(selected_table):
    general_instructions = '''\n1. Follow the same column order as listed in the above table. \n2. Do not miss any column. \n3. Do not include extra columns that are not part of the table. \n4. Ensure data types of values in updated column adhere to the specified data types. \n5. Retain the values as is for all the other columns \n6. Ensure to use existing values of primary keys\n'''
    general_instructions_customers = '''\n1. Follow the  same column order as listed in the above table. \n2. Do not miss any column. \n3. Do not include extra columns that are not part of the table. \n4. Ensure data types of values in updated column adhere to the specified data types. \n5. Retain the values as is for all the other columns \n 6. Ensure to use existing Customer IDs \n 7. Do not leave any value blank (add NA if unknown)'''
    general_instructions_employees = '''\n1. Follow the same column order as listed in the above table. \n2. Do not miss any column. \n3. Do not include extra columns that are not part of the table. \n4. Ensure data types of values in updated column adhere to the specified data types. \n5. Retain the values as is for all the other columns except any date time column \n 6. Ensure data type of date columns in csv as Custom formatted to YYYY-MM-DD \n 7. Ensure to use existing Employee IDs'''

    if selected_table == "Categories":
        return general_instructions
    elif selected_table == "Customers":
        return general_instructions_customers
    elif selected_table == "Employees":
        return general_instructions_employees
    else:
        return general_instructions
  
def update_records(table_name, df_uploaded, table_column_details):
    """
    Compares each row in df_uploaded with the corresponding row in the 
    base table (based on PK). If any non-PK column differs, updates DB.
    """

    # Identify primary key
    primary_key_column = table_column_details.loc[table_column_details['Key'] == 'PRI', 'Field'].values[0]
    # st.write(f"Primary Key Column: {primary_key_column}")
    
    # Identify updatable columns (exclude PK)
    updatable_columns = table_column_details[table_column_details['Field'] != primary_key_column]["Field"].tolist()
    # st.write(f"Updatable Columns: {updatable_columns}")
    updated_rows = 0
    skipped_rows = 0

    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    # Read entire base table into memory for comparison
    base_query = f"SELECT * FROM {table_name}"
    base_df = pd.read_sql(base_query, conn)
    # st.dataframe(base_df, hide_index=True,use_container_width=False)
    # # Convert base_df PK to int for safe comparison
    # base_df[primary_key_column] = base_df[primary_key_column].astype(int)

    # Loop uploaded rows
    for _, new_row in df_uploaded.iterrows():
        
        pk_value = new_row[primary_key_column] #int(new_row[primary_key_column])

        # Extract corresponding base row
        base_row = base_df[base_df[primary_key_column] == pk_value]

        if base_row.empty:
            skipped_rows += 1
            continue   # PK validation already done earlier

        base_row = base_row.iloc[0]

        # Track columns that changed
        changed_columns = {}
        
        for col in updatable_columns:
            old_val = base_row[col]
            new_val = new_row[col]

            # Normalize NaN / None / empty equalities
            if pd.isna(old_val) and pd.isna(new_val):
                continue

            if str(old_val) != str(new_val):
                changed_columns[col] = new_val
        # st.write(changed_columns)
        # If nothing changed → skip
        if not changed_columns:
            skipped_rows += 1
            continue

        # Build dynamic update SQL
        set_clause = ", ".join([f"{col} = %s" for col in changed_columns.keys()])
        sql = f"UPDATE {table_name} SET {set_clause} WHERE {primary_key_column} = %s"

        values = list(changed_columns.values()) + [pk_value]

        cursor.execute(sql, values)
        updated_rows += 1

    conn.commit()
    cursor.close()
    conn.close()
    if updated_rows > 0:
        st.success(f"Total Number of rows updated: {updated_rows}")
    else:
        st.info("No records were updated as there were no changes detected.")
 
def validate_df_against_schema_update(table_name, df_uploaded, table_column_details):
    """Function to validate uploaded DataFrame against table schema"""
    
    # # 1. Check for required columns
    # expected_cols = table_column_details["Field"].tolist()
    
    system_cols = ("CreatedDate", "UpdatedDate")
    expected_cols = [
                        c for c in table_column_details["Field"].tolist()
                        if c not in system_cols
                    ]

    
    uploaded_cols = df_uploaded.columns.tolist()
    # st.write(expected_cols)
    # st.write(uploaded_cols) 

    # Compare sets (exact, case-sensitive)
    missing_cols = [c for c in expected_cols if c not in uploaded_cols]
    
    # st.write(missing_cols)
    if missing_cols:
        st.error(f"Missing required columns:") 
        st.write(missing_cols)
    else:
        required_cols_msg = 1
        
    # 2. Check for NOT NULL constraints
    # not_null_columns = table_column_details.loc[table_column_details["Null"].str.upper() == "NO", "Field"].tolist()
    not_null_columns = [
                            c for c in table_column_details.loc[
                                table_column_details["Null"].str.upper() == "NO", "Field"
                            ].tolist()
                            if c not in system_cols
                        ]
    
    # Identify columns that have NaN or empty string where they shouldn’t
    columns_with_nulls = []
    # for col in not_null_columns:
    #     if df_uploaded[col].isnull().sum()>0 or df_uploaded[col].isna().sum() or df_uploaded[col].eq("").sum()>0:
    #         columns_with_nulls.append(col)
            
            
    for col in not_null_columns:
        # SAFETY CHECK – skip system columns or missing columns
        if col not in df_uploaded.columns:
            continue

        if (
            df_uploaded[col].isnull().sum() > 0
            or df_uploaded[col].isna().sum() > 0
            or df_uploaded[col].eq("").sum() > 0
        ):
            columns_with_nulls.append(col)

            
    if columns_with_nulls:
        st.error("The below columns have null values while they are not supposed to have null values:")
        st.write(columns_with_nulls)
    else:
        not_null_msg = 1

    # 3. Check for primary key existence in the database
    primary_key_column = table_column_details.loc[table_column_details['Key'] == 'PRI', 'Field'].values[0]
    # st.write(primary_key_column)
    
    conn = connect_db()
    query = f"SELECT DISTINCT {primary_key_column} FROM northwind.{table_name}"
    base_table_primary_key_values = pd.read_sql(query, conn)
    conn.close()
    # st.dataframe(base_table_primary_key_values, hide_index=True,use_container_width=False)
    
    df_uploaded_primary_key_values = df_uploaded[primary_key_column].unique()    
    # st.dataframe(df_uploaded_primary_key_values, hide_index=True,use_container_width=False)
    
    # missing_pk_values = [
    #                         int(pk) for pk in df_uploaded_primary_key_values
    #                         if int(pk) not in base_table_primary_key_values[primary_key_column].astype(int).values
    #                     ]

# Convert everything to string for comparison (safe for ALL PK types)
    base_pk_list = base_table_primary_key_values[primary_key_column].astype(str).tolist()
    uploaded_pk_list = df_uploaded_primary_key_values.astype(str).tolist()

    missing_pk_values = [pk for pk in uploaded_pk_list if pk not in base_pk_list]

    if missing_pk_values:
        st.error("❌ These primary key values from uploaded CSV do NOT exist in the base table:")
        st.write(missing_pk_values)
        primary_key_availability_check = 0
    else:
        # st.success("✅ All primary key values in the uploaded CSV exist in the base table.")
        primary_key_availability_check = 1

    return required_cols_msg, not_null_msg, primary_key_availability_check
     
def update_records_in_existing_table(selected_table,table_column_details):
    """Function to update records in existing table"""
    bulk_upload = ["Categories", "Customers", "Employees", "Shippers", "Suppliers"]
    if selected_table in bulk_upload:    
        # st.header("Update Categories from CSV")
        # Remove audit columns so they are not expected in CSV
        system_cols = ["CreatedDate", "UpdatedDate"]
        table_column_details = table_column_details[~table_column_details["Field"].isin(system_cols)]

        with st.popover(f"Update Instructions for {selected_table}"):
            st.warning(f"Ensure the {selected_table} data is in CSV format with the below listed details.")
            st.dataframe(table_column_details,hide_index=True,use_container_width=True)
            st.info(f'{csv_instructions_update(selected_table)}')

        # File uploader
        uploaded_file_update = st.file_uploader(":blue[Upload CSV File fo records to be updated]", type=["csv"],key="update2")
        
        # #Process & verify the uploaded file
        if uploaded_file_update is not None:
            # #Read CSV safely
            try:
                df_uploaded = pd.read_csv(uploaded_file_update)
            except Exception as e:
                st.error(f"❌ Having problem with the file uploaded : {e}")
            else:
                # #Check for empty csv
                if df_uploaded.empty:
                    st.error("❌ The uploaded CSV file has no records. Please provide at least one row of data to update.")
                else:
                    # #Proceed to validation only if data exists
                    # result = validate_df_against_schema(df_uploaded, table_column_details)
                    required_cols_msg, not_null_msg, primary_key_availability_check = validate_df_against_schema_update(selected_table, df_uploaded, table_column_details)
                
                try:
                    if required_cols_msg == 1 and not_null_msg == 1 and primary_key_availability_check == 1:
                        bulk_upload_update_button = st.button("Update Records in Database")
                        # st.write("All validations passed. Ready to update records.")
                        # st.write("reqiored_cols_msg:", required_cols_msg)
                        # st.write("not_null_msg:", not_null_msg)
                        # st.write("primary_key_availability_check:", primary_key_availability_check)   
                        
                        if bulk_upload_update_button:
                            update_records(selected_table, df_uploaded, table_column_details)
                            # st.success("Table updated Successfully!")
                    else:
                        # st.write("reqiored_cols_msg:", required_cols_msg)
                        # st.write("not_null_msg:", not_null_msg)
                        # st.write("primary_key_availability_check:", primary_key_availability_check)   
                        st.error("Please fix the above issues and re-upload the CSV file.")
                        
                except Exception as e:
                    st.error(f"Unknown error occurred. {e}")

    elif selected_table == "OrderDetails":
        # Remove audit columns so they are not expected in CSV
        system_cols = ["CreatedDate", "UpdatedDate"]
        table_column_details = table_column_details[~table_column_details["Field"].isin(system_cols)]
                
        with st.popover(f"Update Instructions for {selected_table}"):
            st.warning(f"Ensure the {selected_table} data is in CSV format with the below listed details.")
            st.dataframe(table_column_details,hide_index=True,use_container_width=True)
            st.info(f'{csv_instructions_update(selected_table)}')
            
        conn = connect_db()
        orderid_query = f'''select distinct(OrderID) from northwind.OrderDetails;'''
        orderid_df = pd.read_sql(orderid_query, conn)
        orderid_list = orderid_df['OrderID'].tolist()
        selected_orderid = st.selectbox(":blue[Select OrderID to update]", orderid_list)
        
        query = f'''select * from northwind.OrderDetails where OrderID = {selected_orderid};'''
        orderdetails_df = pd.read_sql(query, conn)
        # edited_df = st.data_editor(orderdetails_df, use_container_width=False,key="edited_orderdetails")
        
        # Load ProductID list & their prices
        product_query = "SELECT ProductID, UnitPrice FROM northwind.Products;"
        product_df = pd.read_sql(product_query, conn)

        valid_products = product_df["ProductID"].tolist()
        product_price_map = dict(zip(product_df["ProductID"], product_df["UnitPrice"]))        
        
        col1, col2 = st.columns(2, border=True)
        with col1:
            st.write("### Update OrderDetails below")
            
            editable_df = st.data_editor(
                                            orderdetails_df,
                                            use_container_width=False,
                                            key="edited_orderdetails",
                                            hide_index=True,
                                            column_config={
                                                            "OrderID": st.column_config.Column(disabled=True),
                                                            "ProductID": st.column_config.Column(disabled=False),
                                                            "UnitPrice": st.column_config.Column(disabled=True),
                                                            "Quantity": st.column_config.Column(disabled=False),
                                                            "Discount": st.column_config.Column(disabled=False)
                                                        }
                                        )


    # Validate & auto-update UnitPrice
        error_flag = False
        updated_df = editable_df.copy()

        for idx, row in updated_df.iterrows():
            pid = row["ProductID"]
            discount = row["Discount"]

            # 1️⃣ Validate ProductID
            if pid not in valid_products:
                st.error(f"❌ ProductID {pid} not available in Products table (row {idx+1})")
                error_flag = True
            else:
                updated_df.at[idx, "UnitPrice"] = product_price_map[pid]

            # 2️⃣ Validate Discount
            if not (0 <= discount <= 1):
                st.error(f"❌ Discount {discount} is invalid in row {idx+1}. It must be between 0 and 1.")
                error_flag = True

        with col2:
            st.write("### Updated OrderDetails Preview")
            st.dataframe(updated_df, hide_index=True,use_container_width=False)
        
        orderdetails_update_button = st.button("Update OrderDetails", key="update_orderdetails")

        if orderdetails_update_button:
            if error_flag:
                st.error("❌ Cannot update. Fix invalid line items before saving.")
            else:
                # st.success("✔ Validations passed. Updating database...")

                cursor = conn.cursor()

                try:
                    # Loop through each row and update based on OrderID + ProductID
                    for idx, row in updated_df.iterrows():

                        update_query = """
                                            UPDATE northwind.OrderDetails
                                            SET ProductID = %s,
                                                UnitPrice = %s,
                                                Quantity = %s,
                                                Discount = %s
                                            WHERE OrderID = %s AND ProductID = %s;
                                        """

                        cursor.execute(update_query, (
                                                        int(row["ProductID"]),
                                                        float(row["UnitPrice"]),
                                                        int(row["Quantity"]),
                                                        float(row["Discount"]),
                                                        int(row["OrderID"]),
                                                        int(orderdetails_df.loc[idx, "ProductID"])   # old ProductID to match row
                                                    ))

                    conn.commit()
                    st.success("✅ OrderDetails updated successfully!")

                except Exception as e:
                    conn.rollback()
                    st.error(f"❌ Database update failed: {e}")

                finally:
                    cursor.close()
                    conn.close()

    elif selected_table == "Orders":
        # Remove audit columns so they are not expected in CSV
        system_cols = ["CreatedDate", "UpdatedDate"]
        table_column_details = table_column_details[~table_column_details["Field"].isin(system_cols)]

        with st.popover(f"Update Instructions for {selected_table}"):
            st.warning("Ensure the Orders data is correct.")
            st.dataframe(table_column_details, hide_index=True, use_container_width=True)

        conn = connect_db()

        # 1. Load list of Orders
        order_query = "SELECT DISTINCT(OrderID) FROM northwind.Orders;"
        orders_df = pd.read_sql(order_query, conn)
        order_list = orders_df["OrderID"].tolist()

        selected_orderid = st.selectbox(":blue[Select OrderID to update]", order_list)

        # 2. Load selected order row
        query = f"SELECT * FROM northwind.Orders WHERE OrderID = {selected_orderid};"
        order_df = pd.read_sql(query, conn)

        # 3. Load reference tables for validation
        emp_df = pd.read_sql("SELECT EmployeeID FROM northwind.Employees;", conn)
        shipper_df = pd.read_sql("SELECT ShipperID FROM northwind.Shippers;", conn)

        valid_employees = emp_df["EmployeeID"].tolist()
        valid_shippers = shipper_df["ShipperID"].tolist()

        # Editable columns
        disabled_cols = ["OrderID", "CustomerID", "OrderDate", "ShippedDate"]
        col1, col2 = st.columns(2, border=True)
        with col1:
            st.write("### Update Orders Information")

            editable_df = st.data_editor(
                order_df,
                use_container_width=False,
                key="edited_orders",
                hide_index=True,
                column_config={
                    col: st.column_config.Column(disabled=True if col in disabled_cols else False)
                    for col in order_df.columns
                }
            )

        # Validation
        error_flag = False
        updated_df = editable_df.copy()

        for idx, row in updated_df.iterrows():

            emp_id = row["EmployeeID"]
            ship_via = row["ShipVia"]

            # Validate EmployeeID
            if emp_id not in valid_employees:
                st.error(f"❌ EmployeeID {emp_id} does not exist in Employees table (row {idx+1}).")
                error_flag = True

            # Validate ShipVia
            if ship_via not in valid_shippers:
                st.error(f"❌ ShipVia {ship_via} does not exist in Shippers table (row {idx+1}).")
                error_flag = True
        with col2:
            st.write("### Updated Orders Preview")
            st.dataframe(updated_df, hide_index=True, use_container_width=False)

        update_orders_btn = st.button("Update Orders", key="update_orders")

        if update_orders_btn:
            if error_flag:
                st.error("❌ Cannot update. Fix invalid data and try again.")
            else:
                # st.success("✔ Validations passed. Updating database...")

                cursor = conn.cursor()

                try:
                    # Only one row in Orders table per OrderID
                    row = updated_df.iloc[0]

                    update_query = """
                                        UPDATE northwind.Orders
                                        SET EmployeeID = %s,
                                            RequiredDate = %s,
                                            ShipVia = %s,
                                            Freight = %s,
                                            ShipName = %s,
                                            ShipAddress = %s,
                                            ShipCity = %s,
                                            ShipRegion = %s,
                                            ShipPostalCode = %s,
                                            ShipCountry = %s
                                        WHERE OrderID = %s;
                                    """

                    cursor.execute(update_query, (
                                                    int(row["EmployeeID"]),
                                                    row["RequiredDate"], 
                                                    int(row["ShipVia"]),
                                                    float(row["Freight"]),
                                                    row["ShipName"],
                                                    row["ShipAddress"],
                                                    row["ShipCity"],
                                                    row["ShipRegion"],
                                                    row["ShipPostalCode"],
                                                    row["ShipCountry"],
                                                    int(row["OrderID"])
                                                ))

                    conn.commit()
                    st.success("✅ Orders table updated successfully!")

                except Exception as e:
                    conn.rollback()
                    st.error(f"❌ Database update failed: {e}")

                finally:
                    cursor.close()
                    conn.close()
    elif selected_table == "Products":
        # Remove audit columns so they are not expected in CSV
        system_cols = ["CreatedDate", "UpdatedDate"]
        table_column_details = table_column_details[~table_column_details["Field"].isin(system_cols)]

        with st.popover(f"Update Instructions for {selected_table}"):
            st.warning("Ensure the Products data is correct.")
            st.dataframe(table_column_details, hide_index=True, use_container_width=True)

        conn = connect_db()

        # 1. Load list of Products
        products_query = "SELECT DISTINCT(ProductID) FROM northwind.Products;"
        products_df = pd.read_sql(products_query, conn)
        product_list = products_df["ProductID"].tolist()

        selected_productid = st.selectbox(":blue[Select ProductID to update]", product_list)

        # 2. Load selected product row
        query = f"SELECT * FROM northwind.Products WHERE ProductID = {selected_productid};"
        product_df = pd.read_sql(query, conn)

        # 3. Load reference tables for validation
        supplier_df = pd.read_sql("SELECT SupplierID FROM northwind.Suppliers;", conn)
        valid_suppliers = supplier_df["SupplierID"].tolist()

        # Editable columns
        disabled_cols = ["ProductID", "ProductName", "CategoryID"]

        col1, col2 = st.columns(2, border=True)

        with col1:
            st.write("### Update Product Information")

            editable_df = st.data_editor(
                                            product_df,
                                            use_container_width=False,
                                            key="edited_products",
                                            hide_index=True,
                                            column_config={
                                                col: st.column_config.Column(disabled=True if col in disabled_cols else False)
                                                for col in product_df.columns
                                            }
                                        )

        # Validation
        error_flag = False
        updated_df = editable_df.copy()

        for idx, row in updated_df.iterrows():

            supp_id = row["SupplierID"]

            # Validate SupplierID
            if supp_id not in valid_suppliers:
                st.error(f"❌ SupplierID {supp_id} does not exist in Suppliers table (row {idx+1}).")
                error_flag = True

        with col2:
            st.write("### Updated Products Preview")
            st.dataframe(updated_df, hide_index=True, use_container_width=False)

        update_products_btn = st.button("Update Product", key="update_products")

        if update_products_btn:
            if error_flag:
                st.error("❌ Cannot update. Fix invalid data and try again.")
            else:
                cursor = conn.cursor()

                try:
                    # Only one row in Products table per ProductID
                    row = updated_df.iloc[0]

                    update_query = """
                                        UPDATE northwind.Products
                                        SET SupplierID = %s,
                                            QuantityPerUnit = %s,
                                            UnitPrice = %s,
                                            UnitsInStock = %s,
                                            UnitsOnOrder = %s,
                                            ReorderLevel = %s,
                                            Discontinued = %s
                                        WHERE ProductID = %s;
                                    """

                    cursor.execute(update_query, (
                                                    int(row["SupplierID"]),
                                                    row["QuantityPerUnit"],
                                                    float(row["UnitPrice"]),
                                                    int(row["UnitsInStock"]),
                                                    int(row["UnitsOnOrder"]),
                                                    int(row["ReorderLevel"]),
                                                    int(row["Discontinued"]),
                                                    int(row["ProductID"])
                                                ))

                    conn.commit()
                    st.success("✅ Product updated successfully!")

                except Exception as e:
                    conn.rollback()
                    st.error(f"❌ Database update failed: {e}")

                finally:
                    cursor.close()
                    conn.close()

##----------------------##
## Delete Tab Functions ##
##----------------------##      
def delete_records_in_existing_table(selected_table, table_column_details):

    st.write(f"### Delete Records from {selected_table}")

    conn = connect_db()
    cursor = conn.cursor()

    # ------------------------------
    # 1️⃣ GET PRIMARY KEY COLUMN(S)
    # ------------------------------
    pk_query = f"""
        SELECT COLUMN_NAME 
        FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
        WHERE TABLE_SCHEMA = DATABASE()
          AND TABLE_NAME = '{selected_table}'
          AND CONSTRAINT_NAME = 'PRIMARY';
    """
    cursor.execute(pk_query)
    pk_cols = [row[0] for row in cursor.fetchall()]

    if not pk_cols:
        st.error("❌ No primary key found. Cannot delete.")
        return

    st.info(f"Primary Key(s): **{', '.join(pk_cols)}**")

    # -------------------------------------
    # 2️⃣ LOAD EXISTING PK VALUES FROM TABLE
    # -------------------------------------
    pk_col_expr = ", ".join(pk_cols)
    fetch_query = f"SELECT {pk_col_expr} FROM {selected_table};"
    df_pk_values = pd.read_sql(fetch_query, conn)

    if df_pk_values.empty:
        st.warning("No records available to delete.")
        return

    # Make PK values user-friendly for selection
    df_pk_values["display"] = df_pk_values.astype(str).agg(" | ".join, axis=1)

    selected_keys = st.multiselect(
        f"Select {selected_table} records to delete",
        df_pk_values["display"].tolist()
    )

    if not selected_keys:
        return

    # Convert selected display strings → dicts of PK values
    selected_pk_dicts = []
    for val in selected_keys:
        parts = val.split(" | ")
        pk_vals = {pk_cols[i]: parts[i] for i in range(len(pk_cols))}
        selected_pk_dicts.append(pk_vals)

    # -----------------------------
    # 3️⃣ CHECK FOR DEPENDENCIES
    # -----------------------------
    st.divider()
    st.write("### Dependencies")

    dependencies_query = f"""
        SELECT TABLE_NAME, COLUMN_NAME 
        FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
        WHERE REFERENCED_TABLE_SCHEMA = DATABASE()
          AND REFERENCED_TABLE_NAME = '{selected_table}';
    """

    cursor.execute(dependencies_query)
    deps = cursor.fetchall()

    if deps:
        st.warning("⚠ These tables have foreign key references to this below table(s):")
        for table, col in deps:
            st.write(f"- **{table}** (FK column: `{col}`)")
        st.error("Deleting these records *may also delete* related records due to CASCADE/SET NULL.")
    else:
        st.success("No dependency issues. Safe to delete.")

    # ------------------------------
    # 4️⃣ DELETE BUTTON + CONFIRM
    # ------------------------------
    if st.button("⚠ Delete Selected IDs", type="primary"):

        try:
            for pk_vals in selected_pk_dicts:
                where_clause = " AND ".join([f"{col} = %s" for col in pk_vals.keys()])
                delete_query = f"DELETE FROM {selected_table} WHERE {where_clause}"

                cursor.execute(delete_query, list(pk_vals.values()))

            conn.commit()
            st.success("✅ Records deleted successfully!")

        except Exception as e:
            conn.rollback()
            st.error(f"❌ Delete failed: {e}")

        finally:
            cursor.close()
            conn.close()

def delete_records_in_existing_table_2(selected_table):
    st.write(f"### Delete Records from {selected_table}")

    conn = connect_db()
    cursor = conn.cursor()

    # Handle Orders table (simple PK)
    if selected_table == "Orders":
        st.info("Deleting an order will also delete ALL its OrderDetails.")

        df_orders = pd.read_sql("SELECT OrderID FROM northwind.Orders;", conn)

        selected_orders = st.multiselect(
            "Select OrderID(s) to delete",
            df_orders["OrderID"].tolist()
        )

        if st.button("⚠ Delete Selected Orders", type="primary"):
            try:
                for oid in selected_orders:

                    # 1️⃣ Delete child OrderDetails first
                    cursor.execute(
                        "DELETE FROM northwind.OrderDetails WHERE OrderID = %s;",
                        (oid,)
                    )

                    # 2️⃣ Now delete the parent order
                    cursor.execute(
                        "DELETE FROM northwind.Orders WHERE OrderID = %s;",
                        (oid,)
                    )

                conn.commit()
                st.success("✅ Selected orders deleted successfully (and related OrderDetails).")

            except Exception as e:
                conn.rollback()
                st.error(f"❌ Delete failed: {e}")

            finally:
                cursor.close()
                conn.close()

        return

    # Handle OrderDetails table (composite PK)
    if selected_table == "OrderDetails":
        st.info("Deleting OrderDetails affects ONLY the selected line items.")

        df_od = pd.read_sql(
            "SELECT OrderID, ProductID FROM northwind.OrderDetails;",
            conn
        )
        df_od["display"] = df_od["OrderID"].astype(str) + " | ProductID: " + df_od["ProductID"].astype(str)

        selected_lines = st.multiselect(
            "Select OrderDetail records to delete",
            df_od["display"].tolist()
        )

        if st.button("⚠ Delete Selected OrderDetails", type="primary"):
            try:
                for entry in selected_lines:
                    oid, pid = entry.split(" | ProductID: ")
                    cursor.execute(
                        "DELETE FROM northwind.OrderDetails WHERE OrderID = %s AND ProductID = %s;",
                        (oid, pid)
                    )

                conn.commit()
                st.success("✅ Selected OrderDetails line items deleted successfully.")

            except Exception as e:
                conn.rollback()
                st.error(f"❌ Delete failed: {e}")

            finally:
                cursor.close()
                conn.close()

##----------------------####----------------------####----------------------##
################# FOR Analytics Dashboard ################# 
##----------------------####----------------------####----------------------##

# ==========================================================
# 1. OVERVIEW KPI CARDS
# ==========================================================
def show_overview_kpis():

    conn = connect_db()
    df = pd.read_sql("""
        SELECT 
            SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) AS total_revenue,
            COUNT(DISTINCT o.OrderID) AS total_orders,
            COUNT(DISTINCT o.CustomerID) AS total_customers
        FROM Orders o
        JOIN OrderDetails od ON od.OrderID = o.OrderID;
    """, conn)
    conn.close()

    revenue = float(df["total_revenue"][0] or 0)
    orders = int(df["total_orders"][0] or 0)
    customers = int(df["total_customers"][0] or 0)

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Revenue", f"${revenue:,.2f}")
    col2.metric("Total Orders", orders)
    col3.metric("Unique Customers", customers)

# ==========================================================
# 2. MONTHLY SALES TREND
# ==========================================================
def show_monthly_sales():

    conn = connect_db()
    df = pd.read_sql("""
        SELECT 
            DATE_FORMAT(ShippedDate, '%Y-%m') AS month,
            SUM(UnitPrice * Quantity * (1 - Discount)) AS revenue
        FROM Invoices
        WHERE ShippedDate IS NOT NULL
        GROUP BY month
        ORDER BY month;
    """, conn)
    conn.close()

    if df.empty:
        st.info("No shipped orders available.")
        return

    chart = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X("month:T", title="Month"),
        y=alt.Y("revenue:Q", title="Revenue"),
        tooltip=["month", "revenue"]
    )

    st.altair_chart(chart, use_container_width=True)

# ==========================================================
# 3. TOP PRODUCTS BY REVENUE
# ==========================================================
def show_top_products():

    conn = connect_db()
    df = pd.read_sql("""
        SELECT ProductName, SUM(ExtendedPrice) AS revenue
        FROM Invoices
        GROUP BY ProductName
        ORDER BY revenue DESC
        LIMIT 10;
    """, conn)
    conn.close()

    if df.empty:
        st.info("No product revenue data available.")
        return

    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X("revenue:Q", title="Revenue"),
        y=alt.Y("ProductName:N", sort="-x", title="Product"),
        tooltip=["ProductName", "revenue"]
    )

    st.altair_chart(chart, use_container_width=True)

# ==========================================================
# 4. CATEGORY SALES
# ==========================================================
def show_category_sales():

    conn = connect_db()
    df = pd.read_sql("""
        SELECT CategoryName, SUM(ProductSales) AS total_sales
        FROM `Product Sales for 1997`
        GROUP BY CategoryName
        ORDER BY total_sales DESC;
    """, conn)
    conn.close()

    if df.empty:
        st.info("No category sales data available.")
        return

    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X("total_sales:Q", title="Sales"),
        y=alt.Y("CategoryName:N", sort="-x", title="Category"),
        tooltip=["CategoryName", "total_sales"]
    )

    st.altair_chart(chart, use_container_width=True)

# ==========================================================
# 5. CUSTOMER REVENUE
# ==========================================================
def show_customer_revenue():

    conn = connect_db()
    df = pd.read_sql("""
        SELECT CustomerName, SUM(ExtendedPrice) AS revenue
        FROM Invoices
        GROUP BY CustomerName
        ORDER BY revenue DESC
        LIMIT 15;
    """, conn)
    conn.close()

    if df.empty:
        st.info("No customer revenue data available.")
        return

    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X("revenue:Q", title="Revenue"),
        y=alt.Y("CustomerName:N", sort="-x", title="Customer"),
        tooltip=["CustomerName", "revenue"]
    )

    st.altair_chart(chart, use_container_width=True)

# ==========================================================
# 6. SHIPPER PERFORMANCE
# ==========================================================
def show_shipper_performance():

    conn = connect_db()
    df = pd.read_sql("""
        SELECT ShipperName, COUNT(DISTINCT OrderID) AS orders_shipped
        FROM Invoices
        GROUP BY ShipperName
        ORDER BY orders_shipped DESC;
    """, conn)
    conn.close()

    if df.empty:
        st.info("No shipper data available.")
        return

    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X("orders_shipped:Q", title="Orders Shipped"),
        y=alt.Y("ShipperName:N", sort="-x", title="Shipper"),
        tooltip=["ShipperName", "orders_shipped"]
    )

    st.altair_chart(chart, use_container_width=True)

# ==========================================================
# 7. EMPLOYEE SALES
# ==========================================================
def show_employee_sales():

    conn = connect_db()
    df = pd.read_sql("""
        SELECT Salesperson, SUM(ExtendedPrice) AS revenue
        FROM Invoices
        GROUP BY Salesperson
        ORDER BY revenue DESC;
    """, conn)
    conn.close()

    if df.empty:
        st.info("No employee sales data available.")
        return

    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X("revenue:Q", title="Revenue"),
        y=alt.Y("Salesperson:N", sort="-x", title="Employee"),
        tooltip=["Salesperson", "revenue"]
    )

    st.altair_chart(chart, use_container_width=True)
