import streamlit as st
from dotenv import load_dotenv
load_dotenv()

import os
import sqlite3

import google.generativeai as genai

## Configure API key
genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

## Function to Load Google Gemini Model and provide sql query as response
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-2.0-flash-lite')
    response = model.generate_content([prompt[0], question])
    return response.text

## Function to retrieve query from sql database
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()

    for i in rows:
        print(i)
    return rows


## Define Your Prompt
prompt=[
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, SECTION 
    \n\nFor example, 
    \nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ;
    
    \nExample 2 - Tell me all the students studying in Data Science class?, 
    the SQL command will be something like this SELECT * FROM STUDENT 
    where CLASS="Data Science";

    \nExample 3 - Tell me all the students in section A?,
    the SQL command will be something like this SELECT * FROM STUDENT
    where SECTION="A";

    also the sql code should not have ``` in beginning or end and sql word in output

    """
]

## Streamlit App
st.set_page_config(page_title = "I can Retrieve Any SQL query")

st.header("Gemini App To Retrieve SQL Data")

question = st.text_input("Input: ", key="input")

submit = st.button("Ask the question")

# if submit is clicked
if submit:
    response = get_gemini_response(question, prompt)
    print(response)
    response = read_sql_query(response, "student.db")
    st.subheader("The Response is")
    for row in response:
        print(row)
        st.header(row)
