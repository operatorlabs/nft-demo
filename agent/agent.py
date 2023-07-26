import os
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from dotenv import load_dotenv
from planner import PlannerTool  
from operator_search import OperatorTool
from langchain.agents import load_tools
from reservoir import ReservoirTool

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

tools = [OperatorTool(), PlannerTool(), ReservoirTool()]

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

# Ask the agent to execute a task
agent("Get the attributes of the bored ape yacht club nft")
