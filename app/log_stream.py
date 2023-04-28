import asyncio
import socket
from dateutil import parser

from config import BATCH_SIZE
from db import create_logs


# Supports TCP/IP connection
async def connect_to_stream(host, port, stream_reader, loop):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        while True:
            data = await loop.sock_recv(sock, 1024)
            if not data:
                break
            stream_reader.feed_data(data)


# Streams logs via TCP/IP connection with accompanying docker container
async def stream_logs(host, port, timeout, loop):
    # Using timeout to end stream once all data has been collected
    # 1 is safe given current setup, can increase if server has delays/issues during transmission
    stream_reader = asyncio.StreamReader()
    # Connect to server
    connect_coro = connect_to_stream(host, port, stream_reader, loop)
    await asyncio.gather(connect_coro)
    # Set up batching
    logs = []
    log_counter = 0
    while True:
        try:
            # Process logs as they are streamed
            line = await asyncio.wait_for(stream_reader.readline(), timeout=timeout)
            if not line:
                break
            log_counter += 1
            log = process_log(line.decode("utf-8"))
            logs.append(log)
            # Batch send logs to db
            if log_counter == BATCH_SIZE:
                create_logs(logs, log_counter)
                logs = []
        except asyncio.TimeoutError:
            print("Timed out")
            break
    # Send leftover logs before exiting
    if logs:
        create_logs(logs, log_counter)


def process_log(log):
    # logs have datetime set in a non-standard way
    # could use regex to replace to use a parser or
    # split on space and handle manually
    # Choosing split in order to take into consideration
    # possibility of combined log format being introduced as well

    split_log = log.split()
    try:
        # remote user, common log format
        # primary usecase and provided examples, so running the logic for this
        # Could have separate tracks depending on contents if we expected nonconformity ( no user / combined log )
        apache_log_date = parser.parse(
            split_log[3][1:] + " " + split_log[4] + split_log[5][:-1]
        )
        # Schema could be set strictly elsewhere and used for validation / testing
        # Would use flask marshmallow
        data = {
            "ip_address": split_log[0],
            "user": split_log[2],
            "datetime": apache_log_date.isoformat(),
            "method": split_log[6][1:],
            "requested_resource": split_log[7],
            "protocol": split_log[8],
            "code": split_log[9],
            "bytes_sent": split_log[10],
            "raw": log.strip(),
        }
    except (IndexError, parser.ParserError):
        # Unusual line, passing for now
        return {}

    return data
