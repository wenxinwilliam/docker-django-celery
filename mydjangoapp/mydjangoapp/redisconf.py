from django.conf import settings
import redis

redis_conn = redis.StrictRedis(
	host=settings.REDIS_HOST,
	port=settings.REDIS_PORT,
	db=settings.USER_TOKEN_DB,
)