from django.urls import path 
from . import views

urlpatterns = [
    path("",views.home,name="home"),
    path("process_form/",views.process_form,name='process_form'),
    #path('download/<int:task_id>',views.download_data,name="downloadData"),
]