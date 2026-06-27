# import os
# import json
# from openai import OpenAI

# # 1. SETUP YOUR OPENROUTER API KEY
# # Replace the text below with your OpenRouter API key
# OPENROUTER_API_KEY = "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"

# # Initialize the client pointing to OpenRouter's universal gateway
# client = OpenAI(
#     base_url="https://openrouter.ai/api/v1",
#     api_key=OPENROUTER_API_KEY,
#     default_headers={
#         "HTTP-Referer": "http://localhost:3000", # Optional, but helps OpenRouter track requests
#         "X-Title": "DPDP Compliance Engine",
#     }
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
#     Sends the policy text and the DPDP checklist to OpenRouter 
#     to evaluate compliance gaps.
#     """
#     print("🧠 Analyzing document against DPDP checklist using OpenRouter (Free Model)...")
    
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

#     # Call OpenRouter using an available free model
#     response = client.chat.completions.create(
#         model="google/gemini-2.5-flash", # You can also change this to other free model slugs if needed
#         messages=[
#             {"role": "user", "content": prompt}
#         ]
#     )
    
#     return response.choices[0].message.content

# # --- MAIN EXECUTION ---
# if __name__ == "__main__":
#     # Define your paths
#     FOLDER_PATH = r"E:\Just Build\privacy_policy_tool\markdown_files"
#     JSON_PATH = r"E:\Just Build\privacy_policy_tool\dpdp_act_2023.json" # Adjust name if needed
    
#     # Text file generated from Stage 3
#     EXTRACTED_TEXT_FILE = os.path.join(FOLDER_PATH, "user_privacy_policy_extracted.txt")
    
#     # Check if files exist before running
#     if os.path.exists(EXTRACTED_TEXT_FILE) and os.path.exists(JSON_PATH):
#         # Load data
#         policy_text = load_text_file(EXTRACTED_TEXT_FILE)
#         dpdp_checklist = load_json_checklist(JSON_PATH)
        
#         # Run analysis
#         report_json_string = analyze_compliance(policy_text, dpdp_checklist)
        
#         # Clean up code backticks if the model returns them wrapped in ```json ...

#         if report_json_string.startswith("```"):
#            report_json_string = report_json_string.strip("`").replace("json\n", "", 1)
        
#     # Save the report
#     output_report_path = os.path.join(FOLDER_PATH, "compliance_audit_report.json")
#     with open(output_report_path, "w", encoding="utf-8") as f:
#         f.write(report_json_string)
        
#     print(f"🎉 Analysis Complete! Report saved to:\n {output_report_path}")
# else:
#     print("⚠️ Error: Please check that 'user_privacy_policy_extracted.txt' and your DPDP JSON file exist in their correct folders.")