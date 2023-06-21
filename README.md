# Chat with your data sources

This is a chat application that leverages the power of GPT-3.5-turbo to provide conversational responses with access to multiple data sources (SQL, Excel files and CSV files).

## Features

- Chat interface for interacting with the chatbot powered by GPT-3.5-turbo.
- 'Safe' mode to prevent the chatbot from accessing the databases.
- Semantic search functionality to provide informative snippets from the databases.
- Intent classification to route user queries to the appropriate database.
- OpenAI API key integration for authentication.

## Installation

1. Install the required dependencies:

```
pip install -r requirements.txt
```

2. Set up your credentials and data sources:

- Sign up on the OpenAI website and obtain an API key.
- Create a new file called "secrets.toml" in the .streamlit folder.
- Set your OpenAI API key and in the secrets.toml file.
- List your SQL databases in the secrets.toml file, providing your database url.
- List your local file directories in the secrets.toml file, providing the path to the directory. This directory should contain CSV and Excel files that you want the chatbot to access. Note that you can organise these files in subfolders to improve the chatbot's ability to find the correct data.
- For each database, provide a relevant example question which will be used to improve the chatbot's ability to route queries to the correct database.


Example secrets.toml file:

```
OPENAI_API_KEY = 'sk-fawueblgfenkvasqogubhadewalfnwrl'
SQL_DATABASES = { 'company'= {'DB_URL' = 'jdbc:mysql://localhost:3306/example', 'EXAMPLE_QUESTION' = 'How many employees work in the UK?'} }
LOCAL_FILE_DATA = { 'disasters_db' = {'DIRECTORY' = 'local_file_data/disasters','EXAMPLE_QUESTION' = 'How many hurricanes were there in Louisiana?'}, 'movies'= {'DIRECTORY' = 'local_file_data/movies','EXAMPLE_QUESTION' = 'How many movies were released in 2019?'}, 'urban_living'= {'DIRECTORY' = 'local_file_data/urban_living','EXAMPLE_QUESTION' = 'How many people live in New York City?'} }
```

4. Run the application:

```
streamlit run app.py
```

## Usage

1. Access the application by navigating to `http://localhost:8501` in your web browser.

2. Enter your prompt in the input box and press Enter.

3. The chatbot will process your prompt and provide a response based on the available data sources.

4. The chat history will be displayed on the screen, showing both user and assistant messages.

