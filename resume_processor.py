import docx
import google.generativeai as genai

api_key = "your gemini api key"

def configure_genai(api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-flash')

# function to extract text from DOCX file
def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

# function to get skills and suitable roles from LLM
def get_skills_and_roles(model, resume_text):
    skillstext = "This is a resume. Give all the skills of the candidate separated with commas. " + resume_text
    rolestext = "This is a resume, follow this format strictly. Format: Give all the role names only to which candidate can apply separated with commas. " + resume_text
    skills2 = model.generate_content(skillstext).text
    roles = model.generate_content(rolestext).text
    return skills2, roles

# function to process resume and get skills and roles
def process_resume(api_key, file_path):
    model = configure_genai(api_key)
    
    # Extract text from resume
    resume_text = extract_text_from_docx(file_path)
    print("Resume Text Extracted:\n", resume_text)

    # Get skills and suitable roles using LLM
    skills2, roles = get_skills_and_roles(model, resume_text)
    print("\nExtracted Skills:\n", skills2)
    print("\nSuitable Roles:\n", roles)
    return skills2, roles

#if __name__ == "__main__":
#    file_path = "C:\\Users\\kisha\\Documents\\job_genie\\Kishan Tripathi Resume.docx"
#    skills2, roles = process_resume(api_key, file_path)
#
