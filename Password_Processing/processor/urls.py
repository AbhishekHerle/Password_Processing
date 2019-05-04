from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'processor/doProcessing/$', views.doProcessing, name='doProcessing'),
    url(r'processor/getSample/$', views.getSample, name='getSample'),
]

