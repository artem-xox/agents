import time

import streamlit as st

from src.agents.chat.agent import SimpleChat
from src.agents.supporter.agent import SupporterAgent
from src.domain.entities import ChatRequest, Message, Role
from src.infra.cache.dialogs import DialogCache
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

# Initialize dialog cache
dialog_cache = DialogCache()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_dialog_id" not in st.session_state:
    st.session_state.current_dialog_id = None
if "selected_dialog_from_dropdown" not in st.session_state:
    st.session_state.selected_dialog_from_dropdown = ""

openai_config = get_openai_config()

# Initialize agents in session state to avoid recreating them
if "agents_mapping" not in st.session_state:
    st.session_state.agents_mapping = {
        "SimpleChat": SimpleChat(openai_config),
        "Supporter": SupporterAgent(openai_config),
    }

# Agent selection
selected_agent_name = st.sidebar.selectbox(
    "Choose an agent:", options=list(st.session_state.agents_mapping.keys()), index=0
)
agent = st.session_state.agents_mapping[selected_agent_name]

# Dialog management sidebar
st.sidebar.markdown("---")

# Display current dialog info
if st.session_state.current_dialog_id:
    st.sidebar.info(f"**Current Dialog:** {st.session_state.current_dialog_id}")

# Debug info (can be removed in production)
if st.sidebar.checkbox("Show debug info"):
    st.sidebar.write(
        f"Selected from dropdown: {st.session_state.selected_dialog_from_dropdown}"
    )
    st.sidebar.write(f"Current dialog ID: {st.session_state.current_dialog_id}")
    st.sidebar.write(f"Message count: {len(st.session_state.messages)}")


# Start new dialog button
if st.sidebar.button("Start a new dialog", type="secondary"):
    # Save current dialog if it has messages
    if st.session_state.messages:
        dialog_id = dialog_cache.save_dialog(
            st.session_state.messages, st.session_state.current_dialog_id
        )
        st.success(f"Dialog saved as {dialog_id}")

    # Clear current dialog
    st.session_state.messages = []
    st.session_state.current_dialog_id = None
    st.session_state.selected_dialog_from_dropdown = ""
    st.rerun()

# Load existing dialogs
st.sidebar.markdown("### Load Previous Dialog")
available_dialogs = dialog_cache.list_dialogs()

if available_dialogs:
    dialog_options = [
        f"{d['dialog_id']} ({d['message_count']} messages)" for d in available_dialogs
    ]
    selected_dialog = st.sidebar.selectbox(
        "Choose a dialog to load:", options=[""] + dialog_options, index=0
    )

    # Handle dialog selection
    if (
        selected_dialog
        and selected_dialog != st.session_state.selected_dialog_from_dropdown
    ):
        st.session_state.selected_dialog_from_dropdown = selected_dialog

        if selected_dialog:  # Not empty selection
            # Extract dialog ID from selection
            dialog_id = selected_dialog.split(" (")[0]

            # Load the dialog
            loaded_messages = dialog_cache.load_dialog(dialog_id)
            if loaded_messages:
                st.session_state.messages = loaded_messages
                st.session_state.current_dialog_id = dialog_id
                st.success(f"Loaded dialog: {dialog_id}")
                st.rerun()
            else:
                st.error(f"Failed to load dialog: {dialog_id}")
                st.session_state.selected_dialog_from_dropdown = ""

    # Reset dropdown selection if no dialog is currently loaded
    elif not st.session_state.current_dialog_id:
        st.session_state.selected_dialog_from_dropdown = ""

    # Delete dialog option
    st.sidebar.markdown("### Delete Dialog")
    delete_options = [d["dialog_id"] for d in available_dialogs]
    dialog_to_delete = st.sidebar.selectbox(
        "Choose a dialog to delete:", options=[""] + delete_options, index=0
    )

    if dialog_to_delete and st.sidebar.button("🗑️ Delete Dialog", type="secondary"):
        if dialog_cache.delete_dialog(dialog_to_delete):
            st.success(f"Deleted dialog: {dialog_to_delete}")
            # Reset dropdown if we deleted the currently loaded dialog
            if st.session_state.current_dialog_id == dialog_to_delete:
                st.session_state.messages = []
                st.session_state.current_dialog_id = None
                st.session_state.selected_dialog_from_dropdown = ""
            st.rerun()
        else:
            st.error(f"Failed to delete dialog: {dialog_to_delete}")
else:
    st.sidebar.info("No saved dialogs found.")

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

    # Auto-save dialog after each message exchange
    if st.session_state.messages:
        dialog_id = dialog_cache.save_dialog(
            st.session_state.messages, st.session_state.current_dialog_id
        )
        st.session_state.current_dialog_id = dialog_id

    st.rerun()
