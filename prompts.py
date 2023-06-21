from utils import get_db_info

print('Preparing classification prompt...')
examples, schemas = get_db_info()

def get_classification_prompt(user_question):
    return f'''
You are a data expert that finds the best SQL database to answer user questions.
Your task is as follows: you will analyze a list of database schemas and find 
the best one to answer the user's question. You will then return the name of the database. 
The databases and schemas are as follows:\n
{schemas}
Here are some example questions and answers:\n
{examples}
Given these examples, provide an answer to the following user input:

User: {user_question}
Answer:
    '''