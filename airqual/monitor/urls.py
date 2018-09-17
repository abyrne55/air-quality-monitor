from django.urls import path

from . import views

app_name = 'monitor'
urlpatterns = [
    # ex: /monitor/
    path('', views.index, name='index'),
    # ex: /monitor/adddatapoint + params
    path('adddatapoint/', views.addDataPoint, name='addDataPoint'),
]
