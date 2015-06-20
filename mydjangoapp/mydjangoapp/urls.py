from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings

from rest_framework import routers

from mydjangoapp import views

admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'jobs', views.JobViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
	url(r'^$', views.home),
	url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(router.urls)),
    url(r'^ws-token/', views.get_ws_token),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

if settings.DEBUG:
	from django.conf.urls.static import static
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)