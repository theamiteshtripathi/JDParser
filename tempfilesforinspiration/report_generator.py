# Report generation logic
import os
from fpdf import FPDF
from backend.logger import get_logger
from datetime import datetime
import textwrap
from backend.chatbot import chat_with_assistant
import re

logger = get_logger(__name__)

class PDF(FPDF):
    def header(self):
        # Logo
        self.image('frontend/assets/lacormarca.png', 180, 8, 25)
        # Line break
        self.ln(20)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Página ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

    def multi_cell_with_wrap(self, w, h, txt, border=0, align='J', fill=False):
        # Custom method to handle long text
        lines = textwrap.wrap(txt, width=int(w / self.font_size * 2))
        for line in lines:
            self.multi_cell(w, h, line, border, align, fill)

def clean_markdown(text):
    # Remove Markdown syntax for bold, italics, and headers
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # Bold
    text = re.sub(r'\*(.*?)\*', r'\1', text)      # Italics
    text = re.sub(r'### ', '', text)              # Headers
    return text

def generate_report(user_data, processed_files, chat_history, assistant):
    logger.info(f"Generating report for user: {user_data['name']}")
    logger.info(f"Current working directory: {os.getcwd()}")
    
    try:
        # Generate summary using the assistant
        summary_prompt = "Please provide a concise summary of our conversation, highlighting the key points discussed, any career recommendations made, and important insights about the user's talents, intelligences, and personality traits."
        summary = chat_with_assistant(assistant, summary_prompt, generate_summary=True)
        
        # Clean the summary text
        clean_summary = clean_markdown(summary)
        
        # Create the 'reports' directory if it doesn't exist
        os.makedirs('reports', exist_ok=True)

        pdf = PDF()
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)

        # Get the absolute path to the fonts directory
        fonts_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'fonts'))

        # Add fonts
        pdf.add_font('DejaVu', '', os.path.join(fonts_dir, 'DejaVuSansCondensed.ttf'), uni=True)
        pdf.add_font('DejaVu', 'B', os.path.join(fonts_dir, 'DejaVuSansCondensed-Bold.ttf'), uni=True)

        # Title
        pdf.set_font('DejaVu', 'B', 14)
        pdf.cell(0, 10, 'Reporte de Consulta Vocacional', 0, 1)
        pdf.ln(10)

        # User Information
        pdf.set_font('DejaVu', 'B', 10)
        pdf.cell(0, 10, f"Nombre: {user_data['name']}", 0, 1)
        pdf.cell(0, 10, f"Fecha: {datetime.now().strftime('%Y-%m-%d')}", 0, 1)
        pdf.ln(10)

        # Processed Files Information
        pdf.set_font('DejaVu', 'B', 12)
        pdf.cell(0, 10, 'Resultados de los Exámenes', 0, 1)
        pdf.set_font('DejaVu', '', 10)
        for file in processed_files:
            pdf.multi_cell(0, 10, f"{file['name']}:\n{file['content'][:500]}...")
            pdf.ln(5)

        # Add summary to the PDF
        pdf.add_page()
        pdf.set_font('DejaVu', 'B', 12)
        pdf.cell(0, 10, 'Resumen de la Consulta', 0, 1)
        pdf.set_font('DejaVu', '', 10)
        pdf.multi_cell(0, 10, clean_summary)
        pdf.ln(10)

        # Chat History
        pdf.add_page()
        pdf.set_font('DejaVu', 'B', 12)
        pdf.cell(0, 10, 'Consulta Virtual', 0, 1)
        for message in chat_history:
            pdf.set_font('DejaVu', 'B', 10)
            pdf.cell(0, 10, f"{message['role'].capitalize()}:", 0, 1)
            pdf.set_font('DejaVu', '', 10)
            clean_content = clean_markdown(message['content'])
            pdf.multi_cell(0, 10, clean_content)
            pdf.ln(5)

        # Generate a unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = f"reports/{user_data['name']}_{timestamp}_reporte_vocacional.pdf"
        pdf.output(report_path)
        logger.info(f"Report generated successfully: {report_path}")
        return report_path
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        logger.exception("Detailed traceback:")
        raise
