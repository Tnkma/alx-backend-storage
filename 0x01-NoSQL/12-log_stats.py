#!/usr/bin/env python3
""" Log stats """
from pymongo import MongoClient

def print_nginx_stats():
    """ Provides some stats about Nginx logs stored in MongoDB """
    # Connect to MongoDB
    client = MongoClient('localhost', 27017)
    
    # Connect to the 'logs' database and 'nginx' collection
    db = client.logs
    collection = db.nginx
    
    # Count total number of logs
    total_logs = collection.count_documents({})
    print(f"{total_logs} logs")
    
    # Define the HTTP methods we are interested in
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    
    # Count the number of logs for each HTTP method
    print("Methods:")
    for method in methods:
        count = collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")
    
    # Count the number of logs with method "GET" and path "/status"
    status_check = collection.count_documents({"method": "GET", "path": "/status"})
    print(f"{status_check} status check")
    
    # Close the connection
    client.close()

if __name__ == "__main__":
    print_nginx_stats()
