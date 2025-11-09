from pymongo.mongo_client import MongoClient
import certifi
import datetime
import os
from dotenv import load_dotenv


# Take from .env
load_dotenv()

mongo_config = os.getenv("MONGO_URI")
client = MongoClient(
    mongo_config,
    tls=True,
    tlsCAFile=certifi.where(),
)
db = client["search_logs"]
logs = db["films"]


# Logs query by keyword
def write_keyword(keyword: str, count: int):
    data = {
        "timestamp": datetime.datetime.now(),
        "search_type": "keyword",
        "params": {
            "keyword": keyword.lower()
        },
        "results_count": count
    }
    logs.insert_one(data)


# Logs query by genre
def write_genre(genre: str, min_year: int, max_year: int, count: int):
    data = {
        "timestamp": datetime.datetime.now(),
        "search_type": "genre",
        "params": {
            "genre": genre,
            "min_year": min_year,
            "max_year": max_year
        },
        "results_count": count
    }
    logs.insert_one(data)


# Returns last user queries
def get_last_queries(count: int) -> list[dict]:
    cursor = logs.find({}).sort([("timestamp", -1)]).limit(count)
    return [query for query in cursor]


# Returns popular queries by keyword
def popular_keywords():
    pipeline = [
        {"$match": {"search_type": "keyword"}},
        {
            "$group": {
                "_id": "$params.keyword",
                "count": {"$sum": 1}
            }
        },
        {"$sort": {"count": -1}},
        {"$limit": 5}
    ]
    cursor = logs.aggregate(pipeline, allowDiskUse=True, maxTimeMS=60000)
    return [{**query, 'type': 'keyword'} for query in cursor]


# Returns popular queries by genre
def popular_genres():
    pipeline = [
        {"$match": {"search_type": "genre"}},
        {
            "$group": {
                "_id": "$params.genre",
                "count": {"$sum": 1}
            }
        },
        {"$sort": {"count": -1}},
        {"$limit": 5}
    ]
    cursor = logs.aggregate(pipeline, allowDiskUse=True, maxTimeMS=60000)
    return [{**query, 'type': 'genre'} for query in cursor]


