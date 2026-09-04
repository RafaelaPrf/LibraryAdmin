import streamlit as st

from utils.api_client import APIClient
from utils.settings import get_api_base_url, set_api_base_url

st.title("API Health")

url = st.text_input("Enter your API URL",
                    value=get_api_base_url())

if st.button("Save URL"):
    set_api_base_url(str(url))

if st.button("Test connection"):
    result = APIClient.test_connection()

    if result.success:
        st.success(result.message)
    else:
        st.error(result.message)
