import os
import uuid
import redis
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.response import TemplateResponse
from rest_framework import mixins, viewsets

from .models import Job
from .serializers import JobSerializer


def home(request):
	context = {
		'user': request.user
	}
	return TemplateResponse(request, 'home.html', context)



class JobViewSet(mixins.CreateModelMixin,
                 mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    """
    API endpoint that allows jobs to be viewed or created.
    """
    queryset = Job.objects.all()
    serializer_class = JobSerializer


@login_required
def get_ws_token(request):
	r = redis.StrictRedis(
		host=settings.REDIS_HOST,
		port=settings.REDIS_PORT,
		db=settings.USER_TOKEN_DB,
	)
	token = request.session.get('ws_token', None)
	if not token:
		token = uuid.uuid4().hex
		request.session['ws_token'] = token
		r.set(token, 1)

	send_msg(token)
	return JsonResponse({'token': token})


def send_msg(msg):
	import pika
	credentials = pika.PlainCredentials(
	    os.environ.get('RABBIT_ENV_USER', 'admin'),
	    os.environ.get('RABBIT_ENV_RABBITMQ_PASS', 'mypass'),
	)
	parameters = pika.ConnectionParameters(
	    host=os.environ.get('RABBIT_PORT_5672_TCP_ADDR'),
	    port=int(os.environ.get('RABBIT_PORT_5672_TCP_PORT')),
	    credentials=credentials,
	)
	connection = pika.BlockingConnection(parameters)

	channel = connection.channel()
	# channel.queue_delete(queue='ws_msg')
	channel.exchange_declare(exchange='ws_msg.exchange',type='direct')
	channel.queue_declare(queue='ws_msg')
	channel.queue_bind(exchange='ws_msg.exchange', queue='ws_msg')
	channel.basic_publish(
		exchange='ws_msg.exchange',
		routing_key='ws_msg',
		body=msg,
	)
	connection.close()

