import streamlit as st
from llama_index.agent import OpenAIAssistantAgent
import openai
import os
import asyncio
import datetime
import tempfile
from openai import OpenAI
import fitz  # PyMuPDF
import tempfile

#This is the usual openai new assistant but here we will be using the llama index agent which will build the assistant of openai directly 
#You can see the new assistant created in your openAI background after running this code
# api_key = "API KEY"
#os.environ['OPENAI_API_KEY'] = api_key
# Initialize the OpenAI Assistant Agent
# client = OpenAI()

# CSS Styling functions
def apply_global_styles():
    """Apply global CSS styles for the Streamlit app."""
    global_styles = """
        <style>
            footer {visibility: hidden;}
            .stAlert {display: none;}
            [data-testid="stHeader"] {background-color: #e5e7e9;}
        </style>
    """
    st.markdown(global_styles, unsafe_allow_html=True)

def style_sidebar():
    """Apply CSS styles to the sidebar."""
    sidebar_styles = """
        <style>
            [data-testid="stSidebar"] {
                background-image: url("https://img.freepik.com/free-vector/simple-blue-gradient-background-vector-business_53876-166894.jpg?w=826");
                background-repeat: no-repeat;
                background-attachment: fixed;
                background-size: cover;
            }
        </style>
    """
    st.markdown(sidebar_styles, unsafe_allow_html=True)

def style_container():
    """Apply CSS styles to the main container."""
    container_styles = """
        <style>
            [data-testid="stAppViewContainer"] {
                background-color: #e5e7e9;
                background-image: url("https://images.unsplash.com/photo-1559239115-ce3eb7cb87ea?q=80&w=3788&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
                background-position: right -200px top 40px;
                background-repeat: no-repeat;
                background-attachment: fixed;
                background-size: cover;
            }
        </style>
    """
    st.markdown(container_styles, unsafe_allow_html=True)


# Here there is no need to add the memory buffer part from Langchain because the new assistant has chat history so it will answer accordingly while in the same session
# Function to initialize the OpenAI Assistant Agent
def init_agent(api_key, uploaded_file_path=None):
    os.environ['OPENAI_API_KEY'] = api_key
    files = [uploaded_file_path] if uploaded_file_path else []

    return OpenAIAssistantAgent.from_new(
        name="Test Engineer Assistant",
instructions = """
You are the Code Master: An Interactive Guide for Test Engineering and programming. Your role is to assist organizations in enhancing their test engineering and their code writing processes through Python programming. Here is what to respect while providing guidance:

1. Initial Query and Response:
   - Introduction:  Code Master first inquires about the user's specific tests , issues, needs, whether it's about developing test cases, automating testing tasks, or general Python programming queries.
   - General Answer and User Choice: Provide a general answer relevant to the query, along with Python code examples if applicable. Then, ask the user if they wish to proceed with this approach or explore different options.

2. Detailed Focus:
   - In-Depth Guidance: If the user chooses to proceed with the suggested approach, focus on delivering detailed guidance for that particular aspect of test engineering or Python programming. This includes offering refined code examples and explanations.
   - User Collaboration: Script Master ensures to collaborate with the user, seeking their input and preferences to tailor the guidance specifically to their organizational needs.

3. Iterative Process:
   - Sequential Progression: After addressing a part of the query, Script Master asks the user if they wish to move on to the next aspect or delve deeper into the current topic.
   - User-Controlled Pace: This step-by-step process allows the user to control the pace and direction of their learning and problem-solving journey .

Always ask the user any question that may help you give him a better answer. 
Always focus on making the conversation interactive by asking questions(in general or related to the task) to the user.
Remember, your role is to aid in the development and automation of test cases, as well as to address any Python programming queries that the user may need""",

        model="gpt-4-1106-preview",
        verbose=True,
        #openai_tools=[{"type": "code_interpreter"}], 
        #To use the retrieval feature you can use this code with this you can upload a PDF where the model will use it to answer the user questions it is basically a RAG implemented
        openai_tools=[{"type": "retrieval"},{"type": "code_interpreter"}],
        files=files,
        instructions_prefix="Always be interactive with the user and keep asking him questions before answering. Each answer need to be in parts and then ask the user to proceed to the next part or not before proceeding. any code written needs to be in R markdown to be in a good result in streamlit"
    )

# Function to get agent response
async def get_agent_response(agent, query):
    response = await asyncio.to_thread(agent.chat, query)
    return response.text if hasattr(response, 'text') else str(response)

# Function to deal with upload using fitz


def save_conversation_history(history):
    filename = f'conversation_history_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(history)
    return filename

def download_conversation(history):
    if history:
        filename = save_conversation_history(history)
        st.sidebar.download_button(
            label="Download Conversation",
            data=history.encode('utf-8'),
            file_name=filename,
            mime="text/plain"
        )
def main():
    apply_global_styles()
    style_sidebar()
    style_container()

    st.title("👨🏽‍💻 Test Engineering Model 👩🏽‍💻")

    # Step 1: File uploader
    st.sidebar.title("Step 1: Upload a PDF")
    uploaded_file_path = None

    # Initialize session state for skip_pdf_upload
    if 'skip_pdf_upload' not in st.session_state:
        st.session_state.skip_pdf_upload = False

    if not st.session_state.skip_pdf_upload:
        uploaded_file = st.sidebar.file_uploader("Upload a PDF:", type=["pdf"])
        if uploaded_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
                tmpfile.write(uploaded_file.getvalue())
                uploaded_file_path = tmpfile.name
        else:
            if st.sidebar.button("Skip PDF Upload"):
                st.session_state.skip_pdf_upload = True

    # Step 2: API Key Upload
    if uploaded_file_path or st.session_state.skip_pdf_upload:
        st.sidebar.title("Step 2: Enter API Key")
        api_key = st.sidebar.text_input("Enter your OpenAI API key:", type="password")

        if api_key:
            # Initialize or update the agent in session state
            if 'agent' not in st.session_state or st.session_state.api_key != api_key:
                st.session_state.api_key = api_key
                st.session_state.agent = init_agent(api_key, uploaded_file_path) if api_key else None

            # Initialize session state variables for conversation history
            if 'conversation_history' not in st.session_state:
                st.session_state.conversation_history = ""

            st.sidebar.success("API Key entered successfully.")

            # Step 3: Chat Box
            st.write("Hello! I'm your AI assistant. Type your message and chat with me!")
            user_input = st.text_input("Your message:")

            if user_input:
                with st.spinner('Thinking...⏳'):
                    response = asyncio.run(get_agent_response(st.session_state.agent, user_input))
                    response_lines = response.count('\n') + 1
                    min_height = max(600, response_lines * 20)  # 20 pixels per line
                    st.text_area("AI Response:", value=response, height=min_height)

                st.session_state.conversation_history += f"User: {user_input}\nAI: {response}\n"

            if st.session_state.conversation_history:
                download_conversation(st.session_state.conversation_history)
        else:
            st.sidebar.warning("Please enter your OpenAI API key to start.")

if __name__ == '__main__':
    main()
