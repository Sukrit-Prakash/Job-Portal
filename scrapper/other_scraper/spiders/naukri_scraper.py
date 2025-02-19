import scrapy
import pymongo

class NaukriSpider(scrapy.Spider):
    name = "naukri"
    allowed_domains = ["naukri.com"]
    start_urls = ["https://www.naukri.com/software-engineer-jobs"]

    def __init__(self):
        # Connect to MongoDB
        # mongodb+srv://sukritprakash2020:Vkhi2fx6WMnu7N8L@cluster0.ztwxu.mongodb.net/
        # Vkhi2fx6WMnu7N8L
        # sukritprakash2020
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")  # Update with your DB URL if needed
        self.db = self.client["job_scraper_db"]  # Database name
        self.collection = self.db["naukri_jobs"]  # Collection name

    def parse(self, response):
        job_cards = response.css(".jobTuple.bgWhite.br4.mb-8")

        for job in job_cards:
            title = job.css(".title.fw500 a::text").get(default="").strip()
            company = job.css(".comp-name::text").get(default="").strip()
            location = job.css(".locWdth span::text").get(default="").strip()
            link = job.css(".title.fw500 a::attr(href)").get(default="")

            if title and company and link:
                job_data = {
                    "source": "Naukri",
                    "title": title,
                    "company": company,
                    "location": location,
                    "link": link
                }
                self.collection.insert_one(job_data)  # Save to MongoDB

        # Pagination: Follow the "Next" page
        next_page = response.css("a[title='Next']::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def closed(self, reason):
        self.client.close()  # Close MongoDB connection when spider stops
