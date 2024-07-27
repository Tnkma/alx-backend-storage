#!/usr/bin/env python3
""" Log stats """
from pymongo import MongoClient


if __name__ == "__main__":
    """ prints ngix stats logs """
    client = MongoClient('mongodb://127.0.0.1:27017')
    col = client.logs.nginx
    print("{} logs".format(col.estimated_document_count()))
    print("Methods:")
    for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        count = col.count_documents({'method': method})
        print("\tmethod {}: {}".format(method, count))
    get_stats = col.count_documents({'method': 'GET', 'path': "/status"})
    print("{} status check".format(get_stats))