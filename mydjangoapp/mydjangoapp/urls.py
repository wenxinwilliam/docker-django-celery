from django.conf.urls import url, include
from django.contrib import admin

from rest_framework import routers

from mydjangoapp import views

admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'jobs', views.JobViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
	url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(router.urls)),
    url(r'^ws-token/', views.get_ws_token),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]