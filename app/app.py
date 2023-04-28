from flask import Flask, Response, jsonify
import asyncio
from flask import request
from datetime import datetime
from log_stream import stream_logs
from config import *
from db import mongo, get_logs, delete_logs

# Create/ the app
app = Flask(__name__)
app.config["MONGO_URI"] = f"mongodb://{MONGO_DB_USER}:{MONGO_DB_PASS}@{MONGO_DB_HOST}:{MONGO_DB_PORT}/{MONGO_DB_DATABASE}?authSource={MONGO_DB_AUTH_SOURCE}"
mongo.init_app(app)

# Register routes
@app.route('/logs/', strict_slashes=False, methods = ['GET'])
def show_logs():
    request_args = request.args.to_dict()
    if request_args.get('page'):
        page = request_args.pop('page')
    else:
        page = 1
    if request_args.get('limit'):
        limit = request_args.pop('limit')
    else:
        limit = 100

    filters = {}
    for key, value in request_args.items():
        filters[key] = str(value)

    return get_logs(filters, page, limit)

@app.route('/get_logs/', strict_slashes=False, methods=['GET'])
def receive_logs():
    # Retrieve any provided parameters
    host = request.args.get('host', default=LOGGER_HOST, type=str)
    port = request.args.get('port', default=LOGGER_PORT, type=int)
    timeout = request.args.get('timeout', default=1, type=int)

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    loop.run_until_complete(stream_logs(host, port, timeout, loop))
    return jsonify(host=host, port=port, timeout=timeout, message=f"Log ingestion completed at {datetime.now()}"), 201

@app.route('/logs/', strict_slashes=False, methods=['DELETE'])
def remove_logs():
    # Delete existing logs to start fres
    return Response(delete_logs(), 202, mimetype="application/json")


if __name__ == "__main__":
    app.run(debug=True)




