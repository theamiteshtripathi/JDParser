import streamlit as st
import openai
import requests
import json
import os
from docx import Document
from github import Github
from src.summarize_text_with_gpt35 import summarize_text_with_gpt35
from src.parse_summarized_text import parse_summarized_text
from src.generate_full_resume_with_gpt35 import generate_full_resume_with_gpt35, read_resume_from_docx, upload_to_github

def main():
    st.set_page_config(page_title="CareerForge AI", page_icon="📑", layout="wide")
    
    # Add custom CSS
    st.markdown("""
        <style>
        .main {
            padding: 2rem;
        }
        .stButton>button {
            width: 100%;
            background-color: #FF4B4B;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Title and Description
    st.title("🚀 CareerForge AI")
    st.markdown("### Your AI-powered Job Application Assistant")
    
    # Sidebar for API Keys
    with st.sidebar:
        st.header("Configuration")
        openai_api_key = st.text_input("OpenAI API Key", type="password")
        notion_api_key = st.text_input("Notion API Key", type="password")
        database_id = st.text_input("Notion Database ID")
        github_token = st.text_input("GitHub Token", type="password")
        repo_name = st.text_input("GitHub Repo Name", value="JDParser")
        
    # Main content area
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📄 Resume Upload")
        uploaded_resume = st.file_uploader("Upload your resume (DOCX format)", type=['docx'])
        
        if uploaded_resume:
            # Save the uploaded file temporarily
            with open("temp_resume.docx", "wb") as f:
                f.write(uploaded_resume.getbuffer())
            resume_data = read_resume_from_docx("temp_resume.docx")
            st.success("Resume uploaded successfully!")
            
        st.subheader("🔗 Job Details")
        job_link = st.text_input("Job Posting URL")
        job_description = st.text_area("Job Description", height=300)
        
        if st.button("Process Job Application"):
            if not all([openai_api_key, notion_api_key, database_id, github_token, uploaded_resume, job_description]):
                st.error("Please fill in all required fields!")
            else:
                with st.spinner("Processing your application..."):
                    try:
                        # Summarize job description
                        summarized_text = summarize_text_with_gpt35(job_description, openai_api_key)
                        
                        # Generate tailored resume
                        tailored_resume_path = generate_full_resume_with_gpt35(
                            job_description, resume_data, openai_api_key)
                        
                        # Upload to GitHub
                        github_url = upload_to_github(tailored_resume_path, repo_name, github_token)
                        
                        # Parse and save to Notion
                        parsed_data = parse_summarized_text(summarized_text, github_url, job_link)
                        response = insert_into_notion(parsed_data, notion_api_key, database_id)
                        
                        st.success("Application processed successfully!")
                        
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
    
    with col2:
        st.subheader("📊 Results")
        if 'parsed_data' in locals():
            st.json(parsed_data)
            
            st.subheader("🎯 Tailored Resume")
            if os.path.exists(tailored_resume_path):
                with open(tailored_resume_path, "rb") as file:
                    st.download_button(
                        label="Download Tailored Resume",
                        data=file,
                        file_name="tailored_resume.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )

if __name__ == "__main__":
    main()
