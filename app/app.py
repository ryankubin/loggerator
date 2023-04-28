from flask import Flask, Response, jsonify, request
import asyncio

from datetime import datetime
from log_stream import stream_logs
from config import *
from db import mongo, get_logs, delete_logs


def create_app():
    # Create/ the app
    app = Flask(__name__)
    # Update values in docker-compose.yml and config.py for security purposes
    # Provided settings should work as a base
    app.config[
        "MONGO_URI"
    ] = f"mongodb://{MONGO_DB_USER}:{MONGO_DB_PASS}@{MONGO_DB_HOST}:{MONGO_DB_PORT}/{MONGO_DB_DATABASE}?authSource={MONGO_DB_AUTH_SOURCE}"
    mongo.init_app(app)

    # Register routes
    @app.route("/logs/", strict_slashes=False, methods=["GET"])
    def show_logs():
        """
        Designed to take in ALL filters, but pop out page/limit for pagination
        Could limit to schema provided, or even a shorter list (provided requirements for example)
        For security/kidproofing requests
        :param page: Paginated results to provide
        :param limit: Number of results provided at once
        :param *: query filters to be applied to the result set
        :return: dataset of raw received logs, count of logs provided,
        and (if applicable) the next URL
        """
        request_args = request.args.to_dict()
        if request_args.get("page"):
            page = request_args.pop("page")
        else:
            page = 1
        if request_args.get("limit"):
            limit = request_args.pop("limit")
        else:
            limit = 100

        filters = {}
        for key, value in request_args.items():
            filters[key] = str(value)

        return get_logs(filters, page, limit)

    # non-standard route to kickoff data connection
    # hit this AFTER the loggerator server is running to grab your logs
    @app.route("/logs/", strict_slashes=False, methods=["POST"])
    def retrieve_logs():
        """
        :param host: Host to connect to
        :param port: Host's port
        :param timeout: Timeout in case of ingestion issues
        :return: Ingestion complete message including provided parameters and time completed.
        :rtype: json
        """
        # Retrieve any provided parameters for the target server
        params = request.get_json()
        host = params.get("host", LOGGER_HOST)
        port = params.get("port", LOGGER_PORT)
        timeout = params.get("timeout", 1)

        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        # Connect and run through transmitted logs
        loop.run_until_complete(stream_logs(host, port, timeout, loop))
        return (
            jsonify(
                host=host,
                port=port,
                timeout=timeout,
                message=f"Log ingestion completed at {datetime.now()}",
            ),
            201,
        )

    # Would want to add authorization to this endpoint (shocking)
    @app.route("/logs/", strict_slashes=False, methods=["DELETE"])
    def remove_logs():
        """
        Remove all logs from the db
        :return: success message along with number of logs deleted
        :rtype: json
        """
        # Delete existing logs to start fresh
        return jsonify(delete_logs()), 202

    return app
