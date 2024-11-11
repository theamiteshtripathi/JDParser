import streamlit as st
from fpdf import FPDF
import tempfile
from datetime import datetime
from src.utils.logger import get_logger

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
    
    # Report Options
    st.header("Generate Report")
    include_profile = st.checkbox("Include Profile Information", value=True)
    include_applications = st.checkbox("Include Job Applications", value=True)
    
    if st.button("🔄 Generate Report"):
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

if __name__ == "__main__":
    main()
