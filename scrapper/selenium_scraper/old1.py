import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle
import time

# Set up Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--disable-webrtc")
options.add_argument("--log-level=3")
driver = webdriver.Chrome(options=options)

# Load LinkedIn homepage
driver.get("https://www.linkedin.com")

# Load saved cookies
cookies = pickle.load(open("linkedin_cookies.pkl", "rb"))
for cookie in cookies:
    driver.add_cookie(cookie)

# Refresh page to apply cookies
driver.refresh()
time.sleep(3)

# Navigate to LinkedIn Jobs page
driver.get("https://www.linkedin.com/jobs/search/?keywords=software%20developer")

# Wait for job listings to load
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "job-card-container"))
    )
except:
    print("Job listings did not load!")
    driver.quit()
    exit()

# Scroll down to load more jobs (repeat multiple times if needed)
for _ in range(6):  # Adjust number of scrolls if needed
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)  # Wait for new jobs to load

# Scrape job listings
job_elements = driver.find_elements(By.CLASS_NAME, "job-card-container")

# List to store scraped job data
job_list = []

for i in range(len(job_elements)):
    try:
        # Re-fetch job elements to avoid "stale element" error
        job_elements = driver.find_elements(By.CLASS_NAME, "job-card-container")
        job = job_elements[i]

        # Extract job title and link
        title_element = job.find_element(By.CSS_SELECTOR, "a.job-card-container__link")
        title = title_element.text
        link = title_element.get_attribute("href")

        # Extract company name
        company = job.find_element(By.CSS_SELECTOR, "div.artdeco-entity-lockup__subtitle").text

        # Extract job location
        try:
            location = job.find_element(By.CSS_SELECTOR, "li div.artdeco-entity-lockup__caption span").text
        except:
            location = "Location Not Found"

        # Extract salary (if available)
        try:
            salary = job.find_element(By.CSS_SELECTOR, "div.artdeco-entity-lockup__metadata ul li span").text
        except:
            salary = "Salary Not Mentioned"

        # Create a dictionary for the job data
        job_data = {
            "Title": title,
            "Company": company,
            "Location": location,
            "Salary": salary,
            "Link": link
        }

        # Append to job list
        job_list.append(job_data)

    except Exception as e:
        print(f"Error extracting job details: {e}")

# Save job list as a JSON file
with open("jobs.json", "w", encoding="utf-8") as json_file:
    json.dump(job_list, json_file, indent=4, ensure_ascii=False)

print("Scraped job data saved to jobs.json")

driver.quit()
