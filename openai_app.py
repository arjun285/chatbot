import streamlit as st
import openai
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import warnings

import os
from dotenv import load_dotenv
load_dotenv()

## Langsmith tracking
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Q&A ChatBot With Open AI"

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please respond to the user questions."),
        ("user", "Question: {question}")
    ]
)

def generate_response(question, api_key, engine, temperature, max_tokens):
    openai.api_key = api_key
    llm = ChatOpenAI(model=engine,temperature=temperature,max_tokens=max_tokens)
    output_parser = StrOutputParser()
    chain = prompt|llm|output_parser
    answer = chain.invoke({"question": question})
    return answer

## Title
st.title("Chatbot with OpenAI by Arjun")
st.sidebar.title("Settings")
#api_key = st.sidebar.text_input("Enter your OpenAI API key:", type="password")
api_key="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"
## Dropdown to select OpenAI models
engine = st.sidebar.selectbox("Select OpenAI model", ["gpt-4o", "gpt-4-turbo", "gpt-4"])

temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.75)
max_tokens = st.sidebar.slider("Maximum Tokens", min_value=50, max_value=1000, value=125)

## Main interface
st.write("What's on your mind?")
user_input = st.text_input("You:")

if user_input and api_key:
    response = generate_response(user_input, api_key, engine, temperature, max_tokens)
    st.write(response)
elif user_input:
    st.warning("Please enter the OpenAI API key in the sidebar.")
else:
    st.write("Please provide your query.")
