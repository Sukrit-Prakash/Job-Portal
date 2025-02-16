
from twisted.internet import reactor, task
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from .spiders import InternshalaSpider  # Use absolute import based on your folder structure
import datetime

# Configure Scrapy logging
configure_logging()

# Create a CrawlerRunner instance
runner = CrawlerRunner()

def run_spider():
    # Create a timestamp and a unique output filename for this run.
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f'internshala_output_{timestamp}.json'
    
    # Run the spider with a custom FEEDS setting so that the scraped data is exported as JSON.
    return runner.crawl(InternshalaSpider, custom_settings={
        'FEEDS': {
            output_file: {
                'format': 'json',
                'overwrite': True,
                'encoding': 'utf8'
            }
        }
    })

# Use LoopingCall to schedule the crawl every 30 seconds
loop = task.LoopingCall(run_spider)
loop.start(30.0)  # 30 seconds interval

# Start the Twisted reactor (this call blocks)
reactor.run()
