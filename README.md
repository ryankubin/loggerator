# loggerator - Ingest and view your logs
## Thoughts
I decided to use python/flask, which was a technology I'm familiar with, and mongodb, one that I haven't used before.  Better approach for timeseries data like logs, with little need for relationships (in scope or out of scope).  I used flask as both the backend for connecting and ingesting the logs, and serving the logs to the end consumer.  In retrospect, separating ingestion and services may have made more sense, with flask specifically; its not multithreaded without significantly more work, which can slow down the ingestion process and make the async process a bit more finicky.

## Setup  
### Log Server  
Start the log server by running:  
`docker run -p 8080:8080 gcr.io/hiring-278615/loggerator`  
<br/>
Additionally, you can provide the following flags when running the log server:  
1. **count** - Default: 800000, the amount of logs to be sent over the connection  
2. **port** - Default: 8080, the port used by TCP server to send HTTPD logs  
3. **seed** - Default: 1, the seed used to coerce log output deterministically  
<br/>
Confirm its been added to the bridge network:  
`docker network inspect bridge`  
<br/>
`...
"Containers": {
            "07438906aac61339c45b37986ea68a5c42adabf8e8a995f5e6c02bfcd9ff9b4a": {
                "Name": "hopeful_engelbart",
                "EndpointID": "4e653200a67ab063e9f4c3960c60f214cbf6a11edf00377b20175255361852a8",
                "MacAddress": "02:42:ac:11:00:02",
                "IPv4Address": "172.17.0.2/16",
                "IPv6Address": ""
            },
          },
...`

<b>Take note of the IPv4Address of the log server</b>. In the example above, it would be:
`172.17.0.2`

### Config updates  
<b>Update the LOGGER_HOST value in app/config.py to the log server IP address</b>. Note that this can be specified on ingestion call, but better to set here.  
Update batch size and timeout depending on performance concerns  
Update the app/config and docker-compose file to adjust for username/passwords.  Default config will work but is not secure  
<br/>
### App Server  
Create the images and start the containers by running:  
`docker-compose up --build`  
<br/>
### All together  
All three containers should be connected to the bridge network.  To confirm:  
`docker network inspect bridge`  
<br/>
`...
"Containers": {
            "07438906aac61339c45b37986ea68a5c42adabf8e8a995f5e6c02bfcd9ff9b4a": {
                "Name": "hopeful_engelbart",
                "EndpointID": "4e653200a67ab063e9f4c3960c60f214cbf6a11edf00377b20175255361852a8",
                "MacAddress": "02:42:ac:11:00:02",
                "IPv4Address": "172.17.0.2/16",
                "IPv6Address": ""
            },
            "923d330549de31901a1086e45c2169d8ffe17d772163e83d89dacf0b183b3ab0": {
                "Name": "log_explorer",
                "EndpointID": "72abef3f56ba724d111cad785ccf9b6cbc54e6b3af6973af3e78b3082a3ed945",
                "MacAddress": "02:42:ac:11:00:04",
                "IPv4Address": "172.17.0.4/16",
                "IPv6Address": ""
            },
            "ff9ba85b1cd1c87867c465538d18848c7fde573b132447afa1596591aceeb83c": {
                "Name": "loggerator-db-1",
                "EndpointID": "f36a93cb41f381aad24189c931b71a61523f0afe73ca0c4449576d8b8959e0fd",
                "MacAddress": "02:42:ac:11:00:03",
                "IPv4Address": "172.17.0.3/16",
                "IPv6Address": ""
            }
        },
...
`  
</br>

### Interacting  
Trigger Ingestion:  
`curl -X POST -d '{"host":"172.17.0.2", "port":8080, "timeout":1}' http://127.0.0.1:8000/logs --header "Content-Type:application/json"`  
Response:  
`{"host":"172.17.0.2","message":"Log ingestion completed at 2023-04-28 20:52:39.000278","port":8080,"timeout":1}`   
Note: params are optional if config has been adjusted appropriately.  
<br/>  
View Logs:  
`curl -s -X GET 'http://127.0.0.1:8000/logs?limit=5'`  
Response:  
`{"count":5,"logs":["249.87.118.62 - marilyntorres [21/Jul/2000 11:47:23 +0000] \"GET /photos/121 HTTP/1.0\" 500 441","165.76.41.247 - markbutler [07/Jul/2000 03:48:05 +0000] \"PUT /photos/18 HTTP/1.0\" 403 390","149.37.226.15 - delectus_laudantium [04/Jul/2000 10:40:18 +0000] \"PUT /posts/22 HTTP/1.0\" 500 217","149.37.226.15 - delectus_laudantium [04/Jul/2000 10:20:22 +0000] \"GET /photos/35 HTTP/1.0\" 403 499","249.87.118.62 - marilyntorres [03/Jul/2000 09:37:39 +0000] \"POST /likes/188 HTTP/1.0\" 200 107"],"next":"/logs?page=2&limit=5"}`  
<br/>
Protected params:  
limit = Num records to return  
page = Page to view in result set  
<br/>
Filters:  
ip_address  
user  
datetime  
method  
requested_resource  
protocol  
code  
bytes_sent  
<br/>
Any number and combination of filter parameters are available.  Exact matches only.  
<br/>
Result returns whole log enties in descending order by date.  Also provided are total count, and a next value to paginate forward (if applicable)  

### Testing
To run the provided tests, execute the following from within the `app` directory:  
`python -m unittest tests_logs.py`  
There are gaps around testing the db, as I have less familiarity with mongo and how to mock it in flask.  Requires additional tests around CRUD operations.



