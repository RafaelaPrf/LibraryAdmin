
import streamlit as st

from api.api_client import APIClient

st.title("Create New")

book_tab, detail_tab = st.tabs(
    ["Create Book", "Create Book Detail"]
)

with book_tab:
    with st.form("create_book"):
        title = st.text_input("Title")

        upc = st.text_input("UPC")

        genre_id = st.number_input(
            "Genre ID",
            min_value=1,
            step=1
        )

        author_id = st.number_input(
            "Author ID",
            min_value=1,
            step=1
        )

        submitted = st.form_submit_button("Create Book")

        if submitted:

            if not title.strip():
                st.error("Title is required.")

            elif not upc.strip():
                st.error("UPC is required.")

            else:
                payload = {
                    "title": title,
                    "upc": upc,
                    "genre_id": genre_id,
                    "author_id": author_id
                }
                data, error = APIClient.post("/books", payload)

                if error:
                    st.error(error)
                else:
                    st.success("Book created successfully!")
                    st.json(data)

with detail_tab:
    with st.form("create_book_detail"):
        book_id = st.number_input(
            "Book ID",
            min_value=1,
            step=1
        )

        rating = st.number_input(
            "Rating",
            min_value=1,
            max_value=5,
            step=1
        )

        price = st.number_input(
            "Price",
            min_value=0.0
        )

        availability = st.number_input(
            "Availability",
            min_value=0,
            step=1
        )

        submitted = st.form_submit_button("Create Book Detail")

        if submitted:

            payload = {
                "book_id": book_id,
                "rating": rating,
                "price": price,
                "availability": availability
            }

            data, error = APIClient.post(
                "/book-details",
                payload
            )

            if error:
                st.error(error)
            else:
                st.success("Book details created.")
                st.json(data)