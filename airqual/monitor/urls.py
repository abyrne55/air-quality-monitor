from django.urls import path

from . import views

app_name = 'monitor'
urlpatterns = [
    # ex: /monitor/
    path('', views.index, name='index'),
    # ex: /monitor/add/54
    path('add/<int:sensor_id>/', views.add_data_point, name='add_data_point'),
]
