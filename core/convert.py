from fpdf import FPDF
import os

def create_pdf(text_content, output_path):
    pdf = FPDF()
    pdf.add_page()
    font_path = r'C:\AI_Workspace\ai_workspace_core\assets\fonts\DejaVuSans.ttf'
    if os.path.exists(font_path):
        pdf.add_font('DejaVu', '', font_path, uni=True)
        pdf.set_font('DejaVu', '', 12)
    else:
        pdf.set_font('Helvetica', '', 12)
    pdf.multi_cell(0, 10, text_content)
    pdf.output(output_path)
    return output_path
