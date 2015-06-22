## Async Job Queue Websocket Feedback - Project Template / Demo

##### Running
Install docker, docker-compose and run __docker-compose build__ then __docker-compose up__. Django is on port 8008 of docker and aiohttp async server is on port 8009.

##### Overview:
1. User logs in (django), a one time token is generated and pushed to redis cache and sent back to user
2. User uses the token to authenticate and establish a websocket connection to aiohttp async webserver
3. User schedules a job (poentially long running) for celery to process
4. Celery done job processing, send status update through rabbitmq to aiohttp async server
5. Async server confirms logged in user and active websocket connection, send update to the frontend
6. User sees gets alert then page refresh

##### Main Stack
Backend
- docker
- django
- redis
- celery
- rabbitmq

Frontend
 - webpack
 - backbone, marionette

##### Disclaimer
This project is only for proof of concept, not optimized for production or security

Original project can be found [here](http://www.syncano.com/configuring-running-django-celery-docker-containers-pt-1/).
