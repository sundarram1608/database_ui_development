import streamlit as st
from helpers import *


def create_tabs_for_CRUD():
    # #Create tabs for CRUD operations
    tab1, tab2, tab3, tab4 = st.tabs(["Create", "Read", "Update", "Delete"])

    with tab1:
        st.subheader(":green[Create New Records in a Table]")
        st.divider()
        
        tables_list = get_tables()
        selected_table = st.selectbox(":blue[Select Table to Create New Record]", tables_list)
        # st.success(f"You have selected {selected_table}")
        create_new_records(selected_table)

                            
    with tab2:
        st.subheader(":green[View tables with certain predefined individual independent filters]")
        st.warning("For detailed analytics, pls visit the Analytics Dashboard page")
        st.divider()
        
        tables_list = get_tables()
        selected_table_read = st.selectbox(":blue[Select Table to view]", tables_list)
        # st.success(f"You have selected {selected_table}")
        create_query_and_display_table(selected_table_read)

    
    with tab3:
        st.subheader(":green[Update existing records in the tables]")
        st.warning("This tab is to update existing records. \n For any new records, please use the Create tab.")
        st.divider()
        
        tables_list = get_tables()
        selected_table_update = st.selectbox(":blue[Select Table to update records]", tables_list)
        table_column_details_update = fetch_table_column_details(selected_table_update)
        # st.success(f"You have selected {selected_table}")
        update_records_in_existing_table(selected_table_update,table_column_details_update)   
        
    with tab4:
        st.subheader(":green[Delete existing records in the tables]")
        st.warning("""This tab allows deleting records ONLY from Orders and OrderDetails tables. This action is irreversible.Records from other tables cannot be deleted as per the company policies""")
        st.divider()

        allowed_tables = ["Orders", "OrderDetails"]
        selected_table_delete = st.selectbox(":blue[Select Table to delete records]", allowed_tables)
        delete_records_in_existing_table_2(selected_table_delete)             
    
    # with tab4:
    #     st.subheader(":green[Delete existing records in the tables]")
    #     st.warning("This tab is to delete existing records. \n Please proceed with caution as this action is irreversible.")
    #     st.divider()
        
    #     tables_list = get_tables()
    #     selected_table_delete = st.selectbox(":blue[Select Table to delete records]", tables_list)
    #     table_column_details_delete = fetch_table_column_details(selected_table_delete)

    #     # # st.success(f"You have selected {selected_table}")
    #     delete_records_in_existing_table(selected_table_delete,table_column_details_delete)   
        
def create_tabs_for_analytics():
    # st.info("Analytics Dashboard under construction. Coming soon!")

    # Create main tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
                                                            "Overview",
                                                            "Sales Trends",
                                                            "Products",
                                                            "Categories",
                                                            "Customers",
                                                            "Shippers",
                                                            "Employees"
                                                        ])

    # ---------------------- TAB 1: OVERVIEW ----------------------
    with tab1:
        st.subheader("Business Overview")

        with st.expander("Overview Metrics"):
            show_overview_kpis()

        with st.expander("Revenue Summary"):
            show_monthly_sales()

    # ------------------- TAB 2: SALES TRENDS ---------------------
    with tab2:
        st.subheader("Sales Trends")

        with st.expander("Monthly Sales Trend"):
            show_monthly_sales()

    # ------------------- TAB 3: PRODUCTS -------------------------
    with tab3:
        st.subheader("Product Analytics")

        with st.expander("Top Products by Revenue"):
            show_top_products()

    # ------------------- TAB 4: CATEGORIES -----------------------
    with tab4:
        st.subheader("Category Analytics")

        with st.expander("Category Sales Performance"):
            show_category_sales()

    # ------------------- TAB 5: CUSTOMERS ------------------------
    with tab5:
        st.subheader("Customer Analytics")

        with st.expander("Customer Revenue Impact"):
            show_customer_revenue()

    # ------------------- TAB 6: SHIPPERS -------------------------
    with tab6:
        st.subheader("Shipper Performance")

        with st.expander("Orders by Shipper"):
            show_shipper_performance()

    # ------------------- TAB 7: EMPLOYEES ------------------------
    with tab7:
        st.subheader("Employee Sales Analytics")

        with st.expander("Sales by Employee"):
            show_employee_sales()
