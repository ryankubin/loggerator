# Senior Backend Engineer Challenge (2-5 hrs)

Thanks for trying our development challenge!

Let's get started.

### The Logs

The logs we ask you to consume in this challenge are sent from `loggerator` and are HTTP access logs.

For reference, check out this link https://www.w3.org/Daemon/User/Config/Logging.html.

Here is an example of what output may look like:
```bash
143.133.122.190 - shawncarr [02/Jul/2000 07:01:19 +0000] "PUT /bookmarks/281 HTTP/1.0" 403 494
23.59.50.157 - annstewart [09/Jul/2000 04:56:38 +0000] "GET /followers/178 HTTP/1.0" 200 505
37.225.86.209 - pbanks [24/Jul/2000 01:49:23 +0000] "POST /photos/196 HTTP/1.0" 403 259
205.115.86.32 - fmorgan [02/Jul/2000 03:29:28 +0000] "GET /likes/246 HTTP/1.0" 403 225
23.59.50.157 - annstewart [18/Jul/2000 02:12:31 +0000] "POST /photos/90 HTTP/1.0" 500 97
216.240.65.129 - eugeneross [16/Jul/2000 07:10:42 +0000] "POST /photos/279 HTTP/1.0" 403 252
39.106.148.70 - randybishop [21/Jul/2000 08:23:15 +0000] "POST /likes/218 HTTP/1.0" 403 239
23.59.50.157 - annstewart [08/Jul/2000 08:08:53 +0000] "POST /bookmarks/123 HTTP/1.0" 200 562
238.233.70.126 - zlee [03/Jul/2000 09:12:58 +0000] "GET /bookmarks/130 HTTP/1.0" 403 365
205.115.86.32 - fmorgan [30/Jul/2000 07:15:18 +0000] "PUT /likes/66 HTTP/1.0" 403 320
138.91.173.13 - ducimus [02/Jul/2000 04:32:40 +0000] "PUT /posts/118 HTTP/1.0" 403 75
10.183.81.228 - carloswashington [11/Jul/2000 03:13:48 +0000] "POST /bookmarks/93 HTTP/1.0" 200 460
37.225.86.209 - pbanks [26/Jul/2000 04:39:23 +0000] "POST /posts/216 HTTP/1.0" 403 4
216.240.65.129 - eugeneross [15/Jul/2000 06:01:21 +0000] "PUT /photos/40 HTTP/1.0" 200 390
39.106.148.70 - randybishop [11/Jul/2000 06:29:40 +0000] "GET /posts/174 HTTP/1.0" 200 552
37.225.86.209 - pbanks [28/Jul/2000 09:29:02 +0000] "PUT /bookmarks/8 HTTP/1.0" 403 86
```
### The Configuration

During development, it is possible (and likely a good idea) to change the behavior of the `loggerator`. You can do this by using flags:

`$ docker run gcr.io/hiring-278615/loggerator --help`.

1. **count** - Default: 800000, the amount of logs to be sent over the connection
2. **port** - Default: 8080, the port used by TCP server to send HTTPD logs
3. **seed** - Default: 1, the seed used to coerce log output deterministically

For example, `$ docker run -p 8080:8080 gcr.io/hiring-278615/loggerator --count 15 --seed 3`

### The Challenge

We ask that you write a program (or programs), in any programming language, capable of the following:

- must connect to `loggerator`; receive logs sent over the connection
- must have HTTP REST endpoint called `/logs` that allows a user to search logs sent over from `loggerator`; this endpoint must support the following query parameters and return a filtered subset of logs received
	- `code`, e.g. (`code=503`)
	- `method`, e.g. (`method=GET`)
	- `user`, e.g. (`user=randybishop`)
- must return logs in descending order by date, when any permutation of `/logs` is requested 

For example, assume the logs your program receive are the ones above (from the section **The Logs**). Let's imagine a user chooses to `curl` your program.

`$ curl <YOUR_SERVER>/logs?user=annstewart&method=POST`

```json
[
	"23.59.50.157 - annstewart [18/Jul/2000 02:12:31 +0000] \"POST /photos/90 HTTP/1.0\" 500 97"
	"23.59.50.157 - annstewart [08/Jul/2000 08:08:53 +0000] \"POST /bookmarks/123 HTTP/1.0\" 200 562",
]
```

**NOTE** Please treat this as an opportunity to show off and let see how you would write something that you'd be proud of! There is no one "correct" answer.

### Your Solution

We are expecting that you send us the source code of a fully implemented solution for the proposed challenge **using the default configurations** of `loggerator`.

Your code should build and run on a Mac (or GNU/Linux machine) running a recent OS. **Containerized solutions are mandatory** and should be runnable via Docker.

Third party libraries are permitted; however, as our intent is to come to understand your design choices, we ask for a short description of your rationale of your choices.

### Before submitting your code

**IMPORTANT**: To help keep code reviews anonymous, please be sure to remove any sensitive information about yourself from your deliverable.

**We expect you to make sure that your solution works with `loggerator` before sending it to us**. In order to test that your implementation works, be sure you have the server you've written running and listening to port 8080, then run:

```
$ docker run -p 8080:8080 gcr.io/hiring-278615/loggerator --count 10
```
This will start the process and begin listening for connections on which to send logs. Once all logs have been sent, the connection will be closed.

```bash
2020/02/05 11:09:44 listening on port 8080
2020/02/05 11:09:56 74716754 bytes written to &{{0xc0001d6080}}
```

### Acceptance Criteria

We expect you to write **code you would consider production-ready**. This can mean a variety of things, but most importantly we look for code to be well-factored, follow good practices and be tested.

What we will look for:

- Does your code fulfill the requirement and successfully run against the `loggerator`?
- How quickly does the `/logs` endpoint return queries? Are they correct?
- How clean is your design? How easy is it to understand, maintain or extend your code?
- How did you verify your software, if by automated tests or by other means? How much application code is covered?
- What kind of documentation did you ship with your code?
- How cleanly assembled is your container?

Good luck!