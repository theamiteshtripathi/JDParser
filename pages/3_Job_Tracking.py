import streamlit as st
import pandas as pd
from datetime import datetime
from src.utils.logger import get_logger

logger = get_logger(__name__)

def initialize_tracking():
    if 'job_applications' not in st.session_state:
        st.session_state.job_applications = pd.DataFrame(
            columns=['Date', 'Company', 'Position', 'URL', 'Status', 'Notes']
        )

def main():
    st.title("📊 Job Application Tracking")
    initialize_tracking()
    
    # Add New Application
    with st.expander("➕ Add New Application", expanded=True):
        with st.form("new_application"):
            col1, col2 = st.columns(2)
            with col1:
                company = st.text_input("Company Name")
                position = st.text_input("Position")
            with col2:
                url = st.text_input("Job URL")
                status = st.selectbox(
                    "Status",
                    ["Applied", "Interview Scheduled", "Rejected", "Offer Received"]
                )
            notes = st.text_area("Notes")
            
            submitted = st.form_submit_button("Add Application")
            if submitted:
                new_app = pd.DataFrame([{
                    'Date': datetime.now().strftime("%Y-%m-%d"),
                    'Company': company,
                    'Position': position,
                    'URL': url,
                    'Status': status,
                    'Notes': notes
                }])
                st.session_state.job_applications = pd.concat(
                    [st.session_state.job_applications, new_app],
                    ignore_index=True
                )
                st.success("Application added!")
    
    # Display Applications
    if not st.session_state.job_applications.empty:
        st.header("📋 Your Applications")
        st.dataframe(
            st.session_state.job_applications,
            use_container_width=True,
            hide_index=True
        )
        
        # Export to CSV
        if st.button("📥 Export to CSV"):
            csv = st.session_state.job_applications.to_csv(index=False)
            st.download_button(
                "Download CSV",
                csv,
                "job_applications.csv",
                "text/csv"
            )

if __name__ == "__main__":
    main()
