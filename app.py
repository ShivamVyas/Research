# UI Library
import streamlit as st

# URL Image Extractions
import urllib.request
from urllib.request import urlopen
from PIL import Image

# Doc Readers
import docx2txt
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter

# Environment Variable 
import os
from dotenv import load_dotenv

# Open AI And Facebook's Similarity Search Libraries
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import FAISS
from langchain.callbacks import get_openai_callback
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains.question_answering import load_qa_chain 

from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

# Adding Background Image and Removing Watermark
def html_configurations():
    st.markdown(
          f"""
          <style>
          .stApp {{
              background-image: url("https://images.unsplash.com/photo-1518655048521-f130df041f66?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2670&q=80");
              background-attachment: fixed;
              background-size: cover;
          }}
         </style>
         """,
         unsafe_allow_html=True
      )
    hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
    
def sidebar_img():
    st.markdown("""
    <style>
        [data-testid=stSidebar] {
            background-image: url("https://img.freepik.com/free-vector/simple-blue-gradient-background-vector-business_53876-166894.jpg?w=826&t=st=1702933247~exp=1702933847~hmac=9d9051d4fa624db1dcbd97a9d11693293a7f44706c31ace16bdb0fd8eeffae5b");
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-size: contain;
        }
    </style>
    """, unsafe_allow_html=True)
    
def main(): 
    # URL Title and Logo
    urllib.request.urlretrieve('https://ontariotechu.ca/favicon.ico', "img.png")
    img = Image.open("img.png")
    st.set_page_config(page_title="LLM Model", page_icon=img)
    # Adding Background Image and Removing Watermark
    html_configurations()     
    sidebar_img()
    # Title
    st.markdown("<h2>\n👨🏽‍💻 Testing Engineering Model 👩🏽‍💻</h2>", unsafe_allow_html = True)
    st.sidebar.markdown("## API Configuration 🔧")
    
    OPENAI_API_KEY = st.sidebar.text_input(":orange[**Add your OpenAI API key and press Enter**]", type="password")

    if OPENAI_API_KEY:
    # Initializing variables in the first instance to save in memory and prevent reset
      if "history" not in st.session_state:
          st.balloons()
          memory = ConversationBufferMemory(memory_key='history', return_messages=True)
          model_name = "gpt-3.5-turbo"
          llm = ChatOpenAI(model_name=model_name, openai_api_key=OPENAI_API_KEY)
          conversation_chain = ConversationChain(
              llm=llm,
              memory=memory
          )
          st.session_state.conversation = conversation_chain
          st.session_state.history = memory
          st.session_state.openai_cost = [] 

      user_question = st.text_input(":orange[**How can I help you?**]", placeholder="Enter your question here")  

      if user_question:
          # [Rest of the code...]

          with st.spinner(text="**Operation in progress ⏳**"):
              with get_openai_callback() as cost:
                  response = st.session_state.conversation({'input': user_question})
              st.session_state.openai_cost.append(cost.total_cost)

          for index, message in enumerate(response['history']):
            if index%2==0:
              st.write("<h6 style='color:#d95a00;'>"+message.content+"</h6>", unsafe_allow_html = True)
              st.write("**Cost of Operation: :green[$"+str('%.6f'%(st.session_state.openai_cost[int(index/2)]))+"]**")
            else: 
              st.write("<h6>"+message.content+"</h6>", unsafe_allow_html = True)
      


if __name__ == '__main__':
    main()