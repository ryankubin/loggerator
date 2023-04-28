from flask_pymongo import PyMongo
import pymongo
from flask import jsonify

from exceptions import InvalidAPIParams

mongo = PyMongo()


def create_logs(logs, count):
    mongo.db.logs.insert_many(logs)
    return jsonify(inserted_logs=count, success=True), 201


def get_logs(filters, page=1, limit=100):
    cursor = mongo.db.logs.find(filters, {"raw": 1, "_id": 0}).sort(
        "datetime", pymongo.DESCENDING
    )
    try:
        page = int(page)
        limit = int(limit)
    except ValueError:
        raise InvalidAPIParams("Page and limit should be provided as integers ")
    logs = list(cursor.skip((page - 1) * limit).limit(limit))
    count = len(logs)
    # Could get total log count and calculate EXACT end, but overkill when dealing with larger data set like logs
    # having an empty next seems reasonable in this edge case
    if count == limit:
        next = f"/logs?page={page+1}&limit={limit}"
    else:
        next = None
    return {"logs": [d["raw"] for d in logs], "count": count, "next": next}


def delete_logs():
    d_logs = mongo.db.logs.delete_many({})
    return {"success": True, "num_deleted": d_logs.deleted_count}
