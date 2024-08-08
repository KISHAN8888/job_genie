from resume_processor import process_resume
from linkedin_job_search import get_job_recommendations
from google_job_search import get_job_recommendations2
from results import get_result


def main():
    print("Welcome to the Job Search and Matching Application!")

    job_role = "AI Scientist"
    location = "India"
    file_path = "C:\\Users\\kisha\\Documents\\job_genie\\Kishan Tripathi Resume.docx"

    # Get resume path
    #file_path = input("Please enter the path to your resume file: ")

    ## Get job role
    #job_role = input("Enter the job role you're interested in: ")

    ## Get location
    #location = input("Enter the location for job search: ")

    print("\nProcessing your resume and searching for jobs. This may take a moment...\n")

    try:
        # process resume
        
        api_key = "AIzaSyBgXXTa043ZpKYxIYfGOQ6P91fBD6Bkfxk"

        skills, roles = process_resume(api_key,file_path)

        print("Extracted skills from your resume:")
        print(", ".join(skills))
        print("\nSuggested roles based on your resume:")
        print(", ".join(roles))

        # search jobs on LinkedIn
        result_df1 = get_job_recommendations(job_role, location, file_path)
        print("phase 1 completed")
        
        # search for jobs on google jobs
        result_df2 = get_job_recommendations2(job_role, location, file_path)
        print("phase 2 completed")

        result = get_result(result_df1, result_df2)

        print(result)
        print("I am done now go and apply remember you are still unemployed!!")

       



    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Please make sure you've entered the correct resume path and try again.")

if __name__ == "__main__":
    main()