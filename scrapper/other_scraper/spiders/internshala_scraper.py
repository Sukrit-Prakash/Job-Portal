# import scrapy
# import json
# import os

# class InternshalaSpider(scrapy.Spider):
#     name = "internshala"
#     allowed_domains = ["internshala.com"]
#     start_urls = ["https://internshala.com/internships"]

#     jobs_list = []  # List to store job data

#     def parse(self, response):
#         jobs = response.css(".internship_meta")

#         for job in jobs:
#             job_data = {
#                 "title": job.css(".profile a::text").get(default="N/A").strip(),
#                 "company": job.css(".company_name a::text").get(default="N/A").strip(),
#                 "location": job.css(".location_link::text").get(default="N/A").strip(),
#                 "stipend": job.css(".stipend span::text").get(default="N/A").strip(),
#                 "duration": job.css(".item_body div::text").get(default="N/A").strip(),
#                 "apply_link": response.urljoin(job.css(".view_detail_button::attr(href)").get(default="")),
#             }
#             self.jobs_list.append(job_data)

#         # Handle Pagination (Next Page)
#         next_page = response.css("ul.pagination li:last-child a::attr(href)").get()
#         if next_page and "internships" in next_page:
#             yield response.follow(next_page, callback=self.parse)

#     def closed(self, reason):
#         """Save all scraped jobs to a JSON file when spider closes"""
#         output_dir = "output"
#         os.makedirs(output_dir, exist_ok=True)  # Ensure output directory exists

#         with open(f"{output_dir}/internshala_jobs.json", "w", encoding="utf-8") as f:
#             json.dump(self.jobs_list, f, indent=4, ensure_ascii=False)

#         self.log(f"Saved {len(self.jobs_list)} jobs to {output_dir}/internshala_jobs.json")


import json
import scrapy

class InternshalaSpider(scrapy.Spider):
    name = 'internshala'
    start_urls = [
        'https://internshala.com/jobs/',       # First page (Jobs)
        'https://internshala.com/internships/' # Second page (Internships)
    ]
    
    # List to collect scraped items
    custom_items = []

    def parse(self, response):
        jobs = response.css("#internship_list_container_1 .container-fluid.individual_internship")
        
        for job in jobs:
            item = {
                "title": job.css("h3.job-internship-name a::text").get(default="").strip(),
                "company": job.css(".company-name::text").get(default="").strip(),
                "location": job.css("div.row-1-item.locations a::text").getall(),
                "duration": job.css("div.row-1-item:nth-child(2) span::text").get(default="").strip(),
                "salary": job.css("div.row-1-item:nth-child(3) span::text").get(default="").strip(),
                "posted_time": job.css("div.status-inactive span::text, div.status-success span::text").get(default="").strip(),
                "job_url": response.urljoin(job.css("h3.job-internship-name a::attr(href)").get()),
                "logo_url": job.css(".internship_logo img::attr(src)").get(default="")
            }
            self.custom_items.append(item)
            yield item

        # Follow pagination for both jobs and internships
        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def closed(self, reason):
        # When the spider finishes, write all collected items to a JSON file.
        filename = "internshala_output.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.custom_items, f, ensure_ascii=False, indent=4)
        self.logger.info(f"Scrape complete. Data written to {filename}")

