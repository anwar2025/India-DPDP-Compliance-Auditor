import os
import json
from fpdf import FPDF
from fpdf.enums import XPos, YPos

class CompliancePDF(FPDF):
    def header(self):
        # Title banner
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(0, 51, 102) # Professional dark blue
        self.cell(0, 10, "DPDP Act 2023 Compliance Audit Report", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_draw_color(0, 51, 102)
        self.line(10, 22, 200, 22)
        self.ln(10)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}} | Confidential Internal Compliance Audit", align="C")

def clean_text(text):
    """
    Replaces smart quotes and non-latin symbols with basic versions 
    so standard Helvetica font can render them without crashing.
    """
    if not text:
        return ""
    replacements = {
        "\u2018": "'",  # Left single quote ‘
        "\u2019": "'",  # Right single quote ’
        "\u201c": '"',  # Left double quote “
        "\u201d": '"',  # Right double quote ”
        "\u2013": "-",  # En dash –
        "\u2014": "-",  # Em dash —
        "\u2022": "*",  # Bullet point •
    }
    for search, replace in replacements.items():
        text = text.replace(search, replace)
    
    # Fallback: encode to latin-1 and ignore anything else that's weird
    return text.encode('latin-1', 'replace').decode('latin-1')

def create_pdf_report(json_report_path, output_pdf_path):
    print("📄 Generating PDF Audit Report...")
    
    with open(json_report_path, "r", encoding="utf-8") as f:
        report_data = json.load(f)
        
    pdf = CompliancePDF()
    pdf.alias_nb_pages()
    
    # Set safe drawing margins
    pdf.set_margins(15, 15, 15)
    pdf.add_page()
    pdf.set_font("Helvetica", size=10)
    
    usable_width = pdf.epw 
    
    for item in report_data:
        c_id = item.get("Control_ID", "N/A")
        clause_name = item.get("Clause_Name", "N/A")
        status = item.get("Status", "MISSING").upper()
        
        # Clean strings aggressively to prevent encoding errors
        findings = clean_text(item.get("Findings", ""))
        remediation = clean_text(item.get("Suggested_Remediation", ""))
        
        # Heading for each control clause
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(51, 51, 51)
        pdf.cell(usable_width, 7, f"[{c_id}] {clause_name}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        # Status Label badge styling
        pdf.set_font("Helvetica", "B", 10)
        if status == "COMPLIANT":
            pdf.set_text_color(0, 128, 0) # Green
        elif status == "PARTIALLY COMPLIANT":
            pdf.set_text_color(255, 140, 0) # Orange
        else:
            pdf.set_text_color(204, 0, 0) # Red
            
        pdf.cell(usable_width, 6, f"Status: {status}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        # Findings text block
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(77, 77, 77)
        pdf.multi_cell(usable_width, 5, f"Findings: {findings}")
        pdf.ln(1)
        
        # Remediation if missing or partial
        if remediation:
            pdf.set_font("Helvetica", "I", 10)
            pdf.set_text_color(153, 0, 0)
            pdf.multi_cell(usable_width, 5, f"Remediation Recommendation: {remediation}")
            
        pdf.ln(5) # Space between clauses
        
    pdf.output(output_pdf_path)
    print(f"🎉 PDF successfully created at:\n {output_pdf_path}")

if __name__ == "__main__":
    FOLDER_PATH = r"E:\Just Build\privacy_policy_tool\markdown_files"
    JSON_REPORT = os.path.join(FOLDER_PATH, "compliance_audit_report.json")
    OUTPUT_PDF = os.path.join(FOLDER_PATH, "compliance_audit_report.pdf")
    
    if os.path.exists(JSON_REPORT):
        create_pdf_report(JSON_REPORT, OUTPUT_PDF)
    else:
        print("⚠️ Cannot find compliance_audit_report.json. Please run your compliance engine first.")

        