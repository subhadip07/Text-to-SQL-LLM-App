import streamlit as st
from dotenv import load_dotenv
load_dotenv()

import os
import sqlite3

import google.generativeai as genai

## Configure API key
genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

## Function to Load Google Gemini Model and provide sql query as response
def get_gemin_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt, question])
    return response.text

## Function to retrieve query from sql database