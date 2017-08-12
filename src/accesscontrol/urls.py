from django.conf.urls import url

from .views import Home, Login

urlpatterns = [
	url(r'^$', Home.as_view(), name='home'),
	url(r'^login/$', Login.as_view(), name='login'),
]