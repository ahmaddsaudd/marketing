from django.urls import path 
from . import views
from .views import home

urlpatterns = [
    path("",views.home,name="home"),
    path("process_form/",views.process_form,name='process_form')
]