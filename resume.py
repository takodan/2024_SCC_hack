import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import google.generativeai as genai
import hidden
import json

# driver = webdriver.Chrome()
# driver.get("https://www.linkedin.com/login")

# time.sleep(2)

# username = driver.find_element(By.ID, "username")
# password = driver.find_element(By.ID, "password")

# username.send_keys(hidden.linkedin_email())
# password.send_keys(hidden.linkedin_password())

# time.sleep(2)

# page_url = "https://www.linkedin.com/jobs/view/4069963920/"
# for i in range(2):
#     driver.get(page_url)

#     time.sleep(5)

#     try:
#         # Extract job title
#         job_title = driver.find_element(By.CSS_SELECTOR, 'h1.top-card-layout__title').text

#         # Extract company name
#         company_name = driver.find_element(By.CSS_SELECTOR, 'a.topcard__org-name-link').text

#         # Extract job location
#         job_location = driver.find_element(By.CSS_SELECTOR, 'span.topcard__flavor--bullet').text

#         # Extract job description
#         see_more_button = driver.find_element(By.CSS_SELECTOR, 'button.show-more-less-html__button--more')
#         see_more_button.click()
#         job_description = see_more_button.text
#         time.sleep(2)

#         # Prepare the result string
#         result = (
#             f"Job Title: {job_title}\n"
#             f"Company: {company_name}\n"
#             f"Location: {job_location}\n"
#             f"\nJob Description:\n{job_description}\n"
#         )

#         # Save the result to a text file
#         with open("job_details.txt", "w", encoding="utf-8") as file:
#             file.write(result)

#         print("Job details saved to job_details.txt")

#     except Exception as e:
#         print("Error while extracting job details:", e)


GOOGLE_API_KEY = hidden.google_ai_api_key()

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel("gemini-1.5-pro")
resume_pdf = genai.upload_file("resume0923.pdf")
job_details = genai.upload_file("job_details_2.txt")

response_schema = {
    "type": "object",
    "properties": {
        "Job Title": {"type": "string"},
        "Company": {"type": "string"},
        "Location": {"type": "string"},
        "Candidate:": {"type": "string"},
        "Suitable or Not": {"type": "string"},
        "Meets Qualifications": {
            "type": "object",
            "properties": {
                "Programming Languages": {
                    "type": "array",
                    "items":{
                        "type": "string"
                    }
                },
                "Other skills": {
                    "type": "array",
                    "items":{
                        "type": "string"
                    }
                },
                "Academic/Job Experience": {
                    "type": "array",
                    "items":{
                        "type": "string"
                    }
                },
            }
        },
        "Not Meet Qualifications": {
            "type": "object",
            "properties": {
                "Programming Languages": {
                    "type": "array",
                    "items":{
                        "type": "string"
                    }
                },
                "Other skills": {
                    "type": "array",
                    "items":{
                        "type": "string"
                    }
                },
                "Academic/Job Experience": {
                    "type": "array",
                    "items":{
                        "type": "string"
                    }
                },
            }
        }
    }
}

prompt = """
    Please determine if the candidate is suitable for this position based on the job description and resume.
    Please list the items that meet and do not meet.
"""

result = model.generate_content(
    [prompt, resume_pdf, job_details],
    generation_config=genai.GenerationConfig(
        response_mime_type="application/json",
        response_schema=response_schema,
    )
)
json_object = json.loads(result.text)
# print(json_object)

with open(r"output\googleAI.txt", "w") as f:
    f.write(json.dumps(json_object, indent=4))

# input("Press Enter to close the browser...")