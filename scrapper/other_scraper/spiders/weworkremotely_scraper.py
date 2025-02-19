import scrapy
from datetime import datetime
from pymongo import MongoClient
import dotenv
import os
class WeWorkRemotelySpider(scrapy.Spider):
    name = "weworkremotely"
    start_urls = ["https://weworkremotely.com/"]
    
    # MongoDB connection setup
    # mongo_uri = "mongodb+srv://sukritprakash2020:<Password>@cluster0.ztwxu.mongodb.net/"
    dotenv.load_dotenv()
    mongo_uri = os.getenv("MONGO_URI")
    
    mongo_db = "weworkremotely"
    mongo_collection = "jobs"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.mongo_collection]
    
    def parse(self, response):
        job_posts = response.css("section.jobs li")
# <h4 class="new-listing__header__title"> Senior UX/UI Designer </h4>
        for job in job_posts:
            title = job.css("h4.new-listing__header__title::text").get(default="").strip()
            company = job.css("p.new-listing__company-name::text").get(default="").strip()
            location = "Remote"  # We Work Remotely only posts remote jobs
            description = "Job description not available on listing page."
            posted_date = job.css("p.new-listing__header__icons__date::text").get(default="").strip()
            url = response.urljoin(job.css("a::attr(href)").get())
            tags = job.css("p.new-listing__categories__category::text").getall()
            job_type = "Remote"
            salary = job.css("p.new-listing__categories__category::text").get(default="Not specified").strip()
            skills = []  # WeWorkRemotely does not list skills directly
            
            item = {
                "title": title,
                "company": company,
                "location": location,
                "description": description,
                "posted_date": posted_date,
                "url": url,
                "tags": tags,
                "job_type": job_type,
                "salary": salary,
                "skills": skills,
                "scraped_at": datetime.utcnow()
            }
            
            # Save to MongoDB
            self.collection.insert_one(item)
            yield item
        
        # Follow pagination for more jobs
        next_page = response.css('a[rel="next"]::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def closed(self, reason):
        self.client.close()
        self.logger.info("MongoDB connection closed.")



# -----------------USE THIS CODE TO SCRAPE JOBS FROM WEWORKREMOTELY.COM AND SAVE IT TO LOCAL STORAGE-----------------
# import scrapy
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# import time
# import json
# # currently the indeed and naukri is not  working
# class JobScraper(scrapy.Spider):
#     name = "job_scraper"
#     start_urls = [
#         "https://weworkremotely.com/"
#     ]
    
#     def __init__(self):

        

#         self.jobs = []
    
#     def parse(self, response):
#         if "weworkremotely" in response.url:
#             self.parse_weworkremotely(response)
        
#         with open("output/weworkremotely.json", "w") as f:
#             json.dump(self.jobs, f, indent=4)

    
#     def parse_weworkremotely(self, response):
#         job_posts = response.css("section.jobs li")
#         for job in job_posts:
#             title = job.css("span.title::text").get()
#             company = job.css("span.company::text").get()
#             link = response.urljoin(job.css("a::attr(href)").get())
            
#             self.jobs.append({
#                 "source": "We Work Remotely",
#                 "title": title,
#                 "company": company,
#                 "link": link
#             })
    