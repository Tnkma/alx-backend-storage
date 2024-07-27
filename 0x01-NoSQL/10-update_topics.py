#!/usr/bin/env python3
""" Changes the topics of a school document based on the name """
import pymongo


def update_topics(mongo_collection, name, topics):
    """
    update many rows in the school collection
    """
    return mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )