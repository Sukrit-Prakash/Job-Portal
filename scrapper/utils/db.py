# scrapy_project/utils/db.py

from pymongo import MongoClient
import os

def get_mongo_client():
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    return MongoClient(mongo_uri)

def get_job_collection():
    client = get_mongo_client()
    db = client["jobportal"]
    return db["jobs"]

# Example function to delete all jobs (for testing purposes)
def clear_jobs_collection():
    collection = get_job_collection()
    collection.delete_many({})
