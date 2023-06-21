import os

import openai
import streamlit as st
from langchain import SQLDatabase, SQLDatabaseChain, OpenAI
from utils import convert_files_to_sqlite

SQL_DATABASES = st.secrets["SQL_DATABASES"]
LOCAL_FILE_DATA = st.secrets["LOCAL_FILE_DATA"]

print('Converting local files to SQLite databases...')
# Create SQLite databases from CSVs and Excel files
for key in LOCAL_FILE_DATA:
    dir = LOCAL_FILE_DATA[key]["DIRECTORY"]
    convert_files_to_sqlite(dir)

from prompts import get_classification_prompt
from render import user_msg_container_html_template, bot_msg_container_html_template

print('Setting up OpenAI API...')
# Set OpenAI API key
key_ = st.secrets["OPENAI_API_KEY"]
openai.api_key = key_
llm = OpenAI(temperature=0, verbose=True, openai_api_key=key_)
st.header("Chat with your databases")

# Initialize session state for chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Function to generate response
def generate_response():
    # Append user's query to history
    st.session_state.history.append({
        "message": st.session_state.prompt,
        "is_user": True
    })

    print('Prompt: ' + st.session_state.prompt)

    prompt = get_classification_prompt(st.session_state.prompt)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=20
    )

    chosen_db = response['choices'][0]['message']['content'].replace('Answer: ', '')

    print('Searching for answer in: ' + chosen_db)
    # If db a key in SQL_DATABASES
    if chosen_db in SQL_DATABASES:
        db_route = SQL_DATABASES[chosen_db]["DB_URL"]
    else:
        directory = LOCAL_FILE_DATA[chosen_db]["DIRECTORY"]
        folder = os.path.basename(directory)
        db_route = f'sqlite:///{directory}/{folder}.db'

    db = SQLDatabase.from_uri(db_route)
    if llm is None:
        print('No LLM')
    db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True, return_direct=True)

    data_response = db_chain.run(str(st.session_state.prompt))

    # Extract the assistant's message from the response
    assistant_message = data_response
    
    # Append assistant's message to history
    st.session_state.history.append({
        "message": assistant_message,
        "is_user": False
    })


# Take user input
st.text_input("Enter your prompt:",
              key="prompt",
              placeholder="e.g. 'How can I diversify my portfolio?'",
              on_change=generate_response
              )

# Display chat history
for message in st.session_state.history:
    if message["is_user"]:
        st.write(user_msg_container_html_template.replace("$MSG", message["message"]), unsafe_allow_html=True)
    else:
        st.write(bot_msg_container_html_template.replace("$MSG", message["message"]), unsafe_allow_html=True)
