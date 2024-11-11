import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from src.utils.data_store import DataStore
from src.utils.logger import get_logger
import json

logger = get_logger(__name__)

def main():
    st.title("📊 Job Application Tracking")
    
    # Initialize DataStore
    if 'data_store' not in st.session_state:
        st.session_state.data_store = DataStore()

    # Manual URL input section
    with st.expander("🔗 Add Job URL Manually"):
        url = st.text_input("Job Posting URL")
        if url:
            try:
                with st.spinner("Analyzing job posting..."):
                    # Call your FastAPI endpoint
                    response = requests.post(
                        "http://localhost:8000/api/parse-job",
                        json={"url": url}
                    )
                    
                    if response.ok:
                        job_data = response.json()
                        
                        # Display parsed information
                        st.subheader("📝 Parsed Job Details")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write("**Company:**", job_data['company'])
                            st.write("**Position:**", job_data['title'])
                            st.write("**Location:**", job_data['location'])
                            
                        with col2:
                            status = st.selectbox("Status", 
                                ["Applied", "Interview Scheduled", "Rejected", "Offer Received"])
                            notes = st.text_area("Notes")
                        
                        if st.button("Add to Tracking"):
                            job_data.update({
                                'status': status,
                                'notes': notes,
                                'date': datetime.now().strftime("%Y-%m-%d")
                            })
                            st.session_state.data_store.save_application(job_data)
                            st.success("Application added successfully!")
                            st.rerun()
                            
            except Exception as e:
                st.error(f"Failed to parse job details: {str(e)}")

    # Display tracked applications
    try:
        applications_df = st.session_state.data_store.load_applications()
        if not applications_df.empty:
            st.header("📋 Tracked Applications")
            
            # Add filters
            col1, col2 = st.columns(2)
            with col1:
                status_filter = st.multiselect(
                    "Filter by Status",
                    options=applications_df['Status'].unique()
                )
            with col2:
                date_range = st.date_input(
                    "Date Range",
                    value=[applications_df['Date'].min(), applications_df['Date'].max()]
                )
            
            # Apply filters
            filtered_df = applications_df
            if status_filter:
                filtered_df = filtered_df[filtered_df['Status'].isin(status_filter)]
            
            # Display applications
            st.dataframe(
                filtered_df,
                use_container_width=True,
                hide_index=True
            )
            
            # Export options
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📥 Export to CSV"):
                    csv = filtered_df.to_csv(index=False)
                    st.download_button(
                        "Download CSV",
                        csv,
                        "job_applications.csv",
                        "text/csv"
                    )
            with col2:
                if st.button("🗑️ Clear Filters"):
                    st.rerun()
        else:
            st.info("No applications tracked yet. Add your first application above!")
            
    except Exception as e:
        st.error(f"Failed to load applications: {str(e)}")

def parse_job_url(assistant, url):
    prompt = f"""
    Please analyze this job posting URL and extract the required information: {url}
    Return the information in our standard JSON format.
    Remember to use "Not mentioned" for any missing information.
    """
    try:
        response = assistant.chat(prompt)
        parsed_data = json.loads(response)
        
        # Add tracking fields
        parsed_data.update({
            'date_added': datetime.now().strftime("%Y-%m-%d"),
            'resume_link': "Not uploaded",
            'status': "New",
            'applied_date': "Not applied"
        })
        return parsed_data
    except Exception as e:
        st.error(f"Failed to parse job posting: {str(e)}")
        return None

if __name__ == "__main__":
    main()
