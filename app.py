# UI Library
from langchain.schema import AIMessage, HumanMessage
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

# Removing Watermark
def footer():
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

def container():
    st.markdown("""
    <style>
        [data-testid=stAppViewContainer] {
            background-color: #e5e7e9;
            background-image: url("https://images.unsplash.com/photo-1559239115-ce3eb7cb87ea?q=80&w=3788&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
            background-position: right -200px top 40px;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-size: cover;
        }
    </style>            
    """, unsafe_allow_html=True)


# <style>
#     #MainMenu, header, footer {visibility: hidden;}

#     /* This code gets the first element on the sidebar,
#     and overrides its default styling */
#     section[data-testid="stHeader"] div:first-child {
#         top: 0;
#         height: 100vh;
#     }
# </style>

def header():
    st.markdown("""
    <style>
        [data-testid=stHeader] {
            background-color: #e5e7e9;
        }
    </style>            
    """, unsafe_allow_html=True)

def remove_alert():
    st.markdown("""
    <style>
        .stAlert {display:none;}
    </style>
    """, unsafe_allow_html=True)

def submit():
    st.session_state.my_text = st.session_state.widget
    st.session_state.widget = ""

@st.cache(show_spinner=False)
def parse_file(file_list):
    text=""
    if file_list: 
        for file in file_list:
            text += file.name
            if ".pdf" in file.name:
                pdf_reader = PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
            elif ".docx" in file.name:
                text += docx2txt.process(file)
        st.session_state.history.chat_memory.messages.append(HumanMessage(content=text, additional_kwargs={}))
        st.session_state.history.chat_memory.messages.append(AIMessage(content='', additional_kwargs={}))

def main():
    # URL Title and Logo
    urllib.request.urlretrieve('https://ontariotechu.ca/favicon.ico', "img.png")
    img = Image.open("img.png")
    st.set_page_config(page_title="LLM Model", page_icon=img, layout="centered")
    
    # Adding CSS
    container()
    header()
    footer()     
    sidebar_img()
    
    # Title
    st.markdown("<h2>&emsp;&emsp;&emsp;👨🏽‍💻 Test Engineering Model 👩🏽‍💻</h2>", unsafe_allow_html = True)
    st.sidebar.markdown("## API Configuration 🔧")
    
    OPENAI_API_KEY = st.sidebar.text_input(":orange[**Add your OpenAI key and Press Enter**]", type="password")

    st.warning('Please Enter your Open AI Key to start', icon="⚠️")
    
    if OPENAI_API_KEY:
        st.toast('Thanks', icon='🥳')
        remove_alert()
        
        if st.sidebar.button("Clear Chat History"):
            if "history" in st.session_state:
                st.session_state.clear()
        
        # Initializing variables in the first instance to save in memory and prevent reset
        if "history" not in st.session_state:
            st.snow()
            memory = ConversationBufferMemory(memory_key='history', return_messages=True)
            model_name = "gpt-3.5-turbo-1106"
            llm = ChatOpenAI(model_name=model_name, openai_api_key=OPENAI_API_KEY)
            conversation_chain = ConversationChain(
                llm=llm,
                memory=memory
            )
            st.session_state.conversation = conversation_chain
            st.session_state.history = memory
            st.session_state.openai_cost = []
             
        
        file_list = st.file_uploader(":orange[**Please upload your PDF or DOCX files here:**]", type=["pdf","docx"], accept_multiple_files=True) 
        # Extract the text from each PDF
        parse_file(file_list)
            
        if file_list is not None:                  

            st.text_input(":orange[**How can I help you?**]", placeholder="Enter your question here", key='widget', on_change=submit)  

            user_question = st.session_state.get('my_text', '')
            
            
            if user_question!="":
                st.balloons()
                # if text!="":
                #     user_question+=text
                
                with st.spinner(text="**Operation in progress ⏳**"):
                    with get_openai_callback() as cost:
                        response = st.session_state.conversation({'input': user_question})
                    st.session_state.openai_cost.append(cost.total_cost)
                output = response['history'][-1].content
                st.write("**Cost of Operation: :green[$"+str('%.6f'%(0.008*(len(output)/3)/1000))+"]**")
                st.write("<h6 style='color:#d95a00;'>"+"Question: </h6>"+"<h6>"+response['history'][-2].content+"</h6>", unsafe_allow_html = True)
                st.write("<h6 style='color:#d95a00;'>"+"Response: </h6>"+"<h6>"+output+"</h6>", unsafe_allow_html = True) 
                
                #Not working for gpt-3.5-turbo-1106 and gpt-4-1106-preview
                #st.write("**Cost of Operation: :green[$"+str('%.6f'%(st.session_state.openai_cost[-1]))+"]**")
                user_question=""
                
            #debugging    
            #print(st.session_state.history.chat_memory.messages)    


if __name__ == '__main__':
    main()