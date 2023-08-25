import os
from docx import Document
import openai

# Function to read the resume from a DOCX file
def read_resume_from_docx(file_path):
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

# Function to read or upload a resume
def read_or_upload_resume(file_path="docs/Amitesh Tripathi Resume Aug 15.docx"):
    if os.path.exists(file_path):
        stored_resume = read_resume_from_docx(file_path)  # Use read_resume_from_docx here
        
        print("An existing resume is found. Would you like to use it? (yes/no)")
        choice = input()
        
        if choice.lower() == 'yes':
            return stored_resume
        else:
            print("Please upload your new resume (DOCX format).")
    
    # Prompt user to provide the path to the new resume
    resume_path = input("Path to your resume: ")
    
    # Read the resume from the DOCX file
    resume_data = read_resume_from_docx(resume_path)
    
    # Store it for future use
    with open(file_path, 'wb') as f:  # Change mode to 'wb'
        f.write(resume_data.encode('utf-8'))  # Encode to bytes and write
   
    return resume_data

def generate_resume_bullets_with_gpt35(jdtext, resumetext, api_key):
    openai.api_key = api_key
    # Generate the prompt
    prompt = f"""Based on the following job description and the existing resume data, especially experience bullets, please generate 4-5 bullet points for the resume. The bullet points should align with the resume experience bullets and be crafted to clear Applicant Tracking Systems (ATS) and land an interview.

    The bullet points should follow the STAR method (Situation, Task, Action, Result) and be formatted as 'Action-word + Impact + result'. Please read the sample bullet points from the existing resume for formatting inspiration:

    Existing Resume Data:
    {resumetext}

    Job Description:
    {jdtext}

    Please generate 4-5 bullet points:"""
    
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.5,
        max_tokens=150
    )
    
    tailored_bullets = response.choices[0].text.strip()
    return tailored_bullets

