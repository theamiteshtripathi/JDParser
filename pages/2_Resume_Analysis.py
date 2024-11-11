import streamlit as st
import tempfile
import os
from pathlib import Path
from src.utils.logger import get_logger
import PyPDF2
from docx import Document
from datetime import datetime

logger = get_logger(__name__)

def read_pdf(file):
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        logger.error(f"Error reading PDF: {str(e)}")
        st.error("Error reading PDF file. Please ensure it's not corrupted.")
        return None

def read_docx(file):
    try:
        doc = Document(file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        logger.error(f"Error reading DOCX: {str(e)}")
        st.error("Error reading DOCX file. Please ensure it's not corrupted.")
        return None

def main():
    st.title("📝 Resume Analysis")
    
    # Initialize chat history if not exists
    if 'resume_chat_history' not in st.session_state:
        st.session_state.resume_chat_history = []
    
    # Display chat history
    for message in st.session_state.resume_chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Resume Upload and Analysis
    uploaded_file = st.file_uploader(
        "Upload your resume for analysis",
        type=['pdf', 'docx'],
        help="Supported formats: PDF, DOCX"
    )
    
    if uploaded_file:
        process_resume(uploaded_file)
    
    # Persistent chat input
    if prompt := st.chat_input("Ask about your resume..."):
        with st.chat_message("user"):
            st.markdown(prompt)
            st.session_state.resume_chat_history.append({"role": "user", "content": prompt})
        
        try:
            with st.chat_message("assistant"):
                with st.spinner("Analyzing..."):
                    context = f"Resume Content: {st.session_state.get('resume_text', 'No resume uploaded yet')}"
                    response = st.session_state.assistant.chat(f"{context}\n\nUser Question: {prompt}")
                    st.markdown(response)
                    st.session_state.resume_chat_history.append({"role": "assistant", "content": response})
        except Exception as e:
            logger.error(f"Chat error: {str(e)}")
            st.error("Failed to get response. Please try again.")

if __name__ == "__main__":
    main()
