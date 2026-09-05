# Library Management System with AI Agent

A Python-based book management application that combines a **FastAPI backend**, **Streamlit web interface**, **SQL database**, **web scraping**, and a local **AI agent** powered by Ollama.

The application allows users to browse and manage books and related reference data, while the AI chatbot can interact with the database through dedicated tools.

## Features

* Scrape book data from [Books to Scrape](https://books.toscrape.com/)
* Store books, genres, authors, tags, and book details in a relational database
* REST API built with FastAPI for CRUD operations
* Streamlit multipage web interface
* AI chatbot using a local `qwen3:4b` model through Ollama
* MCP tools that allow the AI agent to query and interact with the application
* Create, update, and delete books and related data
* Browse reference data such as genres, authors, and tags
* API health check page


## Requirements

* Python 3.14
* Ollama
* `qwen3:4b` model
* PostgreSQL

Install the Python dependencies with:

```bash
pip install -r requirements.txt
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/RafaelaPrf/LibraryAdmin.git
cd prj
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Seed the database

First, generate the book dataset using the scraper.

From the project root:

```bash
cd database
python scrapper.py
```

This generates `books.csv`.

Alternatively, the repository already contains a `books.csv` file that can be used directly.

### 4. Create and populate the database

While inside the `database` directory:

```bash
python create_tables.py
```

This creates the database tables and loads the initial data, including:

* Books
* Genres
* Authors
* Tags
* Book details

> **Note:** The initialization script drops existing tables before recreating and populating them.

### 5. Start the FastAPI server

From the project root:

```bash
uvicorn database.database:app --reload --port 8000
```

* Interactive API documentation: http://localhost:8000/docs

### 6. Start the AI tool server

Open a new terminal and run:

```bash
uvicorn api.api_AI:app --reload --port 8090
```

This server exposes the MCP tools used by the AI agent.

### 7. Start Ollama

Make sure Ollama is running and that the required model is installed:

```bash
ollama pull qwen3:4b
```

The agent is configured to use `qwen3:4b` through Ollama.

### 8. Launch the Streamlit application

Open a third terminal from the project root:

```bash
streamlit run main.py
```

The Streamlit application will be available at:

http://localhost:8501

## Application Pages

### API Health

Checks whether the Streamlit application can successfully communicate with the backend API.

### Reference Data

Displays reference data used by the application, including:

* Genres
* Authors
* Tags

### Book Details

Allows users to retrieve a book and its associated details using its ID.

### Create

Provides forms for adding new books and related details to the database.

### Update / Delete

Allows existing books and related data to be modified or removed.

### Chatbot

Provides a conversational interface to the AI agent.

The agent uses MCP tools exposed by the AI tool server to retrieve and work with book data.


## Technologies Used

* **Python** – Application development
* **FastAPI** – REST API and backend services
* **Streamlit** – Web interface
* **SQLAlchemy** – Database interaction
* **Ollama** – Local LLM execution
* **Qwen3:4B** – Local language model
* **MCP** – AI tool integration
* **HTTPX** – HTTP communication
* **Pandas** – Data processing
* **Web scraping** – Data collection from Books to Scrape
* **Uvicorn** – ASGI server
