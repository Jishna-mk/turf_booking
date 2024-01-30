from django.urls import path 
from .import views

urlpatterns=[
    path('climate/',views.climate, name="climate")
]
