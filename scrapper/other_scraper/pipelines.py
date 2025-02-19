# scrapy_project/pipelines.py

import os
from pymongo import MongoClient

  # Connect to MongoDB
        # mongodb+srv://sukritprakash2020:<Password>@cluster0.ztwxu.mongodb.net/

class MongoPipeline:
    def __init__(self):
        mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/jobportal")
        self.client = MongoClient(mongo_uri)
        self.db = self.client["jobportal"]
        self.collection = self.db["jobs"]  # Collection matches Mongoose model

    def process_item(self, item, spider):
        job_data = {
            "title": item.get("title"),
            "company": item.get("company"),
            "location": item.get("location"),
            "description": item.get("description"),
            "posted_date": item.get("posted_date"),
            "url": item.get("url"),
            "tags": item.get("tags", []),  # Default to an empty list if missing
            "job_type": item.get("job_type", "Full Time"),
            "salary": item.get("salary", "Not Specified"),
            "skills": item.get("skills", [])
        }

        # Insert into MongoDB, ignoring duplicates
        self.collection.update_one({"url": job_data["url"]}, {"$set": job_data}, upsert=True)
        
        return item

    def close_spider(self, spider):
        self.client.close()

# from itemadapter import ItemAdapter


# class OtherScraperPipeline:
#     def process_item(self, item, spider):
#         return item
