from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
import os

# MongoDB Atlas URI (Keep your credentials secure)
uri = os.getenv('MONGO_URI')

# Initialize MongoDB client
client = MongoClient(uri, server_api=ServerApi('1'))

# Test connection to MongoDB
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

# Function to store trends
def store_trends(unique_id, trends, ip_address):
    # Using the Atlas client connection
    db = client.twitter_trends  # Database name
    collection = db.trends     # Collection name
    
    data = {
        "unique_id": unique_id,
        "trends": trends,
        "ip_address": ip_address,
        "timestamp": datetime.now()
    }
    
    try:
        collection.insert_one(data)
        print("Trends successfully stored in MongoDB!")
    except Exception as e:
        print(f"Error storing trends: {e}")

