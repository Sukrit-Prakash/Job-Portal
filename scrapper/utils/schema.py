# mongo db schema
from pymongo import MongoClient
from pymongo.collection import Collection

client = MongoClient("mongodb://localhost:27017/")
db = client["job_portal"]
jobs_collection: Collection = db["jobs"]

job_schema = {
    "source": {"type": "string"},
    "title": {"type": "string"},
    "company": {"type": "string"},
    "location": {"type": "string"},
    "stipend": {"type": "string"},
    "duration": {"type": "string"},
    "apply_link": {"type": "string"}
}
    #   "title": "N/A",
    #     "company": "N/A",
    #     "location": "N/A",
    #     "stipend": "N/A",
    #     "duration": "N/A",
    #     "apply_link": "https://internshala.com/internships"
    # },
    #  "Title": "Fullstack SDE Intern\nFullstack SDE Intern",
    #     "Company": "OpsLyft",
    #     "Location": "Noida, Uttar Pradesh, India (On-site)",
    #     "Salary": "Salary Not Mentioned",
    #     "Link": "https://www.linkedin.com/jobs/view/4153193791/?eBP=CwEAAAGVDr1hpWQvGcnJUF2dKRkFCadTfvFyk8bI48YH-4dDV3xCDuxLXslrLIUo46objF5WOk3Nj7dw45rRhUC82gnphbAm6MEfdcjDMAeYfrAP5cY9-YA6Is7bRSBlx5SY6DFqrpcg1c6oUUxJMkS4aqIxchUCG3_fQ-FqKZL4TX_kHhzq6plrn1nx_XXY3u8YMdQ8DGzqAWiOfxH-4aeqF6-kfWtQzQq67QQRpcpFYGiJT6rLHiqSF3yPe-RBrSHMyHNJrAuLaQxD9S_-_Ppu1hEO3ZG874VX0Z5cIdnvMope2aQLj8B64NGFfGPQyUHP1qzoDh01oA5h7uLwu-1nwL_8FPnh4lPSZL2uBlA0rxMplkkBss-JvNJVfBeB83e1iCjP87-5yIL1clxd5_HtSF9qtq8xg0VZ68cYIccUaVCMabgOxnqU-JFNpXmlSs30LQHAFzUVCp1NTjY-RVw_GnwRmsfHckUcMCy-_N9JMw0i-Z3I4tCm3f_KDv07&refId=Ypr5pDL%2F7cK8Uu9uJpNF2A%3D%3D&trackingId=y3xkcy4jDve082l1YovXmQ%3D%3D&trk=flagship3_search_srp_jobs"
    # },
    #    "source": "We Work Remotely",