import streamlit as st
from fpdf import FPDF
import tempfile
from datetime import datetime
from src.utils.logger import get_logger
import pandas as pd

logger = get_logger(__name__)

class ReportPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'CareerForge AI Report', 0, 1, 'C')
        self.ln(10)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_pdf_report():
    pdf = ReportPDF()
    pdf.add_page()
    
    # Profile Section
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Profile Information', 0, 1)
    pdf.set_font('Arial', '', 10)
    for key, value in st.session_state.user_info.items():
        pdf.cell(0, 10, f'{key.title()}: {value}', 0, 1)
    
    # Applications Summary
    if hasattr(st.session_state, 'job_applications'):
        pdf.add_page()
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Job Applications Summary', 0, 1)
        pdf.set_font('Arial', '', 10)
        
        apps = st.session_state.job_applications
        pdf.cell(0, 10, f'Total Applications: {len(apps)}', 0, 1)
        
        status_counts = apps['Status'].value_counts()
        for status, count in status_counts.items():
            pdf.cell(0, 10, f'{status}: {count}', 0, 1)
    
    # Save to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        pdf.output(tmp_file.name)
        return tmp_file.name

def main():
    st.title("📊 Career Progress Report")
    
    if 'job_applications' not in st.session_state or not isinstance(st.session_state.job_applications, pd.DataFrame):
        st.warning("No job applications data available. Please add some applications first!")
        if st.button("Go to Job Tracking"):
            st.switch_page("pages/3_Job_Tracking.py")
        return
    
    # Display Statistics
    if not st.session_state.job_applications.empty:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Applications", len(st.session_state.job_applications))
        with col2:
            status_counts = st.session_state.job_applications['Status'].value_counts()
            st.metric("Interview Rate", 
                     f"{(status_counts.get('Interview Scheduled', 0) / len(st.session_state.job_applications) * 100):.1f}%")
        
        # Status Distribution
        st.subheader("Application Status Distribution")
        st.bar_chart(status_counts)
        
        # Generate PDF Report
        if st.button("📄 Generate PDF Report"):
            try:
                with st.spinner("Generating report..."):
                    report_path = generate_pdf_report()
                    with open(report_path, "rb") as file:
                        st.download_button(
                            "📥 Download Report",
                            file,
                            f"CareerForge_Report_{datetime.now().strftime('%Y%m%d')}.pdf",
                            "application/pdf"
                        )
                st.success("Report generated successfully!")
            except Exception as e:
                logger.error(f"Report generation failed: {str(e)}")
                st.error("Failed to generate report")
    else:
        st.info("Add some job applications to generate reports!")

if __name__ == "__main__":
    main()
