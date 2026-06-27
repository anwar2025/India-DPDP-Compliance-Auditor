# import os
# import json
# from google import genai
# from google.genai import types

# # 1. SETUP YOUR FREE GEMINI API KEY
# # Replace the text below with the API key you copied from Google AI Studio
# API_KEY = "AQ.Ab8RN6JaeU4ODfbPYu778bsMgmDr2m3FjTD7G88dmUiwEsJG_A"
# client = genai.Client(api_key=API_KEY)

# def load_text_file(file_path):
#     """Loads the extracted privacy policy text."""
#     with open(file_path, "r", encoding="utf-8") as f:
#         return f.read()

# def load_json_checklist(file_path):
#     """Loads your DPDP JSON checklist."""
#     with open(file_path, "r", encoding="utf-8") as f:
#         return json.load(f)

# def analyze_compliance(extracted_text, checklist):
#     """
#     Sends the policy text and the DPDP checklist to Gemini 
#     to evaluate compliance gaps.
#     """
#     print("🧠 Analyzing document against DPDP checklist using Gemini (Free Tier)...")
    
#     # We simplify the checklist for the AI prompt so it stays organized
#     simplified_checklist = []
#     for item in checklist:
#         simplified_checklist.append({
#             "Control_ID": item.get("Control ID"),
#             "Clause_Name": item.get("Suggested Clause Name"),
#             "Test_Question": item.get("Compliance Test Question"),
#             "Keywords": item.get("Keywords for Detection"),
#             "Recommendation": item.get("Remediation Recommendation")
#         })

#     # Crafting the instruction prompt for the AI
#     prompt = f"""
#     You are an expert legal compliance auditor specializing in the India DPDP Act 2023.
    
#     I will provide you with:
#     1. An extracted Privacy Policy / Terms & Conditions document.
#     2. A DPDP compliance JSON checklist.

#     Your task:
#     For EACH item in the JSON checklist, check if the extracted Privacy Policy satisfies it.
#     Use the 'Keywords' and 'Test_Question' to help locate the relevant section.
    
#     Provide the output strictly as a valid JSON array of objects with these keys:
#     - Control_ID: (from the checklist)
#     - Clause_Name: (from the checklist)
#     - Status: ("COMPLIANT" or "MISSING" or "PARTIALLY COMPLIANT")
#     - Findings: (Brief summary of what you found or why it's missing)
#     - Suggested_Remediation: (If missing/partial, provide the 'Recommendation' from the checklist, else leave empty)

#     ---
#     CHECKLIST:
#     {json.dumps(simplified_checklist, indent=2)}

#     ---
#     EXTRACTED PRIVACY POLICY TEXT:
#     {extracted_text}
#     """

#     # Call Gemini (using gemini-2.5-flash as it is fast and free)
#     response = client.models.generate_content(
#         model='gemini-1.5-flash',
#         contents=prompt,
#         config=types.GenerateContentConfig(
#             response_mime_type="application/json"
#         ),
#     )
    
#     return response.text

# # --- MAIN EXECUTION ---
# if __name__ == "__main__":
#     # Define your paths (Adjust folder names to match your system)
#     FOLDER_PATH = r"E:\Just Build\privacy_policy_tool\markdown_files"
#     JSON_PATH = r"E:\Just Build\privacy_policy_tool\dpdp_act_2023.json" # Update with your exact JSON filename
    
#     # This is the text file generated from Stage 3
#     EXTRACTED_TEXT_FILE = os.path.join(FOLDER_PATH, "user_privacy_policy_extracted.txt")
    
#     # Check if files exist before running
#     if os.path.exists(EXTRACTED_TEXT_FILE) and os.path.exists(JSON_PATH):
#         # Load data
#         policy_text = load_text_file(EXTRACTED_TEXT_FILE)
#         dpdp_checklist = load_json_checklist(JSON_PATH)
        
#         # Run analysis
#         report_json_string = analyze_compliance(policy_text, dpdp_checklist)
        
#         # Save the report
#         output_report_path = os.path.join(FOLDER_PATH, "compliance_audit_report.json")
#         with open(output_report_path, "w", encoding="utf-8") as f:
#             f.write(report_json_string)
            
#         print(f"🎉 Analysis Complete! Report saved to:\n {output_report_path}")
#     else:
#         print("⚠️ Error: Please check that 'user_privacy_policy_extracted.txt' and your DPDP JSON file exist in their correct folders.")


####This is the code where llama is used 

# import os
# import json
# from openai import OpenAI

# # 1. SETUP LOCAL OLLAMA CLIENT
# # Ollama runs automatically on your machine at http://localhost:11434/v1
# client = OpenAI(
#     base_url="http://localhost:11434/v1",
#     api_key="ollama" # Ollama doesn't need a real key, but the code requires a placeholder string
# )

# def load_text_file(file_path):
#     """Loads the extracted privacy policy text."""
#     with open(file_path, "r", encoding="utf-8") as f:
#         return f.read()

# def load_json_checklist(file_path):
#     """Loads your DPDP JSON checklist."""
#     with open(file_path, "r", encoding="utf-8") as f:
#         return json.load(f)

# def analyze_compliance(extracted_text, checklist):
#     """
#     Sends the policy text and the DPDP checklist to your local Llama 3.2 instance
#     to evaluate compliance gaps.
#     """
#     print("🧠 Analyzing document against DPDP checklist using local Llama 3.2 (Ollama)...")
    
#     # Simplify the checklist data structure for the AI prompt
#     simplified_checklist = []
#     for item in checklist:
#         simplified_checklist.append({
#             "Control_ID": item.get("Control ID"),
#             "Clause_Name": item.get("Suggested Clause Name"),
#             "Test_Question": item.get("Compliance Test Question"),
#             "Keywords": item.get("Keywords for Detection"),
#             "Recommendation": item.get("Remediation Recommendation")
#         })

#     # Crafting the instruction prompt for the AI
#     prompt = f"""
#     You are an expert legal compliance auditor specializing in the India DPDP Act 2023.
    
#     I will provide you with:
#     1. An extracted Privacy Policy / Terms & Conditions document.
#     2. A DPDP compliance JSON checklist.

#     Your task:
#     For EACH item in the JSON checklist, check if the extracted Privacy Policy satisfies it.
#     Use the 'Keywords' and 'Test_Question' to help locate the relevant section.
    
#     Provide the output strictly as a valid JSON array of objects with these keys:
#     - Control_ID: (from the checklist)
#     - Clause_Name: (from the checklist)
#     - Status: ("COMPLIANT" or "MISSING" or "PARTIALLY COMPLIANT")
#     - Findings: (Brief summary of what you found or why it's missing)
#     - Suggested_Remediation: (If missing/partial, provide the 'Recommendation' from the checklist, else leave empty)

#     ---
#     CHECKLIST:
#     {json.dumps(simplified_checklist, indent=2)}

#     ---
#     EXTRACTED PRIVACY POLICY TEXT:
#     {extracted_text}
#     """

#     # Call local Ollama using llama3.2
#     response = client.chat.completions.create(
#         model="llama3.2",
#         messages=[
#             {"role": "user", "content": prompt}
#         ],
#         temperature=0.1 # Low temperature makes the AI strict and analytical rather than creative
#     )
    
#     return response.choices[0].message.content

# # --- MAIN EXECUTION ---
# if __name__ == "__main__":
#     # Define your paths
#     FOLDER_PATH = r"E:\Just Build\privacy_policy_tool\markdown_files"
#     JSON_PATH = r"E:\Just Build\privacy_policy_tool\dpdp_act_2023.json"
    
#     # Text file generated from Stage 3
#     EXTRACTED_TEXT_FILE = os.path.join(FOLDER_PATH, "user_privacy_policy_extracted.txt")
    
#     # Check if files exist before running
#     if os.path.exists(EXTRACTED_TEXT_FILE) and os.path.exists(JSON_PATH):
#         # Load data
#         policy_text = load_text_file(EXTRACTED_TEXT_FILE)
#         dpdp_checklist = load_json_checklist(JSON_PATH)
        
#         # Run analysis
#         report_json_string = analyze_compliance(policy_text, dpdp_checklist)
        
#         # Clean up code backticks if Llama wraps the JSON output in markdown formatting
#         report_json_string = report_json_string.strip()
#         if report_json_string.startswith("```"):
#             report_json_string = report_json_string.strip("`").replace("json\n", "", 1)
            
#         # Save the report
#         output_report_path = os.path.join(FOLDER_PATH, "compliance_audit_report.json")
#         with open(output_report_path, "w", encoding="utf-8") as f:
#             f.write(report_json_string.strip())
            
#         print(f"🎉 Analysis Complete! Report saved to:\n {output_report_path}")
#     else:
#         print("⚠️ Error: Please check that 'user_privacy_policy_extracted.txt' and your DPDP JSON file exist in their correct folders.")


##This code is where we have removed the large langugage Model. 

import os
import json
import re

def load_text_file(file_path):
    """Loads the extracted privacy policy text."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def load_json_checklist(file_path):
    """Loads your DPDP JSON checklist."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def find_snippet_with_keyword(text, keyword):
    """
    Finds the exact sentence or paragraph where a keyword appears 
    to provide verifiable evidence of compliance.
    """
    # Split text into sentences roughly using punctuation boundaries
    sentences = re.split(r'(?<=[.!?])\s+', text)
    for sentence in sentences:
        if keyword.lower() in sentence.lower():
            return sentence.strip()
    return "Keyword found in document text."

def analyze_compliance_rules(policy_text, checklist):
    print("⚙️ [STAGE 4] Executing Rule-Based Compliance Matching Engine...")
    
    audit_report = []
    
    for item in checklist:
        control_id = item.get("Control ID")
        clause_name = item.get("Suggested Clause Name")
        recommendation = item.get("Remediation Recommendation")
        
        # 1. Grab the keywords and split them cleanly by commas
        raw_keywords = item.get("Keywords for Detection", "")
        keywords_list = [kw.strip() for kw in raw_keywords.split(",") if kw.strip()]
        
        matched_keywords = []
        evidence_snippet = ""
        
        # 2. Check if any keyword exists in the policy text
        for kw in keywords_list:
            if kw.lower() in policy_text.lower():
                matched_keywords.append(kw)
                # Capture the first context snippet where the keyword occurs for traceability
                if not evidence_snippet:
                    evidence_snippet = find_snippet_with_keyword(policy_text, kw)
        
        # 3. Apply the scoring rule status
        if matched_keywords:
            status = "COMPLIANT"
            findings = f"Matched keyword(s): {', '.join(matched_keywords)}. Found in text: \"{evidence_snippet}\""
            remediation = ""
        else:
            status = "MISSING"
            findings = f"None of the required keywords ({raw_keywords}) were detected in the text."
            remediation = recommendation

        # 4. Construct the audited output object
        audit_report.append({
            "Control_ID": control_id,
            "Clause_Name": clause_name,
            "Status": status,
            "Findings": findings,
            "Suggested_Remediation": remediation
        })
        
    return audit_report

# --- MAIN ENGINE CONTROL ---
if __name__ == "__main__":
    # Your explicit paths
    FOLDER_PATH = r"E:\Just Build\privacy_policy_tool\markdown_files"
    JSON_PATH = r"E:\Just Build\privacy_policy_tool\dpdp_act_2023.json"
    EXTRACTED_TEXT_FILE = os.path.join(FOLDER_PATH, "user_privacy_policy_extracted.txt")
    
    if os.path.exists(EXTRACTED_TEXT_FILE) and os.path.exists(JSON_PATH):
        # Load your files
        policy_text = load_text_file(EXTRACTED_TEXT_FILE)
        dpdp_checklist = load_json_checklist(JSON_PATH)
        
        # Run rule analysis
        report_data = analyze_compliance_rules(policy_text, dpdp_checklist)
        
        # Save output report
        output_report_path = os.path.join(FOLDER_PATH, "compliance_audit_report.json")
        with open(output_report_path, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=4)
            
        print(f"🎉 Rule matching complete! Clean report saved to:\n {output_report_path}")
    else:
        print("⚠️ Error: Please verify that 'user_privacy_policy_extracted.txt' and 'dpdp_act_2023.json' exist.")

        



