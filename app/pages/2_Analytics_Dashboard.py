import streamlit as st
from interface import *

st.set_page_config(
                    page_title="Northwind Analytics Dashboard",
                    page_icon="📈",
                    layout="wide",
                    initial_sidebar_state="collapsed"
                )

# Main Function to Control Navigation
def main():
    st.title("Analytics Dashoboard")
    
if __name__ == "__main__":
    main()