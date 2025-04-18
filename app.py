import streamlit as st
import os
import json
from dotenv import load_dotenv


from utils.langraph_workflow import create_agent_workflow, initialize_state, execute_workflow


load_dotenv()


st.set_page_config(
    page_title="Real Estate Chatbot",
    page_icon="🏠",
    layout="centered"
)


st.markdown("""
<style>
    .stButton button {
        background-color: #4CAF50;
        color: white;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
    }
    .chat-message.user {
        background-color: #d9fdd3;
    }
    .chat-message.assistant {
        background-color: #f0f2f5;
    }
    .chat-message .avatar {
        width: 20%;
    }
    .chat-message .message {
        width: 80%;
    }
    .chat-message .avatar img {       
        max-width: 78px;
        max-height: 78px;
        border-radius: 50%;
        object-fit: cover;
    }
    .agent-tag {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        font-size: 0.75rem;
        font-weight: 700;
        color: white;
        background-color: #007bff;
        border-radius: 0.25rem;
        margin-bottom: 0.5rem;
    }
    .agent-tag.issue {
        background-color: #dc3545;
    }
    .agent-tag.tenancy {
        background-color: #17a2b8;
    }
</style>
""", unsafe_allow_html=True)


if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'workflow' not in st.session_state:
    st.session_state.workflow = create_agent_workflow()


st.title("🏠 Real Estate Assistant")
st.markdown("""
This multi-agent chatbot can help with property issues and tenancy questions:
- **Issue Detection**: Upload images of property problems for analysis and troubleshooting
- **Tenancy FAQ**: Ask questions about rental agreements, tenant rights, and landlord responsibilities
""")

# Sidebar for location info
with st.sidebar:
    st.header("Your Information")
    location = st.text_input("Your Location (Optional)", placeholder="e.g., London, UK")
    
    st.markdown("---")
    st.markdown("### How to use")
    st.markdown("""
    **For Property Issues:**
    - Upload an image of the problem
    - Ask a question about the issue

    **For Tenancy Questions:**
    - Just type your question about rental agreements, rights, etc.
    - Adding your location helps with location-specific answers
    """)

# Chat input area
user_query = st.chat_input("Type your message here...")
uploaded_image = st.file_uploader("Upload an image of the property issue (optional)", type=["jpg", "jpeg", "png"])

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "user":
            st.markdown(message["content"])
            if "image" in message and message["image"] is not None:
                st.image(message["image"], caption="Uploaded Image", use_column_width=True)
        else:
            if "agent" in message:
                if "Issue Detection" in message["agent"]:
                    st.markdown(f'<div class="agent-tag issue">{message["agent"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="agent-tag tenancy">{message["agent"]}</div>', unsafe_allow_html=True)
            
            if "analysis" in message:
                st.markdown(message["analysis"])
            elif "answer" in message:
                st.markdown(message["answer"])
                if "location_used" in message and message["location_used"] != "None specified":
                    st.caption(f"Location: {message['location_used']}")
            else:
                st.markdown(message["content"])


if user_query or uploaded_image:

    user_message = {"role": "user", "content": user_query or "Please analyze this image", "image": uploaded_image}
    st.session_state.messages.append(user_message)
    

    with st.chat_message("user"):
        st.markdown(user_message["content"])
        if uploaded_image:
            st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
    

    initial_state = initialize_state(
        query=user_query or "Please analyze this image",
        image=uploaded_image,
        location=location
    )
    

    with st.spinner("Thinking..."):
        final_state = execute_workflow(st.session_state.workflow, initial_state)
    

    if final_state and "response" in final_state:
        response = final_state["response"]
        st.session_state.messages.append({"role": "assistant", **response})
        

        with st.chat_message("assistant"):
            if "agent" in response:
                if "Issue Detection" in response["agent"]:
                    st.markdown(f'<div class="agent-tag issue">{response["agent"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="agent-tag tenancy">{response["agent"]}</div>', unsafe_allow_html=True)
            
            if "analysis" in response:
                st.markdown(response["analysis"])
            elif "answer" in response:
                st.markdown(response["answer"])
                if "location_used" in response and response["location_used"] != "None specified":
                    st.caption(f"Location: {response['location_used']}")


st.markdown("---")
st.caption("Real Estate Assistant - Powered by OpenAI, LangGraph, and Streamlit")