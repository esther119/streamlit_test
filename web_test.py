"""Python file to serve as the frontend"""
import streamlit as st
from streamlit_chat import message
import pinecone
import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone

from langchain.chains import ConversationChain
from langchain.llms import OpenAI

embeddings = OpenAIEmbeddings(disallowed_special=(), openai_api_key=st.secrets['openai_api_key'])



pinecone.init(
    api_key=st.secrets['pinecone_api_key'],
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
    input_text = st.text_input("You: ", "Write a blog about first principles", key="input")
    return input_text

user_input = get_text()

def similarity_search(user_input):
    docs = chain.similarity_search(user_input)
    return docs[0].page_content



def AI_response_messages(user_input, store, openai_api_key):
    template ='''
    Use the following pieces of context from waitbutwhy to answer the question at the end. 
    If you don't know the answer, just clarify that you are not sure, but this might be how Tim Urban thinks.
    '''
    engineered_user_input = f'{user_input} within 300 words like waitbutwhy using "you" in a casual language'
    from langchain.schema import (
        AIMessage,
        HumanMessage,
        SystemMessage
    )
    from langchain.chat_models import ChatOpenAI
    chat = ChatOpenAI(model_name='gpt-3.5-turbo-16k-0613', openai_api_key=openai_api_key)   

    print("engineered_user_input", engineered_user_input)
    messages = [
        SystemMessage(content=template+store),
        HumanMessage(content=engineered_user_input)
    ]
    response=chat(messages)

    return response

if user_input:
    if user_input:
        store = similarity_search(user_input)
        response = AI_response_messages(user_input, store, st.secrets['openai_api_key'])
    st.write("context search: ", store)
    st.session_state.past.append(user_input)
    st.session_state.generated.append(response.content)

if st.session_state["generated"]:

    for i in range(len(st.session_state["generated"]) - 1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
