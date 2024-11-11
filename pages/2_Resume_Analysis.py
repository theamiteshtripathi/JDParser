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
    
    # Check if user info exists
    if 'user_info' not in st.session_state:
        st.warning("Please complete your profile on the home page first!")
        if st.button("Go to Home"):
            st.switch_page("app.py")
        return
    
    # Display user info
    with st.expander("👤 Your Profile", expanded=False):
        for key, value in st.session_state.user_info.items():
            st.text(f"{key.title()}: {value}")
    
    # Resume Upload Section
    uploaded_file = st.file_uploader(
        "Upload your resume for analysis",
        type=['pdf', 'docx'],
        help="Supported formats: PDF, DOCX"
    )
    
    if uploaded_file:
        try:
            with st.spinner("Processing resume..."):
                # Save file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{uploaded_file.name.split(".")[-1]}') as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    file_path = tmp_file.name
                
                # Read content based on file type
                if uploaded_file.type == "application/pdf":
                    resume_text = read_pdf(file_path)
                else:
                    resume_text = read_docx(file_path)
                
                # Clean up temp file
                os.unlink(file_path)
                
                if resume_text:
                    st.session_state.resume_text = resume_text
                    st.success("Resume processed successfully!")
                    
                    # Store resume info in session state
                    st.session_state.resume_info = {
                        'filename': uploaded_file.name,
                        'content': resume_text
                    }
                    
        except Exception as e:
            logger.error(f"Error processing file: {str(e)}")
            st.error("Failed to process the file. Please try again.")
    
    # Analysis Section
    if 'resume_text' in st.session_state and st.session_state.resume_text:
        if st.button("🔍 Analyze Resume"):
            try:
                with st.spinner("Analyzing your resume..."):
                    analysis_prompt = f"""
                    Please analyze this resume for {st.session_state.user_info.get('name', 'the candidate')} 
                    who is interested in {st.session_state.user_info.get('industry', 'the industry')}.
                    
                    Focus on:
                    1. ATS Compatibility
                    2. Key Skills Identified
                    3. Missing Important Elements
                    4. Format and Structure
                    5. Action Items for Improvement
                    
                    Resume Text:
                    {st.session_state.resume_text}
                    """
                    
                    response = st.session_state.assistant.chat(analysis_prompt)
                    st.session_state.analysis_result = response
                    
                    # Store analysis in session state
                    st.session_state.resume_analysis = {
                        'timestamp': str(datetime.now()),
                        'result': response
                    }
                    
                    st.markdown(response)
            except Exception as e:
                logger.error(f"Analysis failed: {str(e)}")
                st.error("Analysis failed. Please try again.")

if __name__ == "__main__":
    main()
