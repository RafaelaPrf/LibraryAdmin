import streamlit as st

st.set_page_config(
    page_title="Library Admin",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)


st.title("""📚 Library Admin System""")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("📚 Total Books", "100")
with col2:
    st.metric("✍️ Authors", "10")
with col3:
    st.metric("📂 Genres", "29")

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="quick-card">
        <h3>📊 View Data</h3>
        <p>Browse books, authors, and genres</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Go to Data →", key="data_btn", use_container_width=True):
        st.switch_page("pages/01_reference_data.py")

with col2:
    st.markdown("""
    <div class="quick-card">
        <h3>📖 Book Details</h3>
        <p>Search and view book information</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Go to Details →", key="details_btn", use_container_width=True):
        st.switch_page("pages/02_book_details.py")

with col3:
    st.markdown("""
    <div class="quick-card">
        <h3>✏️ Create New</h3>
        <p>Add books or book details</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Go to Create →", key="create_btn", use_container_width=True):
        st.switch_page("pages/03_create_forms.py")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="quick-card">
        <h3>🔄 Update/Delete</h3>
        <p>Modify or remove existing books</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Go to Updates →", key="update_btn", use_container_width=True):
        st.switch_page("pages/04_update_delete.py")

with col2:
    st.markdown("""
    <div class="quick-card">
        <h3>🤖 AI Chat</h3>
        <p>Chat with the AI book assistant</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Go to Chat →", key="chat_btn", use_container_width=True):
        st.switch_page("pages/05_chatbot.py")

with col3:
    st.markdown("""
    <div class="quick-card">
        <h3>🔌 API Health</h3>
        <p>Check API connection status</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Go to Health →", key="health_btn", use_container_width=True):
        st.switch_page("pages/00_api_health.py")

st.markdown("---")
