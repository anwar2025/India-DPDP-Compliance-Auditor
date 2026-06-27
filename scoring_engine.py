# import os
# import json
# from openai import OpenAI

# # Initialize local Ollama client
# client = OpenAI(
#     base_url="http://localhost:11434/v1",
#     api_key="ollama" 
# )

# def load_text_file(file_path):
#     with open(file_path, "r", encoding="utf-8") as f:
#         return f.read()

# def load_json_checklist(file_path):
#     with open(file_path, "r", encoding="utf-8") as f:
#         return json.load(f)

# def analyze_compliance(extracted_text, checklist):
#     print("🧠 Analyzing document against DPDP checklist using local Llama 3.2 (Ollama)...")
    
#     simplified_checklist = []
#     for item in checklist:
#         simplified_checklist.append({
#             "Control_ID": item.get("Control ID"),
#             "Clause_Name": item.get("Suggested Clause Name"),
#             "Test_Question": item.get("Compliance Test Question"),
#             "Keywords": item.get("Keywords for Detection"),
#             "Recommendation": item.get("Remediation Recommendation")
#         })

#     prompt = f"""
#     You are an expert legal compliance auditor specializing in the India DPDP Act 2023.
    
#     Your task:
#     For EACH item in the JSON checklist, check if the extracted Privacy Policy satisfies it.
#     Use the 'Keywords' and 'Test_Question' to locate the relevant section.
    
#     Provide the output strictly as a valid JSON array of objects with these keys:
#     - Control_ID
#     - Clause_Name
#     - Status: (Must be exactly "COMPLIANT", "MISSING", or "PARTIALLY COMPLIANT")
#     - Findings: (Brief summary of what you found or why it's missing)
#     - Suggested_Remediation: (If missing/partial, provide the 'Recommendation' from the checklist, else leave empty)

#     Do not include any introductory or concluding text. Do not wrap the response in markdown blocks. Output raw JSON only.

#     ---
#     CHECKLIST:
#     {json.dumps(simplified_checklist, indent=2)}

#     ---
#     EXTRACTED PRIVACY POLICY TEXT:
#     {extracted_text}
#     """

#     # Call local Ollama with JSON structure enforcement
#     response = client.chat.completions.create(
#         model="llama3.2",
#         messages=[{"role": "user", "content": prompt}],
#         temperature=0.1,
#         response_format={"type": "json_object"} # Tells Ollama to strictly structure output as JSON
#     )
    
#     return response.choices[0].message.content

# if __name__ == "__main__":
#     FOLDER_PATH = r"E:\Just Build\privacy_policy_tool\markdown_files"
#     JSON_PATH = r"E:\Just Build\privacy_policy_tool\dpdp_act_2023.json"
#     EXTRACTED_TEXT_FILE = os.path.join(FOLDER_PATH, "user_privacy_policy_extracted.txt")
    
#     if os.path.exists(EXTRACTED_TEXT_FILE) and os.path.exists(JSON_PATH):
#         policy_text = load_text_file(EXTRACTED_TEXT_FILE)
#         dpdp_checklist = load_json_checklist(JSON_PATH)
        
#         raw_output = analyze_compliance(policy_text, dpdp_checklist).strip()
        
#         # --- CLEANUP LOGIC ---
#         # Strip markdown ```json markers if Llama ignored the strict formatting rule
#         if raw_output.startswith("```"):
#             raw_output = raw_output.strip("`").replace("json", "", 1).strip()
        
#         # Double check if it's safe JSON before saving
#         try:
#             parsed_json = json.loads(raw_output)
            
#             # If Llama wrapped the array inside a root key like {"compliance_report": [...]}, extract just the array
#             if isinstance(parsed_json, dict) and len(parsed_json) == 1:
#                 key = list(parsed_json.keys())[0]
#                 if isinstance(parsed_json[key], list):
#                     parsed_json = parsed_json[key]

#             output_report_path = os.path.join(FOLDER_PATH, "compliance_audit_report.json")
#             with open(output_report_path, "w", encoding="utf-8") as f:
#                 json.dump(parsed_json, f, indent=4)
                
#             print(f"🎉 Stage 4 complete! Clean report saved to:\n {output_report_path}")
            
#         except json.JSONDecodeError as e:
#             print("❌ Llama output invalid JSON data. Saving raw text output to debug.")
#             debug_path = os.path.join(FOLDER_PATH, "debug_raw_output.txt")
#             with open(debug_path, "w", encoding="utf-8") as f:
#                 f.write(raw_output)
#             print(f"Please inspect {debug_path} to see what Llama replied.")
            
#     else:
#         print("⚠️ Error: Check file locations.")

import os
import json

def calculate_compliance_score(checklist_path, report_path):
    print("📊 [STAGE 5] Calculating Final Compliance Score Metric...")
    
    with open(checklist_path, "r", encoding="utf-8") as f:
        master_checklist = json.load(f)
        
    with open(report_path, "r", encoding="utf-8") as f:
        audit_report = json.load(f)

    # Map control IDs to weights
    weights_dict = {item.get("Control ID"): int(item.get("Compliance Weight (1-10)", 5)) for item in master_checklist}

    total_possible_score = 0
    total_earned_score = 0
    
    compliant_count = 0
    missing_count = 0

    for item in audit_report:
        c_id = item.get("Control_ID")
        status = str(item.get("Status", "MISSING")).upper()
        
        weight = weights_dict.get(c_id, 5)
        total_possible_score += weight
        
        if status == "COMPLIANT":
            total_earned_score += weight
            compliant_count += 1
        elif status == "PARTIALLY COMPLIANT":
            total_earned_score += (weight * 0.5)
            compliant_count += 0.5
        else:
            missing_count += 1

    # Calculate final score percentage
    compliance_percentage = (total_earned_score / total_possible_score * 100) if total_possible_score > 0 else 0
    rounded_score = round(compliance_percentage, 2)

    # Benchmarking compliance level profiles
    if rounded_score >= 90:
        grade = "EXCELLENT (Highly Compliant with DPDP Act)"
    elif rounded_score >= 70:
        grade = "MODERATE (Passable, but needs immediate adjustments)"
    else:
        grade = "POOR (High risk of regulatory non-compliance)"

    return {
        "score": f"{rounded_score}%",
        "evaluation_grade": grade,
        "clauses_checked": len(audit_report),
        "fully_or_partially_compliant_clauses": compliant_count,
        "missing_clauses": missing_count
    }

if __name__ == "__main__":
    FOLDER_PATH = r"E:\Just Build\privacy_policy_tool\markdown_files"
    JSON_CHECKLIST = r"E:\Just Build\privacy_policy_tool\dpdp_act_2023.json"
    AUDIT_REPORT = os.path.join(FOLDER_PATH, "compliance_audit_report.json")

    if os.path.exists(JSON_CHECKLIST) and os.path.exists(AUDIT_REPORT):
        metrics = calculate_compliance_score(JSON_CHECKLIST, AUDIT_REPORT)
        print(f"Score: {metrics['score']}")
        