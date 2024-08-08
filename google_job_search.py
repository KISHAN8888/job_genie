# update this if you forgot what to do then use your memory
import requests
from resume_processor import process_resume
import re
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
from serpapi import GoogleSearch
import json
import pandas as pd
import nltk


API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
API_TOKEN = "your hf token" 
headers = {"Authorization": f"Bearer {API_TOKEN}"}
api_key = "your gemini api key"

nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)




def fetch_job_results(params):
    search = GoogleSearch(params)
    results = search.get_dict()
    return results


def get_job_listings(params,results):



    all_job_results = []
    all_job_results.extend(results.get('jobs_results', []))


    while 'next_page_token' in results:
        params['start'] = results['next_page_token']
        results = fetch_job_results(params)
        all_job_results.extend(results.get('jobs_results', []))

    print(all_job_results)
    return all_job_results


def get_job_details(job_results):
    job_details = []
    for job in job_results:
        job_info = {
            'title': job.get('title'),
            'company': job.get('company_name'),
            'job_link': job.get('job_link', 'Link not provided'),
            'job_description': job.get('description'),
            'job_id': job.get('job_id', 'ID not provided'),
            'related_links': job.get('related_links', [])
        }
        job_details.append(job_info)
    return job_details


def extract_skills(job_description):
    tech_skills = set([
    'python', 'java', 'c++', 'javascript', 'sql', 'nosql', 'aws', 'azure', 'gcp',
    'docker', 'kubernetes', 'machine learning', 'deep learning', 'ai', 'data science',
    'data analysis', 'data engineering', 'big data', 'hadoop', 'spark', 'tableau',
    'power bi', 'excel', 'r', 'scala', 'git', 'devops', 'ci/cd', 'agile', 'scrum',
    'rest api', 'microservices', 'cloud computing', 'database', 'networking',
    'security', 'linux', 'windows', 'mac os', 'ios', 'android', 'react', 'angular',
    'vue', 'node.js', 'express', 'django', 'flask', 'spring', 'hibernate', 'orm',
    'api', 'json', 'xml', 'html', 'css', 'sass', 'less', 'webpack', 'babel',
    'typescript', 'redux', 'graphql', 'rest', 'soap', 'mvc', 'mvvm', 'tdd', 'cicd',
    'jenkins', 'travis ci', 'circle ci', 'terraform', 'ansible', 'puppet', 'chef',
    'mongodb', 'postgresql', 'mysql', 'oracle', 'ms sql server', 'redis', 'elasticsearch',
    'kafka', 'rabbitmq', 'activemq', 'tcp/ip', 'http', 'https', 'ssl/tls', 'oauth',
    'saml', 'ldap', 'active directory', 'unix', 'shell scripting', 'powershell', 'bash',
    'perl', 'ruby', 'go', 'rust', 'kotlin', 'swift', 'objective-c', 'xamarin',
    'react native', 'flutter', 'unity', 'unreal engine', 'photoshop', 'illustrator',
    'indesign', 'sketch', 'figma', 'invision', 'zeplin', 'jira', 'confluence', 'trello',
    'asana', 'slack', 'microsoft teams', 'zoom', 'webex', 'kanban', 'lean', 'six sigma',
    'prince2', 'pmp', 'itil', 'cobit', 'togaf', 'uml', 'erd', 'data modeling', 'etl',
    'olap', 'oltp', 'data warehouse', 'data lake', 'business intelligence',
    'data visualization', 'predictive analytics', 'statistical analysis', 'a/b testing',
    'seo', 'sem', 'google analytics', 'digital marketing', 'content management', 'crm',
    'erp', 'sap', 'salesforce', 'dynamics 365', 'workday', 'netsuite', 'blockchain',
    'cryptocurrency', 'iot', 'augmented reality', 'virtual reality', 'computer vision',
    'natural language processing', 'reinforcement learning', 'generative ai',
    'cybersecurity', 'penetration testing', 'ethical hacking', 'cryptography', '5g',
    'wifi', 'bluetooth', 'rfid', 'nfc', 'quantum computing', 'fpga', 'embedded systems',
    'robotics', 'plc', 'scada', 'can bus', 'modbus', 'cloud architecture', 'lambda',
    'cloudformation', 'docker swarm', 'helm', 'prometheus', 'grafana', 'elk stack',
    'logstash', 'graylog', 'splunk', 'new relic', 'datadog', 'opentracing', 'openmetrics',
    'loggly', 'sumologic', 'appdynamics', 'dynatrace', 'servicenow', 'incident management',
    'chaos engineering', 'site reliability engineering', 'bluemix', 'openshift', 'cloud foundry',
    'cloudbees', 'spinnaker', 'terraform cloud', 'packer', 'vault', 'consul', 'nomad',
    'vagrant', 'artifactory', 'nexus', 'sonarQube', 'veracode', 'snyk', 'blackduck', 'twistlock',
    'aqua', 'anchore', 'clair', 'trivy', 'aws lambda', 'aws ec2', 'aws s3', 'aws rds',
    'aws dynamodb', 'aws sagemaker', 'aws emr', 'azure functions', 'azure devops',
    'azure active directory', 'azure sql database', 'azure cosmos db', 'gcp functions',
    'gcp bigquery', 'gcp datastore', 'gcp pubsub', 'gcp firestore', 'gcp cloud run',
    'cloud storage', 'cloud sql', 'cloud spanner', 'bigtable', 'dataflow', 'dataproc',
    'firestore', 'pubsub', 'composer', 'cloud endpoints', 'cloud iam', 'cloud kms',
    'cloud scheduler', 'cloud tasks', 'cloud vision', 'cloud speech', 'cloud translate',
    'autoML', 'vertex ai', 'vertex pipelines', 'airflow', 'kubeflow', 'mlflow',
    'h2o.ai', 'datarobot', 'aws cloudtrail', 'aws config', 'aws guardduty', 'aws inspector',
    'aws security hub', 'aws shield', 'aws wafv2', 'aws sso', 'aws secrets manager',
    'azure security center', 'azure sentinel', 'azure policy', 'azure blueprints',
    'gcp security command center', 'gcp cloud security scanner', 'gcp vpc service controls',
    'gcp identity-aware proxy', 'gcp security key management', 'gcp confidential computing',
    'network security', 'application security', 'endpoint security', 'data security',
    'identity and access management', 'incident response', 'threat hunting',
    'vulnerability management', 'cyber threat intelligence', 'forensic analysis',
    'compliance and regulation', 'gdpr', 'ccpa', 'pci dss', 'hipaa', 'soc 2', 'iso 27001',
    'nist', 'csf', 'dfars', 'fedramp', 'cloud security', 'devsecops', 'zero trust architecture',
    'sase', 'sd-wan', 'vpn', 'firewall', 'ids/ips', 'siem', 'soar', 'xdr', 'cspm',
    'cdp', 'msp', 'mdm', 'uem', 'pam', 'waf', 'dos/ddos protection', 'network segmentation',
    'microsegmentation', 'end-to-end encryption', 'homomorphic encryption',
    'post-quantum cryptography', 'threat modeling', 'attack surface management',
    'red teaming', 'blue teaming', 'purple teaming', 'bug bounty', 'ethical hacking',
    'penetration testing', 'offensive security', 'defensive security', 'reverse engineering',
    'malware analysis', 'exploit development', 'incident response', 'digital forensics',
    'root cause analysis', 'threat hunting', 'security operations', 'security monitoring',
    'security analytics', 'security architecture', 'security engineering', 'security automation',
    'security orchestration', 'security testing', 'security auditing', 'security training',
    'awareness training', 'phishing simulation', 'cyber hygiene', 'security metrics',
    'security reporting', 'security compliance', 'security governance', 'security risk management',
    'business continuity', 'disaster recovery', 'crisis management', 'incident management',
    'data loss prevention', 'identity governance', 'threat intelligence platforms',
    'threat hunting platforms', 'security data lakes', 'security data fabric', 'security data mesh',
    'observability', 'monitoring', 'logging', 'tracing', 'alerting', 'cloud cost management',
    'finops', 'cloud billing', 'cloud cost optimization', 'cloud cost monitoring', 'cost explorer',
    'cloud cost governance', 'cloud cost allocation', 'cloud cost control', 'cloud cost transparency',
    'cloud cost visualization', 'cloud cost benchmarking', 'cloud cost forecasting', 'cloud cost savings',
    'cloud cost efficiency', 'cloud cost management tools', 'cloud cost management best practices',
    'cloud cost management strategies'])

    job_description = job_description.lower()
    job_description = re.sub(r'[^\w\s]', '', job_description)

    # Tokenize the job description
    tokens = nltk.word_tokenize(job_description)

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]

   
    single_word_skills = set(tokens) & tech_skills


    vectorizer = CountVectorizer(vocabulary=tech_skills, ngram_range=(2,3))
    multi_word_skills = vectorizer.fit_transform([job_description]).nonzero()[1]
    multi_word_skills = [vectorizer.get_feature_names_out()[i] for i in multi_word_skills]

    # Combine single-word and multi-word skills
    extracted_skills = list(single_word_skills) + multi_word_skills

    return extracted_skills
  

def extract_skills_from_descriptions(description_list):
    skills_list = []
    for description in description_list:
        skills = extract_skills(description)
        skills_list.append(skills)
    return skills_list


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()
   

def calculate_job_match(row,user_skills_text):
    
    job_text = row['title']
    if isinstance(row['extracted_skills'], str) and row['extracted_skills'] != '[]':
        job_text += " " + row['extracted_skills']
    
    # calculate similarity
    payload = {
        "inputs": {
            "source_sentence": user_skills_text,
            "sentences": [job_text]
        }
    }
    result = query(payload)
    
    # The API returns a list of similarities, we only sent one job so we take the first (and only) result
    return result[0] if isinstance(result, list) and len(result) > 0 else 0

def get_job_details2(job_id):
    params = {
    "api_key": "aa52dda07aca37c1537058311ddea2dedf13c06a954dc05af4aa866a66a61b28",
    "engine": "google_jobs_listing",
    "q": job_id
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    return results


def get_job2(job_ids2):
    job_datas2 = []
    for job_id in job_ids2:
        job_data = get_job_details2(job_id)
        job_datas2.append(job_data)
        
        print(f"Iteration {len(job_datas2)}: job_id={job_id}, job_data={job_data}")

    

    return job_datas2
  

def extract_job_details2(api_response):
    # extract job title
    title = api_response.get('search_parameters', {}).get('q', '')
  
    
    apply_link = None
    if 'apply_options' in api_response and api_response['apply_options']:
        first_option = api_response['apply_options'][0]
        
        apply_link = first_option['link']
    
    
    location = "Not specified"
    
    description = None
    
    salaries = api_response.get('salaries', [])
    salary_info = []
    for salary in salaries:
        salary_info.append({
            'job_title': salary.get('job_title'),
            'salary_from': salary.get('salary_from'),
            'salary_to': salary.get('salary_to'),
            'salary_period': salary.get('salary_period'),
            'source': salary.get('source')
        })
    

    apply_options = [{'title': option['title'], 'link': option['link']} 
                     for option in api_response.get('apply_options', [])]
    
    # extract company ratings
    ratings = [{'source': rating['source'], 'rating': rating['rating'], 'reviews': rating['reviews']} 
               for rating in api_response.get('ratings', [])]
    
    # prepare job details object
    job_details = {
        'job_title': title,
        
        'location': location,
        'job_description': description,
        'apply_link': apply_link,  # Added apply link here
        'salary_info': salary_info,
        'apply_options': apply_options,
        'company_ratings': ratings
    }
    
    return job_details
  
def process_job_data2(job_data_list):
    results2 = []
    for job_data in job_data_list:
        job_details = extract_job_details2(job_data)
        results2.append(job_details)
        print(f"Iteration {len(results2)}: job_details={job_details}")
    print(results2)    
    return results2
    

def get_job_recommendations2(job_role, location,file_path):

    
    skills2, roles = process_resume(api_key, file_path)
    user_skills = [skill.strip() for skill in skills2.split(',')]
    # get initial job listings
    params = {
    "api_key": "your google jobs api key",
    "engine": "google_jobs",
    "google_domain": "google.com",
    "q": job_role,
    "gl": "in",
    "num": "60",
    "location": "India",
    "country": "India"
    }

    results = fetch_job_results(params)
    all_job_results = get_job_listings(params,results)
    print(all_job_results)
    
  
    final_results = get_job_details(all_job_results)
    
    print(final_results)
    
  
    description_list = [job['job_description'] for job in final_results]
    
 
    skills_list = extract_skills_from_descriptions(description_list)
    
    # add extracted skills to final_results
    for i, skills in enumerate(skills_list):
        if i < len(final_results):
            final_results[i]['extracted_skills'] = skills
    
    # create DataFrame from final_results
    job_data2 = pd.DataFrame(final_results)
    
    # calculate match scores
    
    user_skills_text = ", ".join(user_skills)
    job_data2['match_score'] = job_data2.apply(lambda row: calculate_job_match(row,user_skills_text), axis=1)
    
    # sort and get top jobs
    top_jobs = job_data2.sort_values('match_score', ascending=False).head(5)
    
    # get detailed job information
    job_ids2 = top_jobs['job_id'].tolist()
    company_name = top_jobs['company'].tolist()
    
    job_datas2 = get_job2(job_ids2)
    job_details2 = process_job_data2(job_datas2)
    
    # creating final DataFrame
    df2 = pd.DataFrame(job_details2)
    for i in range(len(df2)):
        df2.loc[i, 'company'] = company_name[i]

    file_name1 = job_role+location+'.2csv'
    df2.to_csv(file_name1)  
    
    return df2

#job_role = "AI Scientist"
#location = "Bangalore"
#file_path = "C:\\Users\\kisha\\Documents\\job_genie\\Kishan Tripathi Resume.docx"
#result_df2 = get_job_recommendations2(job_role, location, file_path)
#print(result_df2)
#result_df2.to_csv('job_details1.3.csv')