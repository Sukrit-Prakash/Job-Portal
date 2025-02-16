import scrapy
import json

class IndeedSpider(scrapy.Spider):
    name = "indeed"
    start_urls = ["https://www.indeed.com/"]

    def parse(self, response):
        jobs = []
        job_cards = response.css(".job_seen_beacon")

        for job in job_cards:
            title = job.css(".jobTitle::text").get()
            company = job.css(".companyName::text").get()
            link = response.urljoin(job.css("a::attr(href)").get())

            if title and company and link:
                jobs.append({
                    "source": "Indeed",
                    "title": title.strip(),
                    "company": company.strip(),
                    "link": link
                })
        
        self.save_jobs(jobs)

    def save_jobs(self, jobs):
        with open("output/jobs.json", "a") as f:
            json.dump(jobs, f, indent=4)
