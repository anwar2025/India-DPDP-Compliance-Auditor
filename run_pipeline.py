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

# def run_stage_4_analysis(extracted_text, checklist):
#     print("\n🧠 [STAGE 4] Analyzing document against DPDP checklist using local Llama 3.2...")
    
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
#     Evaluate the extracted Privacy Policy against the checklist below.
    
#     You MUST output a valid JSON array of objects with exactly these keys:
#     - Control_ID
#     - Clause_Name
#     - Status: (Must be exactly "COMPLIANT", "MISSING", or "PARTIALLY COMPLIANT")
#     - Findings: (Brief summary of what you found or why it's missing)
#     - Suggested_Remediation: (Provide the 'Recommendation' from the checklist if missing/partial)

#     Return ONLY the raw JSON array. No conversational text. No markdown blocks.

#     CHECKLIST:
#     {json.dumps(simplified_checklist, indent=2)}

#     EXTRACTED TEXT:
#     {extracted_text}
#     """

#     response = client.chat.completions.create(
#         model="llama3.2",
#         messages=[{"role": "user", "content": prompt}],
#         temperature=0.1
#     )
    
#     raw_output = response.choices[0].message.content.strip()
    
#     # Clean up accidental markdown wraps
#     if raw_output.startswith("```"):
#         raw_output = raw_output.strip("`").replace("json", "", 1).strip()
        
#     return raw_output

# def run_stage_5_scoring(master_checklist, audit_report_data):
#     print("📊 [STAGE 5] Calculating DPDP Compliance Score scorecard...")
    
#     weights_dict = {item.get("Control ID"): int(item.get("Compliance Weight (1-10)", 5)) for item in master_checklist}
    
#     total_possible_score = 0
#     total_earned_score = 0
#     breakdown = []

#     for item in audit_report_data:
#         c_id = item.get("Control_ID")
#         status = str(item.get("Status", "MISSING")).upper()
#         clause_name = item.get("Clause_Name", "Unknown Clause")
        
#         weight = weights_dict.get(c_id, 5)
#         total_possible_score += weight
        
#         if "COMPLIANT" in status and "PARTIALLY" not in status:
#             earned = weight
#         elif "PARTIALLY" in status:
#             earned = weight * 0.5
#         else:
#             earned = 0
            
#         total_earned_score += earned
#         breakdown.append({
#             "Control_ID": c_id,
#             "Clause_Name": clause_name,
#             "Status": status,
#             "Max_Weight": weight,
#             "Earned_Points": earned
#         })

#     final_percentage = (total_earned_score / total_possible_score * 100) if total_possible_score > 0 else 0
    
#     if final_percentage >= 90: grade = "Excellent (Low DPDP Risk)"
#     elif final_percentage >= 75: grade = "Good (Medium-Low Risk)"
#     elif final_percentage >= 50: grade = "Needs Improvement (Medium-High Risk)"
#     else: grade = "Critical Non-Compliance (High Legal/Penalty Risk)"

#     return {
#         "Compliance_Score": f"{round(final_percentage, 2)}%",
#         "Risk_Status_Grade": grade,
#         "Total_Possible_Points": total_possible_score,
#         "Total_Earned_Points": total_earned_score,
#         "Detailed_Breakdown": breakdown
#     }

# # --- MAIN ENGINE CONTROL ---
# if __name__ == "__main__":
#     FOLDER_PATH = r"E:\Just Build\privacy_policy_tool\markdown_files"
#     JSON_PATH = r"E:\Just Build\privacy_policy_tool\dpdp_act_2023.json"
#     EXTRACTED_TEXT_FILE = os.path.join(FOLDER_PATH, "user_privacy_policy_extracted.txt")
    
#     if os.path.exists(EXTRACTED_TEXT_FILE) and os.path.exists(JSON_PATH):
#         policy_text = load_text_file(EXTRACTED_TEXT_FILE)
#         dpdp_checklist = load_json_checklist(JSON_PATH)
        
#         # Max 3 attempts to get clean data from local Llama instance
#         max_retries = 3
#         parsed_audit_data = None
        
#         for attempt in range(max_retries):
#             raw_report = run_stage_4_analysis(policy_text, dpdp_checklist)
#             try:
#                 parsed_audit_data = json.loads(raw_report)
#                 if isinstance(parsed_audit_data, dict) and len(parsed_audit_data) == 1:
#                     key = list(parsed_audit_data.keys())[0]
#                     if isinstance(parsed_audit_data[key], list):
#                         parsed_audit_data = parsed_audit_data[key]
#                 break # Success, break out of loop
#             except json.JSONDecodeError:
#                 print(f"⚠️ Llama returned malformed text on attempt {attempt + 1}. Retrying...")
        
#         if parsed_audit_data:
#             # Save Stage 4 Clean Output
#             with open(os.path.join(FOLDER_PATH, "compliance_audit_report.json"), "w", encoding="utf-8") as f:
#                 json.dump(parsed_audit_data, f, indent=4)
                
#             # Immediately run Stage 5 Scoring engine using the clean variable data
#             score_results = run_stage_5_scoring(dpdp_checklist, parsed_audit_data)
            
#             # Save Final Scores
#             with open(os.path.join(FOLDER_PATH, "final_compliance_score.json"), "w", encoding="utf-8") as f:
#                 json.dump(score_results, f, indent=4)
                
#             print("\n=======================================================")
#             print(f"🏆 FINAL DPDP COMPLIANCE SCORE: {score_results['Compliance_Score']}")
#             print(f"📋 RISK ASSESSMENT GRADE:     {score_results['Risk_Status_Grade']}")
#             print("=======================================================")
#             print(f"Full metrics summary successfully updated in your folder structure!")
#         else:
#             print("❌ Pipeline failed: Llama 3.2 was unable to format the text into clean JSON after 3 attempts.")
#     else:
#         print("⚠️ Missing core configuration tracking files.")


