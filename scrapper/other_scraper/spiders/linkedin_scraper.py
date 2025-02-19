# import scrapy
# import time
# import pickle
# from datetime import datetime
# from pymongo import MongoClient
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# class LinkedInSpider(scrapy.Spider):
#     name = "linkedin"
#     # Dummy start URL; Selenium will handle the navigation
#     start_urls = ["https://www.linkedin.com/jobs/search/?keywords=software%20developer"]

#     # MongoDB connection setup

#     # mongo_uri = "mongodb+srv://sukritprakash2020:<Password>@cluster0.ztwxu.mongodb.net/"
#     mongo_db = "linkedin"
#     mongo_collection = "jobs"

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Initialize MongoDB connection
#         self.client = MongoClient(self.mongo_uri)
#         self.db = self.client[self.mongo_db]
#         self.collection = self.db[self.mongo_collection]
        
#         # Setup Selenium WebDriver
#         self.options = Options()
#         self.options.add_argument("--disable-webrtc")
#         self.options.add_argument("--log-level=3")
#         self.driver = webdriver.Chrome(options=self.options)
        
#         # Load saved cookies if available
#         try:
#             self.cookies = pickle.load(open("linkedin_cookies.pkl", "rb"))
#         except Exception as e:
#             self.logger.error("Could not load cookies: %s", e)
#             self.cookies = []

#     def parse(self, response):
#         driver = self.driver

#         # Load LinkedIn homepage
#         driver.get("https://www.linkedin.com")
#         # Add cookies (if any) to maintain session
#         if self.cookies:
#             for cookie in self.cookies:
#                 driver.add_cookie(cookie)
#         driver.refresh()
#         time.sleep(3)  # Wait for cookies to take effect

#         # Navigate to LinkedIn Jobs page
#         driver.get("https://www.linkedin.com/jobs/search/?keywords=software%20developer")

#         # Wait for job listings to load
#         try:
#             WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located((By.CLASS_NAME, "job-card-container"))
#             )
#         except Exception as e:
#             self.logger.error("Job listings did not load: %s", e)
#             driver.quit()
#             return

#         # Scroll down to load more jobs
#         for _ in range(6):  # Adjust number of scrolls if needed
#             driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#             time.sleep(3)

#         # Scrape job listings
#         job_elements = driver.find_elements(By.CLASS_NAME, "job-card-container")
#         self.logger.info("Found %d job postings.", len(job_elements))

#         for job in job_elements:
#             try:
#                 # Extract job title and link
#                 title_element = job.find_element(By.CSS_SELECTOR, "a.job-card-container__link")
#                 title = title_element.text.strip()
#                 link = title_element.get_attribute("href")
                
#                 # Extract company name
#                 company = job.find_element(By.CSS_SELECTOR, "p.artdeco-entity-lockup__subtitle").text.strip()
                
#                 # Extract job location
#                 try:
#                     location = job.find_element(By.CSS_SELECTOR, "li div.artdeco-entity-lockup__caption span").text.strip()
#                 except Exception:
#                     location = "Location Not Found"
                
#                 # Extract salary if available
#                 try:
#                     salary = job.find_element(By.CSS_SELECTOR, "div.artdeco-entity-lockup__metadata ul li span").text.strip()
#                 except Exception:
#                     salary = "Salary Not Mentioned"
                
#                 # Map data to new schema
#                 item = {
#                     "title": title,
#                     "company": company,
#                     "location": location,
#                     "description": "Job description not available on listing page.",
#                     # Using current date as posted_date; adjust if you can extract an actual date
#                     "posted_date": datetime.utcnow().strftime("%Y-%m-%d"),
#                     "url": link,
#                     "tags": [],
#                     # Defaulting to "Full Time"; adjust if you have job type info
#                     "job_type": "Full Time",
#                     "salary": salary,
#                     "skills": [],
#                     "scraped_at": datetime.utcnow()
#                 }
                
#                 # Save to MongoDB
#                 self.collection.insert_one(item)
#                 yield item

#             except Exception as e:
#                 self.logger.error("Error extracting job details: %s", e)

#     def closed(self, reason):
#         self.driver.quit()
#         self.client.close()
#         self.logger.info("Selenium driver and MongoDB connection closed.")
