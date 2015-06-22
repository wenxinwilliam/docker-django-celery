## Async Job Queue Websocket Feedback - Project Template / Demo

##### Running
Install docker, docker-compose and run __docker-compose build__ (only need to build once unless Dockerfile changes) then __docker-compose up__ (see notes below). Django is on port 8008 of docker and aiohttp async server is on port 8009 (refer to docker-compose.yml).  

(Temporary)  
1. Either install webpack on host / cd into docker (__docker exec -it dockerdjangocelery_app_1 bash__) and run __webpack --watch --colors__ in __mydjangoapp/mydjangoapp/static/apps/main/__ to generate compiled static files  
2. Right now to start the system, use __docker-compose up -d__ then do __docker start dockerdjangocelery_worker_1__ until worker container bootstrapping with message queue is fixed  
3. Create admin user using __docker exec -it dockerdjangocelery_app_1 python manage.py createsuperuser__, then login at _docker_hostname_or_ip_:8008/admin/  
4. Go to _docker_hostname_or_ip_:8008/ to view jobs or add job  

In case of any problem, use __docker ps__ and check if the following containers are running:
 - dockerdjangocelery_asyncapp_1
 - dockerdjangocelery_worker_1
 - dockerdjangocelery_app_1
 - dockerdjangocelery_rabbitmq_1
 - dockerdjangocelery_redis_1
 - dockerdjangocelery_db_1  

Check their logs using __docker logs -f _container_name___

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
