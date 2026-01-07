import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

@st.cache_resource
def connect_sheet():
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    return gspread.authorize(creds)
