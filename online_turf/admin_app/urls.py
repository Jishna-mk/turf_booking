from django.urls import path
from .import views



urlpatterns=[
    path('', views.admin_signin, name='admin_signin'),
    path('viewManagers',views.viewManagers,name="viewManagers"),
    path('approveManager/<int:m_id>/',views.approveManager,name="approveManager"),
    path('removeManager/<int:m_id>/',views.removeManager,name="removeManager"),
    path('signout',views.admin_signout,name='admin_signout'),
    path('total_booking',views.total_booking,name='total_booking'),
    
]