import time

import streamlit as st

from src.agents.first.agent import FirstAgent
from src.domain.entities import ChatRequest, Message, Role
from src.ui.configs import get_openai_config, get_streamlit_config

# ----------------------------
# Streamlit App Configuration
# ----------------------------
streamlit_config = get_streamlit_config()
st.set_page_config(
    page_title=streamlit_config["page_title"],
    page_icon=streamlit_config["page_icon"],
    layout=streamlit_config["layout"],
)
st.subheader("Dialog")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []


openai_config = get_openai_config()


# Agent selection
agents_mapping = {
    "First Agent": FirstAgent(openai_config),
}

selected_agent_name = st.sidebar.selectbox(
    "Choose an agent:", options=list(agents_mapping.keys()), index=0
)
agent = agents_mapping[selected_agent_name]

# Display chat history
for msg in st.session_state.messages:
    role = "user" if msg.role == Role.USER else "assistant"
    with st.chat_message(role):
        st.write(msg.text)

# Handle user input
if prompt := st.chat_input("Type your message..."):
    # Add user message
    user_msg = Message(role=Role.USER, text=prompt)
    st.session_state.messages.append(user_msg)

    with st.chat_message("user"):
        st.write(user_msg.text)

    # Get agent response
    chat_request = ChatRequest(messages=st.session_state.messages)
    chat_response = agent.chat(chat_request)

    # Display new assistant messages with animation
    new_msgs = chat_response.messages[len(st.session_state.messages) :]
    for msg in new_msgs:
        st.session_state.messages.append(msg)

        with st.chat_message("assistant"):
            placeholder = st.empty()

            # Typing animation
            typing_text = ""
            for char in msg.text:
                typing_text += char
                placeholder.write(typing_text + "▋")
                time.sleep(0.001)

            # Final text
            placeholder.write(msg.text)

    st.rerun()
