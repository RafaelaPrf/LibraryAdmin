import streamlit as st
from api.api_client import APIClient
import pandas as pd

st.title("Book Details")

book_id = st.number_input("book ID:", step=1, value=1)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Book")
    data, error = APIClient.get("/books/{}".format(book_id))
    if error:
        st.error("Book not found")
    else:
        if isinstance(data, dict):
            df = pd.DataFrame([data])
        else:
            df = pd.DataFrame(data)
        st.table(df)

with col2:
    st.subheader("Book Details")
    data, error = APIClient.get("/book-details/{}".format(book_id))
    if error:
        st.error(error)
    else:
        if isinstance(data, dict):
            df = pd.DataFrame([data])
        else:
            df = pd.DataFrame(data)
        st.table(df)

