from django.urls import path
from .import views


urlpatterns=[
    path('',views.index,name="index"),
    path('about',views.about,name="about"),
    path('contact',views.contact,name="contact"),
    path('service',views.service,name="service"),
    path('signup/',views.signup,name="signup"),
    path('signin/',views.signin,name="signin"),
    path('viewpage/',views.viewpage,name="viewpage"),
    path('category/<str:loc_code>/',views.location_view,name='location_view'),
    path('view_detail/<int:Turf_ID>/',views.view_detail,name="view_detail"),
    path('booking/', views.booking_details, name='booking_details'),
    path('book_turf/<int:turf_id>/', views.book_turf, name='book_turf'),
    path('cancel_booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('view_managers/',views.view_managers,name="view_managers"),
    path('send_message/<int:id>', views.send_message, name="send_message"),
    path('view_messages/', views.view_messages, name="view_messages"),
]