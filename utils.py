import os
import sqlite3

import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, inspect


def csv_to_sqlite(csv_file, conn):
    csv_data = pd.read_csv(csv_file)
    table_name = os.path.splitext(os.path.basename(csv_file))[0]
    csv_data.to_sql(table_name, conn, if_exists='replace')


def xls_to_sqlite(xls_file, conn):
    xls_data = pd.read_excel(xls_file)
    table_name = os.path.splitext(os.path.basename(xls_file))[0]
    xls_data.to_sql(table_name, conn, if_exists='replace')


def convert_files_to_sqlite(directory):
    # Get the name of the directory
    folder = os.path.basename(directory)
    output_file = f'{directory}/{folder}.db'
    conn = sqlite3.connect(output_file)
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if file.endswith('.csv'):
            csv_to_sqlite(file_path, conn)
        elif file.endswith('.xls') or file.endswith('.xlsx'):
            xls_to_sqlite(file_path, conn)

    conn.commit()
    conn.close()

def get_table_names(db_path):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    res = cur.execute("SELECT name FROM sqlite_master where type='table'")
    return str(res.fetchall())


def clean_string(string):
    new_string = string.replace("(", "")
    new_string = new_string.replace(",)", "")
    return new_string

def get_db_info():
    SQL_DATABASES = st.secrets["SQL_DATABASES"]
    LOCAL_FILE_DATA = st.secrets["LOCAL_FILE_DATA"]
    SQL_DATABASES_KEYS = list(SQL_DATABASES.keys())
    LOCAL_FILE_DATA_KEYS = list(LOCAL_FILE_DATA.keys())

    examples = ""
    schemas = ''
    # iterate through SQL_DATABASES
    for key in SQL_DATABASES_KEYS:
        examples += f"User: {SQL_DATABASES[key]['EXAMPLE_QUESTION']}\n"
        examples += f"Answer: {key}\n"
        url = SQL_DATABASES[key]["DB_URL"]
        table_names = get_table_name_string(url)
        schemas += f"{key}: {table_names}\n"
    # iterate through LOCAL_FILE_DATA
    for key in LOCAL_FILE_DATA_KEYS:
        examples += f"User: {LOCAL_FILE_DATA[key]['EXAMPLE_QUESTION']}\n"
        examples += f"Answer: {key}\n"
        directory = LOCAL_FILE_DATA[key]["DIRECTORY"]
        db_filename = os.path.basename(directory) + '.db'
        url = f'sqlite:///{directory}/{db_filename}'
        table_names = get_table_name_string(url)
        schemas += f"{key}: {table_names}\n"

    return examples, schemas


def get_table_name_string(url):
    engine = create_engine(url)
    insp = inspect(engine)
    table_names = ', '.join(insp.get_table_names())
    table_names = clean_string(table_names)
    return table_names