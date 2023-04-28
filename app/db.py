from flask_pymongo import PyMongo
import pymongo

mongo = PyMongo()


def create_logs(logs):
    mongo.db.logs.insert_many(logs)
    return True


def get_logs(filters, page=1, limit=100):
    cursor = mongo.db.logs.find(filters, {"raw": 1, "_id": 0}).sort(
        "datetime", pymongo.DESCENDING
    )
    try:
        page = int(page)
        limit = int(limit)
    except ValueError:
        return "Page and limit should be provided as integers "
    logs = cursor.skip((page - 1) * limit).limit(limit)
    return {[d["raw"] for d in list(logs)]}


def delete_logs():
    d_logs = mongo.db.logs.delete_many({})
    return {"success": True, "num_deleted": d_logs.deleted_count}
