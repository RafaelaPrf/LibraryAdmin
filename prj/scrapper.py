"""
Books to Scrape - Web Scraper
=====================================
Site  : https://books.toscrape.com/
Output: books.csv

How it works:
  1. Loop through the first 5 listing pages (20 books each = 100 books total).
  2. For each book, follow the link to its detail page and scrape the full info.
  3. Save all collected books to a CSV file.
"""
import csv
import re
import time
import requests
from bs4 import BeautifulSoup

# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------

# Every book URL on this site starts with this prefix
BASE_URL      = "https://books.toscrape.com/catalogue/"

OUTPUT_CSV    = "books.csv"

REQUEST_DELAY = 0.1

# Scraping helpers

def fetch_page(url):
    """Download `url` and return a parsed BeautifulSoup object."""

    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def scrape_book(url):
    """
    Visit one book detail page and return a dict with all the info we want.
    """

    soup = fetch_page(url)

    title = soup.select_one("div.product_main h1").text.strip()

    breadcrumbs = soup.select("ul.breadcrumb li")
    genre = breadcrumbs[-2].text.strip()

    rating = soup.select_one("p.star-rating")["class"][1]

    table = {}
    for row in soup.select("table.table-striped tr"):
        label = row.select_one("th").text.strip()
        value = row.select_one("td").text.strip()
        table[label] = value

    upc = table.get("UPC", "")


    price = table.get("Price (incl. tax)", "").replace("£", "").replace("Â", "").strip()


    availability_raw = table.get("Availability", "")

    if "Out of stock" in availability_raw:
        availability = "0"
    else:
        match        = re.search(r"\((\d+) available\)", availability_raw)
        availability = match.group(1) if match else availability_raw.strip()

    # Return all scraped fields as a dictionary
    return {
        "title":        title,
        "genre":        genre,
        "rating":       rating,
        "upc":          upc,
        "price":        price,
        "availability": availability,
    }


def get_book_urls_from_page(page_number):
    """Return the list of book detail-page URLs found on a given listing page."""


    url  = f"{BASE_URL}page-{page_number}.html"
    soup = fetch_page(url)

    urls = []
    for article in soup.select("article.product_pod"):
        relative = article.select_one("h3 > a")["href"]
        urls.append(BASE_URL + relative.replace("../../", ""))

    return urls


def save_to_csv(books, filepath):
    fieldnames = ["title", "genre", "rating", "upc", "price", "availability"]

    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(books)

    print(f"\nSaved {len(books)} books to '{filepath}'")


def main():
    books = []

    for page_num in range(1, 6):
        print(f"Scraping listing page {page_num}/5 ...")

        book_urls = get_book_urls_from_page(page_num)

        for url in book_urls:
            book = scrape_book(url)
            books.append(book)
            print(f"  Scraped: {book['title'][:60]}")

            time.sleep(REQUEST_DELAY)

    print(f"\nDone! {len(books)} books collected.")

    save_to_csv(books, OUTPUT_CSV)


if __name__ == "__main__":
    main()
