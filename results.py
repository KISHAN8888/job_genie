#df_selected = df.iloc[:3]  # First 3 rows of df
#df2_selected = df2.iloc[:2]  # First 2 rows of df2
#
#df_1= df_selected.to_string()
#df_2= df2_selected.to_string()
#print(df_1)
#print(df_2)


# this has to be updated as the api response format has been changed

import pandas as pd
def get_result(df_1,df_2):
        
    
    df = df_1
    
    # generate html
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Job Listings</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }
            .container {
                width: 80%;
                margin: 20px auto;
                background-color: #fff;
                padding: 20px;
                border-radius: 5px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            .job {
                border-bottom: 1px solid #ccc;
                padding: 10px 0;
            }
            .job:last-child {
                border-bottom: none;
            }
            .job h2 {
                color: #333;
            }
            .job p {
                margin: 5px 0;
            }
            .job a {
                color: #0066cc;
                text-decoration: none;
            }
            .job a:hover {
                text-decoration: underline;
            }
            .skills, .details {
                margin: 10px 0;
            }
            .skills span, .details span {
                background-color: #e0e0e0;
                padding: 5px;
                border-radius: 3px;
                margin-right: 5px;
                display: inline-block;
            }
        </style>
    </head>
    <body>
    
    <div class="container">
    """
    
    for _, row in df.iterrows():
        html_content += f"""
        <div class="job">
            <h2>{row['job_title']} at {row['company']}</h2>
            <p><strong>Location:</strong> {row['location']}</p>
            <p><strong>Company:</strong> <a href="{row['company']}" target="_blank">{row['company']}</a></p>
            <p><strong>Job Link:</strong> <a href={row['link']} target="_blank">View Job</a></p>
            
            <div class="details">
                <strong>Job Description:</strong>
                <p>{row['job_description']}</p>
            </div>
        </div>
        """
    
    html_content += """
    </div>
    
    </body>
    </html>
    """
    
 
    with open('job_listings.html', 'w', encoding='utf-8') as file:
        file.write(html_content)
    
    print("HTML file generated successfully.")
    