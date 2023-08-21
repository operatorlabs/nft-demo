import os
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.agents import initialize_agent
from dotenv import load_dotenv
from operator_content import ContentTool
from langchain.agents import load_tools
from reservoir import ReservoirTool
from langchain.callbacks import StreamlitCallbackHandler  # Assuming this is the correct import for the class

requests_tools = load_tools(["requests_all"])

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(
    openai_api_key=OPENAI_API_KEY,
    temperature=0,
    model_name='gpt-4'
)

# initialize conversational memory
conversational_memory = ConversationBufferWindowMemory(
    memory_key='chat_history',
    k=5,
    return_messages=True
)

system_message = {
    "role": "system",
    "content": "You are a helpful assistant tasked with answering questions. When encountering new words, do not attempt to change their spelling. Assume they are proper nouns."
}

tools = [ContentTool()]

# initialize agent with tools
agent = initialize_agent(
    agent='structured-chat-zero-shot-react-description',
    tools=tools,
    llm=llm,
    verbose=True,
    max_iterations=3,
    early_stopping_method='generate',
    memory=conversational_memory,
    agent_kwargs=system_message
)

st.set_page_config(
    page_title="AI Assistant", 
    page_icon="🤖", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

st.title("AI Assistant")

with st.form(key="form"):
    user_input = st.text_input("Ask your question")
    submit_clicked = st.form_submit_button("Submit Question")

output_container = st.empty()
if submit_clicked:
    output_container = output_container.container()
    output_container.markdown(f"**Question:** {user_input}")

    answer_container = output_container.markdown("**Answer:**", unsafe_allow_html=True)

    # Use the agent to generate an answer
    st_callback = StreamlitCallbackHandler(answer_container)  # Create callback with the container
    answer = agent.run(user_input, callbacks=[st_callback])  # Pass the callback to the run method

    answer_container.markdown(f"<p>{answer}</p>", unsafe_allow_html=True)
