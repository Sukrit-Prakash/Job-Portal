import json
import scrapy
from datetime import datetime, timedelta
from pymongo import MongoClient
# import dotenv
import os
import dotenv
class InternshalaSpider(scrapy.Spider):
    name = 'internshala'
    start_urls = [
        'https://internshala.com/jobs/',       # First page (Jobs)
        'https://internshala.com/internships/' # Second page (Internships)
    ]
    

    # mongo_uri = "mongodb+srv://sukritprakash2020:<Password>@cluster0.ztwxu.mongodb.net/"

    dotenv.load_dotenv()
    mongo_uri = os.getenv("MONGO_URI") 
    mongo_db = "internshala"
    mongo_collection = "jobs"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.mongo_collection]

        # self.mongo_uri = os.getenv("MONGO_URI") 
    
    def parse(self, response):
        jobs = response.css("#internship_list_container_1 .container-fluid.individual_internship")
        
        for job in jobs:
            title = job.css("h3.job-internship-name a::text").get(default="").strip()
            company = job.css(".company-name::text").get(default="").strip()
            location = job.css("div.row-1-item.locations a::text").getall()
            description = job.css("div.job-profile div.text-container *::text").getall()
            description = " ".join([text.strip() for text in description if text.strip()])
            posted_time = job.css("div.status-inactive span::text, div.status-success span::text").get(default="").strip()
            job_type = job.css("div.job-type::text").get(default="").strip()
            tags = job.css("div.tags a::text").getall()
            skills = job.css("div.skills a::text").getall()
            salary = job.css("div.row-1-item:nth-child(3) span::text").get(default="").strip()
            url = response.urljoin(job.css("h3.job-internship-name a::attr(href)").get())
            
            # Convert posted_time to a proper date format (assumed format: 'X days ago')
            posted_date = self.parse_posted_date(posted_time)
            
            item = {
                "title": title,
                "company": company,
                "location": location,
                "description": description,
                "posted_date": posted_date,
                "url": url,
                "tags": tags,
                "job_type": job_type if job_type in ["Full Time", "Part Time", "Internship", "Contract", "Remote", "Freelance"] else "Internship",
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
        # with open("output/internshala.json", "w",encoding="utf-8") as f:
        #   json.dump(self.custom_items, f, ensure_ascii=False, indent=4)
        # self.logger.info(f"Scrape complete. Data written ")
        self.client.close()
        self.logger.info("MongoDB connection closed.")
    
    def parse_posted_date(self, posted_time):
        """Converts posted_time text into a proper date format."""
        if "day" in posted_time:
            days_ago = int(posted_time.split()[0])
            return (datetime.today() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
        return datetime.today().strftime('%Y-%m-%d')



#   -----------------------------------------------------------
#   USE THIS CODE FOR SCRAPING AND SAVING DATA TO JSON FILE LOCALLY IN OUTPUT FOLDER
# GOOD FOR TESTING AND DEBUGGING
# import json
# import scrapy
# from datetime import datetime, timedelta

# class InternshalaSpider(scrapy.Spider):
#     name = 'internshala'
#     start_urls = [
#         'https://internshala.com/jobs/',       # First page (Jobs)
#         'https://internshala.com/internships/' # Second page (Internships)
#     ]
    
#     # List to collect scraped items
#     custom_items = []

#     def parse(self, response):
#         jobs = response.css("#internship_list_container_1 .container-fluid.individual_internship")
        
#         for job in jobs:
#             title = job.css("h3.job-internship-name a::text").get(default="").strip()
#             company = job.css(".company-name::text").get(default="").strip()
#             location = job.css("div.row-1-item.locations a::text").getall()
#             description = job.css("div.job-profile div.text-container *::text").getall()
#             description = " ".join([text.strip() for text in description if text.strip()])
#             posted_time = job.css("div.status-inactive span::text, div.status-success span::text").get(default="").strip()
#             job_type = job.css("div.job-type::text").get(default="").strip()
#             tags = job.css("div.tags a::text").getall()
#             skills = job.css("div.skills a::text").getall()
#             salary = job.css("div.row-1-item:nth-child(3) span::text").get(default="").strip()
#             url = response.urljoin(job.css("h3.job-internship-name a::attr(href)").get())
            
#             # Convert posted_time to a proper date format (assumed format: 'X days ago')
#             posted_date = self.parse_posted_date(posted_time)
            
#             item = {
#                 "title": title,
#                 "company": company,
#                 "location": location,
#                 "description": description,
#                 "posted_date": posted_date,
#                 "url": url,
#                 "tags": tags,
#                 "job_type": job_type if job_type in ["Full Time", "Part Time", "Internship", "Contract", "Remote", "Freelance"] else "Internship",
#                 "salary": salary,
#                 "skills": skills,
#             }
#             self.custom_items.append(item)
#             yield item

#         # Follow pagination for more jobs
#         next_page = response.css('a[rel="next"]::attr(href)').get()
#         if next_page:
#             yield response.follow(next_page, callback=self.parse)

#     def closed(self, reason):
#         # When the spider finishes, write all collected items to a JSON file.
#         # filename = "internshala_output.json"
         
#         with open("output/internshala.json", "w",encoding="utf-8") as f:
#             json.dump(self.custom_items, f, ensure_ascii=False, indent=4)
#         self.logger.info(f"Scrape complete. Data written ")
#         # with open(filename, "w", encoding="utf-8") as f:
#         #     json.dump(self.custom_items, f, ensure_ascii=False, indent=4)
#         # self.logger.info(f"Scrape complete. Data written ")
    
#     def parse_posted_date(self, posted_time):
#         """Converts posted_time text into a proper date format."""
#         if "day" in posted_time:
#             days_ago = int(posted_time.split()[0])
#             return (datetime.today() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
#         return datetime.today().strftime('%Y-%m-%d')
