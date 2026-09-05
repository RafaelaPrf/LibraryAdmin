
import streamlit as st

from api.api_client import APIClient

st.title("Data")

refresh = st.button("🔄 Refresh")
if refresh:
    st.rerun()

tab1, tab2, tab3 = st.tabs(["Genres", "Authors", "Tags"])

with tab1:
    st.header("Genres")
    data, error = APIClient.get("/genres")
    if error:
        st.error(error)
    else:
        st.dataframe(data, width='stretch')


with tab2:
    st.header("Authors")
    data, error = APIClient.get("/authors")
    if error:
        st.error(error)
    else:
        st.dataframe(data, width='stretch')

with tab3:
    st.header("Tags")
    data, error = APIClient.get("/tags")
    if error:
        st.error(error)
    else:
        st.dataframe(data, width='stretch')

