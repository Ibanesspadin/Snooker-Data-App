import streamlit as st
from google.oauth2.service_account import Credentials
import gspread

scopes = ["https://www.googleapis.com/auth/spreadsheets"]

# Pega o JSON do Secret do Streamlit
service_account_info = st.secrets["gcp_service_account"]

# Cria as credenciais
creds = Credentials.from_service_account_info(service_account_info, scopes=scopes)

# Conecta com o Google Sheets
gc = gspread.authorize(creds)

def connect_sheets():
    return gc
