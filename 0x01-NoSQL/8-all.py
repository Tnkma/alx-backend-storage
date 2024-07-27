#!/usr/bin/env python3
"""
This module have a utility function that list all document inserted in a collection
"""
import pymongo


def list_all(mongo_collection):
    """
    list all collections
    """
    if not mongo_collection:
        return []
    return list(mongo_collection.find())