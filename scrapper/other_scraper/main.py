from scrapy.crawler import CrawlerProcess
from spiders.internshala_scraper import InternshalaSpider
# from spiders.weworkremotely_scraper import WeWorkRemotelySpider
# from spiders.linkedin_scraper import LinkedInSpider
# ------------------NOT WORING CURRENTLY-------------------
# from spiders.naukri_scraper import NaukriSpider
# from spiders.indeed_scraper import IndeedSpider

import os
import json

# Ensure output directory exists
os.makedirs("output", exist_ok=True)

# Clear previous job results
with open("output/jobs.json", "w") as f:
    json.dump([], f)

# Run all spiders
process = CrawlerProcess()

process.crawl(InternshalaSpider)
# process.crawl(WeWorkRemotelySpider)
# process.crawl(LinkedInSpider)

process.start()
