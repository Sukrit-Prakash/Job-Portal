import scrapy
import json
import os

class NaukriSpider(scrapy.Spider):
    name = "naukri"
    allowed_domains = ["naukri.com"]
    start_urls = ["https://www.naukri.com/software-engineer-jobs"]  # Direct job listings page

    jobs_list = []  # List to store job data

    def parse(self, response):
        job_cards = response.css(".jobTuple.bgWhite.br4.mb-8")  # Corrected selector

        for job in job_cards:
            title = job.css(".title.fw500 a::text").get(default="").strip()
            company = job.css(".comp-name::text").get(default="").strip()
            location = job.css(".locWdth span::text").get(default="").strip()
            link = job.css(".title.fw500 a::attr(href)").get(default="")

            if title and company and link:
                self.jobs_list.append({
                    "source": "Naukri",
                    "title": title,
                    "company": company,
                    "location": location,
                    "link": link
                })

        # Pagination: Follow "Next" page link
        next_page = response.css("a[title='Next']::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def closed(self, reason):
        """Save all scraped jobs to a JSON file when spider closes"""
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)  # Ensure output directory exists

        with open(f"{output_dir}/naukri_jobs.json", "w", encoding="utf-8") as f:
            json.dump(self.jobs_list, f, indent=4, ensure_ascii=False)

        self.log(f"Saved {len(self.jobs_list)} jobs to {output_dir}/naukri_jobs.json")
