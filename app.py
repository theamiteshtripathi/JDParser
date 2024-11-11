import streamlit as st
from Assistants.CareerForge.assistant_handler import CareerForgeAssistant
from src.utils.logger import get_logger

logger = get_logger(__name__)

def initialize_session_state():
    if 'assistant' not in st.session_state:
        try:
            assistant = CareerForgeAssistant()
            st.session_state.assistant = assistant
            logger.info("Assistant initialized in session state")
        except Exception as e:
            logger.error(f"Error initializing assistant: {str(e)}")
            st.error(f"Failed to initialize assistant: {str(e)}")
    
    # Initialize other session state variables
    if 'user_info' not in st.session_state:
        st.session_state.user_info = {}
    if 'resume_info' not in st.session_state:
        st.session_state.resume_info = None
    if 'job_applications' not in st.session_state:
        st.session_state.job_applications = []

def main():
    st.set_page_config(
        page_title="CareerForge AI",
        page_icon="🚀",
        layout="wide"
    )
    
    initialize_session_state()
    
    st.title("🚀 Welcome to CareerForge AI")
    
    # User Profile Section
    st.header("👤 Complete Your Profile")
    with st.form("user_profile"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name", st.session_state.user_info.get('name', ''))
            email = st.text_input("Email", st.session_state.user_info.get('email', ''))
            
        with col2:
            industry = st.selectbox(
                "Preferred Industry",
                ["Technology", "Finance", "Healthcare", "Education", "Other"],
                index=0 if not st.session_state.user_info.get('industry') else 0
            )
            experience = st.selectbox(
                "Years of Experience",
                ["0-2", "3-5", "5-10", "10+"],
                index=0 if not st.session_state.user_info.get('experience') else 0
            )
            
        submit = st.form_submit_button("Save Profile")
        if submit:
            st.session_state.user_info = {
                'name': name,
                'email': email,
                'industry': industry,
                'experience': experience
            }
            st.success("Profile saved successfully!")
    
    # Quick Navigation
    st.header("🎯 What would you like to do?")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("💭 Career Guidance")
        st.write("Get personalized career advice and guidance")
        if st.button("Start Career Consultation"):
            st.switch_page("pages/1_Career_Guidance.py")
            
    with col2:
        st.info("📝 Resume Analysis")
        st.write("Upload and analyze your resume for improvements")
        if st.button("Analyze Resume"):
            st.switch_page("pages/2_Resume_Analysis.py")
            
    with col3:
        st.info("📊 Job Application Tracking")
        st.write("Track your job applications and progress")
        if st.button("Track Applications"):
            st.switch_page("pages/3_Job_Tracking.py")
    
    # Getting Started Guide
    with st.expander("📚 Getting Started Guide"):
        st.markdown("""
        1. **Complete Your Profile**: Add your basic information
        2. **Upload Your Resume**: Go to Resume Analysis page
        3. **Start Job Tracking**: Add job applications to track
        4. **Get Guidance**: Chat with AI for career advice
        5. **Generate Reports**: Track your progress
        """)

if __name__ == "__main__":
    main()
