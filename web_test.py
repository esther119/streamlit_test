"""Python file to serve as the frontend"""
import streamlit as st
from streamlit_chat import message
import pinecone
import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone

from langchain.chains import ConversationChain
from langchain.llms import OpenAI
import pinecone_api

embeddings = OpenAIEmbeddings()


pinecone_api_key = pinecone_api.pinecone_api_key


pinecone.init(
    api_key=pinecone_api_key,  
    environment='asia-southeast1-gcp-free'   
)
index_name =  'tim-urban-test'



def load_chain():
    """Logic for loading the chain you want to use should go here."""
    docsearch = Pinecone.from_existing_index(index_name, embeddings)
    return docsearch

chain = load_chain()

# From here down is all the StreamLit UI.
st.set_page_config(page_title="LangChain Demo", page_icon=":robot:")
st.header("LangChain Demo")

if "generated" not in st.session_state:
    st.session_state["generated"] = []

if "past" not in st.session_state:
    st.session_state["past"] = []


def get_text():
    input_text = st.text_input("You: ", "Hello, how are you?", key="input")
    return input_text


user_input = get_text()

if user_input:
    if user_input:
        docs = chain.similarity_search(user_input)
        output = docs[0].page_content

    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

if st.session_state["generated"]:

    for i in range(len(st.session_state["generated"]) - 1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
