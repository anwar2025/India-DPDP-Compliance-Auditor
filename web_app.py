import os
import json
import streamlit as st

# Import your existing logic blocks
from app import extract_text_from_document, save_extracted_text
from compliance_engine import analyze_compliance_rules
from scoring_engine import calculate_compliance_score
from generate_pdf import create_pdf_report

# Page configurations
st.set_page_config(page_title="DPDP Compliance Auditor", page_icon="🛡️", layout="wide")

# App Header
st.title("🛡️ India DPDP Act 2023 Compliance Auditor")
st.subheader("Upload a Privacy Policy or Terms & Conditions document to scan for legal compliance gaps.")
st.markdown("---")

# Layout columns: Left side for upload & metrics, Right side for detailed breakdown
col1, col2 = st.columns([1, 2])

# --- CLOUD COMPATIBLE PATHS ---
# This automatically finds your project directory, whether local or on Streamlit Cloud
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FOLDER_PATH = os.path.join(BASE_DIR, "markdown_files")
JSON_CHECKLIST = os.path.join(BASE_DIR, "dpdp_act_2023.json")

# Ensure markdown files folder exists
os.makedirs(FOLDER_PATH, exist_ok=True)

with col1:
    st.header("📥 Upload Document")
    uploaded_file = st.file_uploader("Choose a file (.docx, .pdf, .txt, .md)", type=["docx", "pdf", "txt", "md"])
    
    if uploaded_file is not None:
        st.success(f"📄 File uploaded: {uploaded_file.name}")
        
        # Save uploaded file temporarily to process it
        temp_input_path = os.path.join(FOLDER_PATH, uploaded_file.name)
        with open(temp_input_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        # Trigger button for processing pipeline
        if st.button("🚀 Run Compliance Audit", type="primary"):
            with st.spinner("Processing pipeline... Extracting text, executing rules, and compiling scores."):
                
                # STAGE 3: Extract Text
                extracted_text = extract_text_from_document(temp_input_path)
                
                # Create standard output filename text match
                base_name = os.path.splitext(uploaded_file.name)[0]
                output_filename = f"{base_name}_extracted.txt"
                save_extracted_text(extracted_text, FOLDER_PATH, output_filename)
                
                # Load Master Rule Checklist
                with open(JSON_CHECKLIST, "r", encoding="utf-8") as f:
                    dpdp_checklist = json.load(f)
                
                # STAGE 4: Execute Rule Engine
                audit_report_data = analyze_compliance_rules(extracted_text, dpdp_checklist)
                report_json_path = os.path.join(FOLDER_PATH, "compliance_audit_report.json")
                with open(report_json_path, "w", encoding="utf-8") as f:
                    json.dump(audit_report_data, f, indent=4)
                    
                # STAGE 5: Scoring Metrics Engine
                scores = calculate_compliance_score(JSON_CHECKLIST, report_json_path)
                
                # STAGE 6: PDF Generation
                output_pdf_path = os.path.join(FOLDER_PATH, "compliance_audit_report.pdf")
                create_pdf_report(report_json_path, output_pdf_path)
                
                # Store audit results in session memory for display
                st.session_state['audit_completed'] = True
                st.session_state['scores'] = scores
                st.session_state['report_data'] = audit_report_data
                st.session_state['pdf_path'] = output_pdf_path
                
                st.balloons()

    # If audit run complete, render key metrics cards
    if 'audit_completed' in st.session_state:
        st.markdown("---")
        st.header("🏆 Compliance Summary")
        scores = st.session_state['scores']
        
        # Display large status badges
        st.metric(label="Total Score", value=scores['score'])
        st.info(f"**Rating Profile:** \n{scores['evaluation_grade']}")
        
        # Small metric subcategories
        st.write(f"📊 Clauses Audited: **{scores['clauses_checked']}**")
        st.write(f"❌ Missing Requirements: **{scores['missing_clauses']}**")
        
        # PDF Download Button
        with open(st.session_state['pdf_path'], "rb") as pdf_file:
            st.download_button(
                label="📥 Download Printable PDF Report",
                data=pdf_file,
                file_name="DPDP_Compliance_Audit_Report.pdf",
                mime="application/pdf"
            )

with col2:
    st.header("📋 Detailed Audit Breakdown")
    if 'audit_completed' in st.session_state:
        report_data = st.session_state['report_data']
        
        for item in report_data:
            c_id = item.get("Control_ID")
            clause_name = item.get("Clause_Name")
            status = item.get("Status")
            findings = item.get("Findings")
            remediation = item.get("Suggested_Remediation")
            
            # Change expander color grouping based on compliance tier
            if status == "COMPLIANT":
                title_prefix = f"🟢 [{c_id}] {clause_name} - COMPLIANT"
            elif status == "PARTIALLY COMPLIANT":
                title_prefix = f"🟡 [{c_id}] {clause_name} - PARTIALLY COMPLIANT"
            else:
                title_prefix = f"🔴 [{c_id}] {clause_name} - MISSING"
                
            with st.expander(title_prefix):
                st.markdown(f"**Findings & Traceability Evidence:**")
                st.write(findings)
                if remediation:
                    st.markdown(f"<span style='color:red'>**Required Remediation Fix:**</span>", unsafe_html=True)
                    st.warning(remediation)
    else:
        st.info("Your detailed compliance scorecard, clause-by-clause evaluation text, and recommendations will be displayed here once you run the audit engine.")







        
