from django.conf.urls import url
from . import views
app_name = 'cricVis'
urlpatterns = [
    url(r'^$', views.index, name='index'), #URL for home page
    url(r'^fetchGraphData/$', views.fetchGraphData, name='fetchGraphData'), #URL for GET function to fetch chart response
]
