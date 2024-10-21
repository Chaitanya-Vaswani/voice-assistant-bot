import streamlit as st
import asyncio
from rasa.core.agent import Agent
from rasa.utils.endpoints import EndpointConfig

agent = Agent.load('models/20241020-211135-partial-yeoman.tar.gz', action_endpoint=EndpointConfig(url="http://localhost:5055/webhook"))

# Function to handle async responses
async def get_bot_response(user_input):
    return await agent.handle_text(user_input)

st.title("Rasa Chatbot")

# User input
user_input = st.text_input("You: ", "")

# Send input and get bot response when button is pressed
if st.button("Send"):
    response = asyncio.run(get_bot_response(user_input))
    for message in response:
        st.write(f"Bot: {message['text']}")

