import streamlit as st
from src.utils.logger import get_logger

logger = get_logger(__name__)

def main():
    st.title("💭 Career Guidance")
    
    # Initialize chat history
    if 'guidance_messages' not in st.session_state:
        st.session_state.guidance_messages = []
    
    # Sidebar with topic suggestions
    with st.sidebar:
        st.header("🎯 Discussion Topics")
        st.info("""
        - Career Path Planning
        - Skill Development
        - Interview Preparation
        - Salary Negotiation
        - Industry Insights
        """)
    
    # Display chat history
    for message in st.session_state.guidance_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask for career guidance..."):
        with st.chat_message("user"):
            st.markdown(prompt)
            st.session_state.guidance_messages.append({"role": "user", "content": prompt})
        
        try:
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = st.session_state.assistant.chat(prompt)
                    st.markdown(response)
                    st.session_state.guidance_messages.append({"role": "assistant", "content": response})
        except Exception as e:
            logger.error(f"Chat error: {str(e)}")
            st.error("Failed to get response. Please try again.")

if __name__ == "__main__":
    main()
