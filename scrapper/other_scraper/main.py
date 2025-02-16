from scrapy.crawler import CrawlerProcess
from spiders.internshala_scraper import InternshalaSpider
from spiders.naukri_scraper import NaukriSpider
from spiders.indeed_scraper import IndeedSpider
from spiders.weworkremotely_scraper import JobScraper
import os
import json

# Ensure output directory exists
os.makedirs("output", exist_ok=True)

# Clear previous job results
with open("output/jobs.json", "w") as f:
    json.dump([], f)

# Run all spiders
process = CrawlerProcess()

# process.crawl(NaukriSpider)
# process.crawl(IndeedSpider)
process.crawl(InternshalaSpider)
process.crawl(JobScraper)
process.start()
