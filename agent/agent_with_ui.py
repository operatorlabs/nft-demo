import os
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.agents import initialize_agent
from dotenv import load_dotenv
from operator_content import ContentTool
from langchain.agents import load_tools
from neynar_fid import AddressesToFidTool
from neynar_followed_by import FollowedByFidTool
from find_channel_url import FindChannelIDTool
from operator_search import OperatorTool
from neynar_channels import SearchInChannelTool
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
    k=10,
    return_messages=True
)

system_message = {
    "role": "system",
    "content": """
You are a helpful assistant tasked with finding relevant casts on Farcaster.
You must return the hash/ID for each cast or thread you return, or your answer cannot be evaluated.

The first thing you must always do is decide whether the user is looking for content by a specific entity or not.

If you need to identify content/casts by a specific identity (ex: 'balaji's casts about zkp'), you must follow these steps exactly in sequence:
1. Use the Operator Search Tool to get the associated addresses for an identity/identities.
2. Use the AddressesToFidTool to get the FID (farcaster ID) associated with the addresses you found in step 1.
3. Use the Operator Content Tool, BUT MAKE SURE in addition to supplying the query also supply the 'fid' parameter with the FID you retrieved.

The last step is ALWAYS to check and make sure you included the hash associated with each thread or cast in your answer.

NOTE: When encountering new words, do not attempt to change their spelling. Assume they are proper nouns. You must follow the instructions below for your final answer:
"""
}

tools = [OperatorTool(), AddressesToFidTool(), ContentTool(), FollowedByFidTool(), FindChannelIDTool(), SearchInChannelTool()]

# initialize agent with tools
agent = initialize_agent(
    agent='structured-chat-zero-shot-react-description',
    tools=tools,
    llm=llm,
    verbose=True,
    max_iterations=5,
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

    custom_input = user_input + """

NOTE: If your goal is to return a FINAL ANSWER, you MUST follow these rules: 
1. Return a numbered list of threads that are relevant to the user's original query, AND
2. Each thread in the list MUST INCLUDE the thread ID so it can be tracked by the user, AND
3. You must DOUBLE CHECK your list to ensure steps 1 and 2 are followed BEFORE returning your answer
"""
    answer = agent.run(user_input, callbacks=[st_callback])  # Pass the callback to the run method

    answer_container.markdown(f"<p>{answer}</p>", unsafe_allow_html=True)
