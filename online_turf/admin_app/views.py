from django.shortcuts import render,redirect
from manager_app.models import ManagerProfile,TurfList
from django.contrib.auth.models import User,Group
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from users_app.models import Booking
from datetime import timedelta
from django.utils import timezone
# Create your views here.


def admin_signin(request):
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]
        user=authenticate(request,username=username,password=password)
        if user is not None:
            request .session["username"]=username
            request .session["password"]=password
            login(request,user)
            return redirect("viewManagers")
        else:
            
            messages.info(request,"username or password incorrect")
            return redirect("admin_signin")

    return render(request,"admin/admin_signin.html")

def admin_signout(request):
    logout(request)
    return redirect("admin_signin")  

# def admin_home(request):
#     managers = ManagerProfile.objects.all()
#     total_turfs = TurfList.objects.all().count()
#     total_managers = ManagerProfile.objects.all().count()
#     total_bookings = Booking.objects.all().count()
#     return render(request,"admin/home_page.html",{"managers":managers,"total_turfs":total_turfs,"total_managers":total_managers,"total_bookings":total_bookings})

def viewManagers(request):
    managers = ManagerProfile.objects.all().order_by("-id")
    total_turfs = TurfList.objects.all().count()
    total_managers = ManagerProfile.objects.all().count()
    total_bookings = Booking.objects.all().count()
    return render(request,"admin/view-managers.html",{"managers":managers,"total_turfs":total_turfs,"total_managers":total_managers,"total_bookings":total_bookings})

def total_booking(request):
    # Fetch all bookings made within the last 24 hours
    time_threshold = timezone.now() - timedelta(days=1)
    allbookings = Booking.objects.filter(start_time__gte=time_threshold).order_by('-start_time')
    return render(request, 'admin/total_booking.html', {'allbookings': allbookings})


def approveManager(request,m_id):
    manager = User.objects.get(id = m_id)
    manager.is_active = True
    manager.save()
    messages.success(request,"Approved as Manager")
    return redirect("viewManagers")

from django.shortcuts import get_object_or_404
from django.contrib import messages


def removeManager(request, m_id):
    try:
        manager = get_object_or_404(User, id=m_id)

        # Access related profile using the default related name (user_set)
        manager_profile_set = manager.managerprofile_set.all()

        # Assuming there is only one related profile, you can delete it
        if manager_profile_set:
            manager_profile_set[0].delete()

        # Delete the User instance
        manager.delete()

        messages.success(request, "Removed Manager")
    except Exception as e:
        # Print the exception for debugging
        print(f"Error removing manager: {str(e)}")
        messages.error(request, "Error removing manager")

    return redirect("viewManagers")
