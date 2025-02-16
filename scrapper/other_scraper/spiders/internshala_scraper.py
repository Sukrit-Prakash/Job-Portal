import scrapy
import json
import os

class InternshalaSpider(scrapy.Spider):
    name = "internshala"
    allowed_domains = ["internshala.com"]
    start_urls = ["https://internshala.com/internships"]

    jobs_list = []  # List to store job data

    def parse(self, response):
        jobs = response.css(".internship_meta")

        for job in jobs:
            job_data = {
                "title": job.css(".profile a::text").get(default="N/A").strip(),
                "company": job.css(".company_name a::text").get(default="N/A").strip(),
                "location": job.css(".location_link::text").get(default="N/A").strip(),
                "stipend": job.css(".stipend span::text").get(default="N/A").strip(),
                "duration": job.css(".item_body div::text").get(default="N/A").strip(),
                "apply_link": response.urljoin(job.css(".view_detail_button::attr(href)").get(default="")),
            }
            self.jobs_list.append(job_data)

        # Handle Pagination (Next Page)
        next_page = response.css("ul.pagination li:last-child a::attr(href)").get()
        if next_page and "internships" in next_page:
            yield response.follow(next_page, callback=self.parse)

    def closed(self, reason):
        """Save all scraped jobs to a JSON file when spider closes"""
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)  # Ensure output directory exists

        with open(f"{output_dir}/internshala_jobs.json", "w", encoding="utf-8") as f:
            json.dump(self.jobs_list, f, indent=4, ensure_ascii=False)

        self.log(f"Saved {len(self.jobs_list)} jobs to {output_dir}/internshala_jobs.json")
