import scrapy
from datetime import datetime
from pymongo import MongoClient
import dotenv
#  this is not working properly NEEDS TO BE FIXED
class IndeedSpider(scrapy.Spider):
    name = "indeed"
    start_urls = ["https://in.indeed.com/jobs?q=&l="]

    # MongoDB connection
    # mongo_uri = "mongodb+srv://sukritprakash2020:,Password>@cluster0.ztwxu.mongodb.net/"
    mongo_uri = dotenv.get("mongo_uri")

    mongo_db = "indeed"
    mongo_collection = "jobs"

    custom_settings = {
        "PLAYWRIGHT_BROWSER_TYPE": "chromium",
        "PLAYWRIGHT_LAUNCH_OPTIONS": {"headless": True},
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.mongo_collection]

    def start_requests(self):
        """Use Playwright to load Indeed pages"""
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, meta={"playwright": True})

    async def parse(self, response):
        job_posts = response.css("div.job_seen_beacon")

        for job in job_posts:
            title = job.css("h2.jobTitle span::text").get(default="").strip()
            company = job.css("span.companyName::text").get(default="").strip()
            location = job.css("div.companyLocation::text").get(default="").strip()
            description = "Job description not available on listing page."
            posted_date = job.css("span.date::text").get(default="").strip()
            url = response.urljoin(job.css("h2.jobTitle a::attr(href)").get())
            salary = job.css("div.metadata.salary-snippet-container div::text").get(default="Not specified").strip()
            tags = []
            job_type = ""
            skills = []

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

        # Follow pagination
        next_page = response.css('a[aria-label="Next"]::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse, meta={"playwright": True})

    def closed(self, reason):
        self.client.close()
        self.logger.info("MongoDB connection closed.")

