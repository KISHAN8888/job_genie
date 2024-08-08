import requests
import pandas as pd
from linkedin_api import Linkedin
import browser_cookie3
import docx
import google.generativeai as genai


def get_job_recommendations(keywords, location_name, file_path):

    cookiejar_simple = browser_cookie3.firefox(domain_name='.linkedin.com')
    cookiejar = requests.cookies.RequestsCookieJar()
    for cookie in cookiejar_simple:
        cookiejar.set_cookie(cookie)
    
    api = Linkedin('ritvik024748@gmail.com', 'Iambatman', cookies=cookiejar)
    api_key = "AIzaSyBgXXTa043ZpKYxIYfGOQ6P91fBD6Bkfxk"
    API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
    API_TOKEN = "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"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}

    jobs = api.search_jobs(keywords=keywords, location_name=location_name)
    jobs = jobs[:20] # remove this line for good results
    print(jobs)

    def get_skill_names(skill_match_statuses):
        return [skill['skill']['name'] for skill in skill_match_statuses]


    def extract_job_info(jobs):
        job_info = []
        for job in jobs:
            job_title = job.get('title')
            tracking_urn = job.get('trackingUrn')
            
            if tracking_urn:
    
                
                job_id = tracking_urn.split(':')[-1]
                job_skills_data = api.get_job_skills(job_id)
                skill_match_statuses = job_skills_data.get('skillMatchStatuses', [])
                job_skills = get_skill_names(skill_match_statuses)
                job_link = f"https://www.linkedin.com/jobs/view/{job_id}/"
                job_info.append({'urnlijobposting': tracking_urn, 'job_id': job_id, 'link': job_link,'title':job_title, 'skills':job_skills})
        return job_info
    

    job_info = extract_job_info(jobs)
    
    print(job_info)
    
    for job in job_info:
        print(job)

    job_data = pd.DataFrame(job_info)
    print(job_data)

    

    def configure_genai(api_key):
        genai.configure(api_key=api_key)
        return genai.GenerativeModel('gemini-1.5-flash')
    
    # Function to extract text from DOCX fil
    def extract_text_from_docx(file_path):
        doc = docx.Document(file_path)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return '\n'.join(full_text)
    
    
    def get_skills_and_roles(model, resume_text):
        skillstext = "This is a resume. Give all the skills of the candidate separated with commas. " + resume_text
        rolestext = "This is a resume, follow this format strictly. Format: Give all the role names only to which candidate can apply separated with commas. " + resume_text
        skills2 = model.generate_content(skillstext).text
        roles = model.generate_content(rolestext).text
        return skills2, roles
    
    
    def process_resume(api_key, file_path):
        model = configure_genai(api_key)
        
        resume_text = extract_text_from_docx(file_path)
        print("Resume Text Extracted:\n", resume_text)
    
        skills2, roles = get_skills_and_roles(model, resume_text)
        print("\nExtracted Skills:\n", skills2)
        print("\nSuitable Roles:\n", roles)
        return skills2, roles
    
    
 
 
    skillsofuser, roles = process_resume(api_key, file_path)

    



    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()
    
    # User skills
    user_skills = [skill.strip() for skill in skillsofuser.split(',')]
    
    # Combine all skills into a single string
    user_skills_text = ", ".join(user_skills)
    
    def calculate_job_match(row):
        # Combine title and skills (if available) for job text
        job_text = row['title']
        if isinstance(row['skills'], str) and row['skills'] != '[]':
            job_text += " " + row['skills']
        
        # Calculate similarity
        payload = {
            "inputs": {
                "source_sentence": user_skills_text,
                "sentences": [job_text]
            }
        }
        result = query(payload)
        
        # The API returns a list of similarities, we only sent one job so we take the first (and only) result
        return result[0] if isinstance(result, list) and len(result) > 0 else 0
    
    # Calculate match scores for all jobs
    job_data['match_score'] = job_data.apply(calculate_job_match, axis=1)
    
    # Sort jobs by match score in descending order
    top_jobs = job_data.sort_values('match_score', ascending=False).head(5)
    
    # Print results
    for _, job in top_jobs.iterrows():
        print(f"Title: {job['title']}")
        print(f"Match score: {job['match_score']:.2f}")
        print(f"Link: {job['link']}")
        print(f"Skills: {job['skills']}")
        print(f"Job_id: {job['job_id']}")
        print()
        
    results = []
    for _, job in top_jobs.iterrows():
        job_result = {
            "title": job['title'],
            "match_score": job['match_score'],
            "link": job['link'],
            "skills": job['skills'],
            "job_id": job['job_id']
            
        }
        results.append(job_result)
    
    # Return results (you can further process or display these as needed)
    print(results)

    job_ids = [job['job_id'] for job in results]
    job_links = [job['link'] for job in results]
    skills_required = [job['skills'] for job in results]

    print(job_ids)
    print(job_links)
    print(skills_required)

    def get_job(job_ids):
        job_datas = []
        for job_id in job_ids:
            job_data = api.get_job(job_id)
            job_datas.append(job_data)
            print(f"Iteration {len(job_datas)}: job_id={job_id}, job_data={job_data}")
    
        
    
        return job_datas
    
    job_datas = get_job(job_ids)


    def extract_job_details(api_response):
    # Extract company name
        company_name = "N/A"
        company_url = "N/A"
        try:
            company_details = api_response.get('companyDetails', {})
            if 'com.linkedin.voyager.deco.jobs.web.shared.WebCompactJobPostingCompany' in company_details:
                company_info = company_details['com.linkedin.voyager.deco.jobs.web.shared.WebCompactJobPostingCompany']
                company_name = company_info.get('companyResolutionResult', {}).get('name', "N/A")
                company_url = company_info.get('companyResolutionResult', {}).get('url', "N/A")
            elif 'company' in company_details:
                company_name = company_details['company'].get('name', "N/A")
                company_url = company_details['company'].get('url', "N/A")
        except Exception as e:
            print(f"Error extracting company details: {e}")
    
        title = api_response.get('title', "N/A")
    
      
        location = api_response.get('formattedLocation', "N/A")
    
     
        remote_work_allowed = api_response.get('workRemoteAllowed', False)
    
      
        description = api_response.get('description', {}).get('text', "N/A")
    
        
        employment_type = api_response.get('employmentType', "N/A")
        seniority_level = api_response.get('seniorityLevel', "N/A")
    

        job_functions = [func['name'] for func in api_response.get('jobFunctions', [])]
        industries = [industry['name'] for industry in api_response.get('industries', [])]
    
    
        technical_skills = [skill['name'] for skill in api_response.get('technicalSkills', [])]
        other_skills = [skill['name'] for skill in api_response.get('otherSkills', [])]
        soft_skills = [skill['name'] for skill in api_response.get('softSkills', [])]
    
       
        job_url = "N/A"
        apply_method = api_response.get('applyMethod', {})
        if isinstance(apply_method, dict):
            for key, value in apply_method.items():
                if isinstance(value, dict) and 'companyApplyUrl' in value:
                    job_url = value['companyApplyUrl']
                    break
    

        job_details = {
            'job_title': title,
            'company': company_name,
            'location': location,
            'job_details': {
                'employment_type': employment_type,
                'seniority_level': seniority_level,
                'job_functions': job_functions,
                'industries': industries,
                'remote_work_allowed': remote_work_allowed,
                'job_description': {
                    'description': description
                },
                'job_url': job_url
            },
            'company_details': {
                'company_name': company_name,
                'company_url': company_url
            },
            'skills': {
                'technical_skills': technical_skills,
                'other_skills': other_skills,
                'soft_skills': soft_skills
            }
        }
    
        return job_details



    

    def process_job_data(job_data_list):
        results2 = []
        for job_data in job_data_list:
            try:
                job_details = extract_job_details(job_data)
                results2.append(job_details)
                print(f"Processed job: {job_details['job_title']}")
            except Exception as e:
                print(f"Error processing job data: {e}")
        return results2
    
    job_details = process_job_data(job_datas)

    df = pd.DataFrame(job_details)

    for i in range(len(df)):
        df.loc[i, 'link'] = job_links[i]
        df.loc[i, 'skills_required'] = ', '.join(skills_required[i])  
    print(df)

    file_name1 = keywords+location_name+'.1csv'
    df.to_csv(file_name1)   

    return df


#if __name__ == "__main__":
#    keywords = "AI Scientist"
#    location_name = "South Africa"
#    file_path = "C:\\Users\\kisha\\Documents\\job_genie\\Kishan Tripathi Resume.docx"
#    resultx = get_job_recommendations(keywords, location_name, file_path)
#    print(resultx)
#    resultx.to_csv(keywords+location_name+"1.csv")