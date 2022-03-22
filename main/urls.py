from django.urls import path
from .views import *

urlpatterns = [
    path('main/', fileUpload, name="main"),

]
