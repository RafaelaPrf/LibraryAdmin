import streamlit as st
from utils.api_client import APIClient

st.title("Update/Delete")

update_tab, delete_book_tab, delete_detail_tab = st.tabs(
    ["Update Book", "Delete Book", "Delete Book Detail"]
)

with update_tab:
    with st.form("update_book"):
        book_id = st.number_input("Book ID", min_value=1)

        title = st.text_input("Title (optional)")
        upc = st.text_input("UPC (optional)")

        genre_id = st.number_input(
            "Genre ID (0 = unchanged)",
            min_value=0
        )

        author_id = st.number_input(
            "Author ID (0 = unchanged)",
            min_value=0
        )

        submitted = st.form_submit_button("Update Book")

        if submitted:

            payload = {}

            if title.strip():
                payload["title"] = title

            if upc.strip():
                payload["upc"] = upc

            if genre_id != 0:
                payload["genre_id"] = genre_id

            if author_id != 0:
                payload["author_id"] = author_id

            data, error = APIClient.put(
                f"/books/{book_id}",
                payload
            )

            st.success("Book updated!")
            st.rerun()

with delete_book_tab:
    book_id = st.number_input(
        "Book ID",
        min_value=1,
        key="delete_book"
    )

    confirm = st.checkbox(
        "I confirm I want to delete this book."
    )

    if st.button("Delete Book"):

        if not confirm:
            st.warning("Please confirm deletion.")
        else:
            success, message = APIClient.delete(
                f"/books/{book_id}"
            )

            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)


with delete_detail_tab:
    detail_id = st.number_input(
        "Book Detail ID",
        min_value=1,
        key="detail"
    )

    confirm = st.checkbox(
        "Delete this book detail?",
        key="confirm_detail"
    )

    if st.button("Delete Book Detail"):

        if confirm:
            success, message = APIClient.delete(
                f"/book-details/{detail_id}"
            )

            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)