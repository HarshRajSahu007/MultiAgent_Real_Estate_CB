import streamlit as st
import os
import json
from dotenv import load_dotenv
import logging
from logging.handlers import RotatingFileHandler
from typing import Optional, Dict, Any
import traceback
import hashlib

# Configure logging
def setup_logging():
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            RotatingFileHandler(
                os.path.join(log_dir, 'real_estate_bot.log'),
                maxBytes=1024*1024*5,  # 5MB
                backupCount=5
            ),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logging()

load_dotenv()

from utils.langraph_workflow import create_agent_workflow, initialize_state, execute_workflow

st.set_page_config(
    page_title="Real Estate Chatbot",
    page_icon="🏠",
    layout="centered"
)

def hash_uploaded_file(uploaded_file):
    """Generate SHA256 hash of the uploaded image's content"""
    if uploaded_file is None:
        return None
    file_bytes = uploaded_file.read()
    uploaded_file.seek(0)  # Reset pointer after reading
    return hashlib.sha256(file_bytes).hexdigest()

# Initialize session states
if "last_image_hash" not in st.session_state:
    st.session_state.last_image_hash = None
if "clear_file_uploader" not in st.session_state:
    st.session_state.clear_file_uploader = False
if "file_uploader_key" not in st.session_state:
    st.session_state.file_uploader_key = 0

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
    .error-message {
        color: #dc3545;
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8d7da;
    }
    .file-uploader {
        padding: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

def display_assistant_message(response: Dict[str, Any]):
    """Display assistant message with proper formatting"""
    with st.chat_message("assistant"):
        if "agent" in response:
            agent_class = "issue" if "Issue Detection" in response["agent"] else "tenancy"
            st.markdown(f'<div class="agent-tag {agent_class}">{response["agent"]}</div>', unsafe_allow_html=True)
        
        if "analysis" in response:
            st.markdown(response["analysis"])
        elif "answer" in response:
            st.markdown(response["answer"])
            if "location_used" in response and response["location_used"] != "None specified":
                st.caption(f"Location: {response['location_used']}")

def main():
    """Main application logic"""
    # Clear file uploader if flag is set
    if st.session_state.clear_file_uploader:
        st.session_state.clear_file_uploader = False
        st.session_state.file_uploader_key += 1
        st.rerun()

    # Initialize session state
    if 'messages' not in st.session_state:
        logger.info("Initializing session messages")
        st.session_state.messages = []
    
    if 'workflow' not in st.session_state:
        try:
            logger.info("Creating agent workflow")
            st.session_state.workflow = create_agent_workflow()
        except Exception as e:
            logger.error(f"Failed to create workflow: {str(e)}", exc_info=True)
            st.error("Failed to initialize chatbot. Please try again later.")
            return

    st.title("🏠 Real Estate Assistant")
    st.markdown("""
    This multi-agent chatbot can help with property issues and tenancy questions:
    - **Issue Detection**: Upload images of property problems for analysis
    - **Tenancy FAQ**: Ask questions about rental agreements and tenant rights
    """)

    # Sidebar
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
        - Type your question about rental agreements
        - Adding location helps with location-specific answers
        """)

        if st.button("Clear Conversation"):
            st.session_state.messages = []
            st.session_state.last_image_hash = None
            st.session_state.clear_file_uploader = True
            st.rerun()

    # Chat interface
    col1, col2 = st.columns([4, 1])
    with col1:
        user_query = st.chat_input("Type your message here...", key="chat_input")
    with col2:
        uploaded_image = st.file_uploader(
            "Upload image", 
            type=["jpg", "jpeg", "png"], 
            label_visibility="collapsed",
            key=f"file_uploader_{st.session_state.file_uploader_key}"
        )

    # Check for new image upload
    current_image_hash = hash_uploaded_file(uploaded_image) if uploaded_image else None
    new_image_uploaded = (current_image_hash is not None and 
                         current_image_hash != st.session_state.last_image_hash)

    # Display message history
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message("user"):
                if message.get("content"):
                    st.markdown(message["content"])
                if message.get("image"):
                    st.image(message["image"], caption="Uploaded Image", use_column_width=True)
        else:  # assistant
            if isinstance(message, dict):
                display_assistant_message(message)
            else:
                with st.chat_message("assistant"):
                    st.markdown(str(message))

    # Process new input
    if user_query or new_image_uploaded:
        logger.info(f"New input received - Query: {user_query}, Image: {uploaded_image is not None}")
        try:
            # Update image hash in session state
            if uploaded_image:
                st.session_state.last_image_hash = current_image_hash

            # Add user message to history
            user_message = {
                "role": "user",
                "content": user_query if user_query else "Please analyze this image",
                "image": uploaded_image if new_image_uploaded else None
            }
            
            st.session_state.messages.append(user_message)
            logger.debug(f"Added user message to history: {user_message}")
            
            # Display user message immediately
            with st.chat_message("user"):
                if user_query:
                    st.markdown(user_query)
                if uploaded_image and new_image_uploaded:
                    st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)

            # Initialize state
            initial_state = initialize_state(
                query=user_query if user_query else "Please analyze this image",
                image=uploaded_image if new_image_uploaded else None,
                location=location
            )
            logger.debug(f"Initial state: {initial_state}")
            
            # Execute workflow with the initialized state
            with st.spinner("Thinking..."):
                final_state = execute_workflow(st.session_state.workflow, initial_state)
                logger.info(f"Workflow execution result: {final_state}")

            # Validate and display response
            if not final_state or not isinstance(final_state, dict):
                logger.error("Invalid workflow response format")
                st.error("Invalid response from chatbot. Please try again.")
                return

            if "response" not in final_state or final_state["response"] is None:
                agent_type = final_state.get("agent_type", "UNKNOWN")
                error_msg = f"The {agent_type} agent failed to generate a response"
                
                if agent_type == "ISSUE_DETECTION" and not uploaded_image:
                    error_msg += ". Note: Issue Detection requires an image upload."
                
                logger.error(error_msg)
                st.error(error_msg)
                return

            response = final_state["response"]
            
            if not isinstance(response, dict):
                logger.error(f"Invalid agent response format: {response}")
                st.error("Invalid response format. Please try again.")
                return

            # Display the successful response
            logger.info("Displaying assistant response")
            assistant_message = {"role": "assistant", **response}
            st.session_state.messages.append(assistant_message)
            
            # Clear the file uploader after processing
            if new_image_uploaded:
                st.session_state.clear_file_uploader = True
            
            # Rerun to display the new message in the correct order
            st.rerun()

        except Exception as e:
            logger.error(f"Error processing request: {str(e)}", exc_info=True)
            st.error(f"An error occurred: {str(e)}")

    # Footer
    st.markdown("---")
    st.caption("Real Estate Assistant - Powered by OpenAI, LangGraph, and Streamlit")

if __name__ == "__main__":
    main()