from django.urls import path
from . import views
urlpatterns = [
 path('', views.register_start, name='register'),
 path('/functions', views.functions, name='functions'),
 path('/success', views.success, name='success'),
 path('/proxy_func', views.proxy_func, name='proxy_func'),
 path('/steps', views.register_steps, name='register_steps'),
 path('/write', views.register_write, name='register_write'),
]