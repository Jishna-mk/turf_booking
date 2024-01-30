from django.urls import path
from .import views

urlpatterns=[
    path('',views.turf_detail,name="turf_detail"),
    path("managersignup",views.managersignup,name="managersignup"),
    path("managersignin",views.managersignin,name="managersignin"),
    path("managersignout",views.managersignout,name="managersignout"),
    path("add_turf/",views.add_turf,name="add_turf"),
    path('deleteturf/<int:pk>',views.deleteturf,name="deleteturf"),
    path('edit_turf/<int:tid>',views.edit_turf,name='edit_turf'),
    path('all_booking/',views.all_booking,name="all_booking"),
    path('manager_profiles/', views.manager_profiles, name='manager_profiles'),
    path('view-manager-messages/', views.view_manager_messages, name="view_manager_messages"),
    path('reply_message/<int:id>', views.reply_message, name="reply_message"),
    path('send_message_to_user/', views.send_message_to_user, name='send_message_to_user'),
]

