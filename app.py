import os
from markitdown import MarkItDown

def extract_text_from_document(file_path):
    """
    Takes the full file path of the uploaded document, 
    extracts the text using MarkItDown, and returns it.
    """
    print(f"🔄 Processing file: {file_path}...")
    
    # Initialize the MarkItDown converter
    md = MarkItDown()
    
    try:
        # Convert the document to text
        result = md.convert(file_path)
        return result.text_content
    except Exception as e:
        return f"❌ Error processing file: {str(e)}"

def save_extracted_text(text, output_folder, original_filename):
    """
    Saves the extracted text into the same folder with a '_extracted.txt' suffix.
    """
    # Change the extension to .txt (e.g., policy.docx becomes policy_extracted.txt)
    base_name = os.path.splitext(original_filename)[0]
    output_filename = f"{base_name}_extracted.txt"
    full_output_path = os.path.join(output_folder, output_filename)
    
    with open(full_output_path, "w", encoding="utf-8") as f:
        f.write(text)
    
    print(f"✅ Success! Extracted text saved to:\n   {full_output_path}")

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    # Your specific folder location
    FOLDER_PATH = r"E:\Just Build\privacy_policy_tool\markdown_files"
    
    # Change this name to match whatever sample file you put inside that folder!
    FILE_NAME = "user_privacy_policy.docx" 
    
    # Combine the folder path and file name together perfectly
    FULL_INPUT_PATH = os.path.join(FOLDER_PATH, FILE_NAME)
    
    # Check if the file actually exists at that location
    if os.path.exists(FULL_INPUT_PATH):
        # 1. Run the text extraction
        extracted_text = extract_text_from_document(FULL_INPUT_PATH)
        
        # 2. Save the result back into your folder
        save_extracted_text(extracted_text, FOLDER_PATH, FILE_NAME)
    else:
        print("⚠️ File Not Found!")
        print(f"Looked for: {FULL_INPUT_PATH}")
        print("Please ensure your document is placed in that exact folder and the FILE_NAME matches exactly.")
        