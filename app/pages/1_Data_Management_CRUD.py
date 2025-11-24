import streamlit as st
from interface import *

st.set_page_config(
                    page_title="Northwind DBMS CRUD",
                    page_icon="🔁",
                    layout="wide",
                    initial_sidebar_state="collapsed"
                )

# #Main Function to Control Navigation
def main():
    st.title(":blue[Northwind DBMS CRUD Operations]")
    create_tabs_for_CRUD()
        

if __name__ == "__main__":
    main()