import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import json
# currently the indeed and naukri is not  working
class JobScraper(scrapy.Spider):
    name = "job_scraper"
    start_urls = [
        "https://weworkremotely.com/",
        # "https://www.naukri.com/",
        # "https://www.indeed.com/"
    ]
    
    def __init__(self):
    #     chrome_options = Options()
    #     chrome_options.add_argument("--headless")
    #     chrome_options.add_argument("--disable-gpu")
    #     chrome_options.add_argument("--no-sandbox")
    #     chrome_options.add_argument("--disable-dev-shm-usage")
        
    #     self.driver = webdriver.Chrome(service=Service(), options=chrome_options)
        self.jobs = []
    
    def parse(self, response):
        if "weworkremotely" in response.url:
            self.parse_weworkremotely(response)
        # elif "naukri" in response.url:
        #     self.parse_naukri()
        # elif "indeed" in response.url:
        #     self.parse_indeed()
        
        with open("output/jobs.json", "w") as f:
            json.dump(self.jobs, f, indent=4)
        #     def save_jobs(self, jobs):
        # with open("output/jobs.json", "a") as f:
        #     json.dump(jobs, f, indent=4)
    
    def parse_weworkremotely(self, response):
        job_posts = response.css("section.jobs li")
        for job in job_posts:
            title = job.css("span.title::text").get()
            company = job.css("span.company::text").get()
            link = response.urljoin(job.css("a::attr(href)").get())
            
            self.jobs.append({
                "source": "We Work Remotely",
                "title": title,
                "company": company,
                "link": link
            })
    
    # def parse_naukri(self):
    #     self.driver.get("https://www.naukri.com/")
    #     time.sleep(5)
    #     job_cards = self.driver.find_elements(By.CLASS_NAME, "jobTuple")
        
    #     for job in job_cards:
    #         try:
    #             title = job.find_element(By.CLASS_NAME, "title").text
    #             company = job.find_element(By.CLASS_NAME, "company").text
    #             link = job.find_element(By.TAG_NAME, "a").get_attribute("href")
                
    #             self.jobs.append({
    #                 "source": "Naukri",
    #                 "title": title,
    #                 "company": company,
    #                 "link": link
    #             })
    #         except:
    #             continue
    
    # def parse_indeed(self):
    #     self.driver.get("https://www.indeed.com/")
    #     time.sleep(5)
    #     job_cards = self.driver.find_elements(By.CLASS_NAME, "job_seen_beacon")
        
    #     for job in job_cards:
    #         try:
    #             title = job.find_element(By.CLASS_NAME, "jobTitle").text
    #             company = job.find_element(By.CLASS_NAME, "companyName").text
    #             link = job.find_element(By.TAG_NAME, "a").get_attribute("href")
                
    #             self.jobs.append({
    #                 "source": "Indeed",
    #                 "title": title,
    #                 "company": company,
    #                 "link": link
    #             })
    #         except:
    #             continue
    
    # def closed(self, reason):
    #     self.driver.quit()
