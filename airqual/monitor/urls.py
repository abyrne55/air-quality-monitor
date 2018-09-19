from django.urls import path

from . import views

app_name = 'monitor'
urlpatterns = [
    # ex: /monitor/
    path('', views.index, name='index'),
    # ex: /monitor/add/54
    path('new/', views.new_sensor, name='new_sensor'),
    path('add/<int:sensor_id>/', views.add_data_point, name='add_data_point'),
    path('del/<int:sensor_id>/', views.del_sensor, name='del_sensor'),
    path('view/<int:sensor_id>/', views.sensor_data, name='sensor_data'),
]
