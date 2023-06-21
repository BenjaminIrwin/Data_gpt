# Chat with your data sources

This is a chat application that leverages the power of GPT-3.5-turbo to provide conversational responses with access to multiple data sources (SQL, Excel files and CSV files). SQL databases can be accessed via an ordinary connection, whilst Excel and CSV files are loaded into SQLite databases at runtime for the chatbot to query. This method allows us to leverage the power of GPT's text2SQL capabilities, maximising the accuracy of our results.

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
- List any SQL databases in the secrets.toml file, providing your database url.
- AND/OR List any local file directories in the secrets.toml file, providing the path to the directory. This directory should contain CSV and Excel files that you want the chatbot to access. Note that you should organise these files into relevant subfolders to improve the chatbot's ability to find the correct data. The chatbot will load each of these local file directories into their own SQLite database when the app starts up.
- For each database, provide a relevant example question which is linked to its data. This question MUST be uniquely associated with the data in its database. The example questions will be used to 'train' the chatbot and improve its ability to route queries to the correct database.


Example secrets.toml file (use this as a template):

```
OPENAI_API_KEY = 'sk-fawueblgfenkvasqogubhadewalfnwrl'
SQL_DATABASES = { 'company'= {'DB_URL' = 'jdbc:mysql://localhost:3306/example', 'EXAMPLE_QUESTION' = 'How many employees work in the UK?'} }
LOCAL_FILE_DATA = { 'disasters' = {'DIRECTORY' = 'local_file_data/disasters','EXAMPLE_QUESTION' = 'How many hurricanes were there in Louisiana?'}, 'movies'= {'DIRECTORY' = 'local_file_data/movies','EXAMPLE_QUESTION' = 'How many movies were released in 2019?'}, 'urban_living'= {'DIRECTORY' = 'local_file_data/urban_living','EXAMPLE_QUESTION' = 'How many people live in New York City?'} }
```

- This example will create a chatbot with access to FOUR databases. The four will be comprised of one existing MYSQL database ('company') and three more SQLite databases ('disasters', 'movies' and 'urban living'). Each of these SQLite databases will be created when the app starts up from the CSV and excel files provided in the ```DIRECTORY``` folders.
- To extend the example, the 'local_file_data/disasters' may contain three files: ```hurricanes.csv```, ```earthquakes.xls``` and ```volcanoes.csv```. At startup time an SQLite database will be created called disasters.db, with three tables: ```hurricanes```, ```earthquakes``` and ```volcanoes```.
- Note that you, while the example above has just one, you could also have multiple sql databases.


4. Run the application:

```
streamlit run app.py
```

## Usage

1. Access the application by navigating to `http://localhost:8501` in your web browser.

2. Enter your prompt in the input box and press Enter.

3. The chatbot will process your prompt and provide a response based on the available data sources.

4. The chat history will be displayed on the screen, showing both user and assistant messages.

