from django.shortcuts import render,redirect
from users_app.forms import UserAddForm
from .forms import ManagerProfileForm
from django.contrib.auth.models import User,Group
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from .models import TurfList
from .forms import TurfDetailsForm
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from users_app.models import Booking,Message
# Create your views here.


def turf_detail(request):
    turfs=TurfList.objects.all().order_by("-Turf_ID")
    return render(request,"manager/manager_index.html",{"all_turf":turfs})

from django.utils import timezone
from datetime import timedelta
 # Assuming your Booking model is in the same app

def all_booking(request):
    # Fetch all bookings made within the last 24 hours
    time_threshold = timezone.now() - timedelta(days=1)
    allbookings = Booking.objects.filter(start_time__gte=time_threshold).order_by('-start_time')
    return render(request, 'all_booking.html', {'allbookings': allbookings})




from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import ManagerProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

def managersignup(request):
    form=UserAddForm()
    manager_form=ManagerProfileForm()
    if request.method=="POST":
        form = UserAddForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            email=form.cleaned_data.get('email')
            if User.objects.filter(username=username).exists():
                messages.info(request,"Username is Already Exists")
                return redirect('managersignup')
            if User.objects.filter(email=email).exists():
                messages.info(request,"This Emailid is Already Taken")
                return redirect('managersignup')
            
            new_user = form.save()
            new_user.is_active = False
            new_user.save()
                
            group = Group.objects.get(name='manager')
            new_user.groups.add(group) 

            manager_form = ManagerProfileForm(request.POST,request.FILES)
            if manager_form.is_valid():
                manager = manager_form.save()
                manager.user = new_user
                manager.save()
                messages.success(request,"Registered as Manager! Wait for Approval")
                return redirect('managersignin')
            else:
                messages.success(request,"Couldn't perform  Signup")
        else:
            messages.error(request,"Error in manager profile details.")
    return render(request,"manager\signup.html",{"form":form,"manager_form":manager_form})



def managersignin(request):
    if request.method == "POST":
        username = request.POST['uname']
        password = request.POST['password']
        user1 = authenticate(request, username = username , password = password)
        
        if user1 is not None:
            
            request.session['username'] = username
            request.session['password'] = password
            messages.info(request,'Logged In Successfully')
            login(request, user1)
            group = request.user.groups.all()[0].name
            if(group == "manager"):
                return redirect('turf_detail')
            else:
                messages.info(request,'Username or Password Incorrect')
                return redirect("managersignout")
        
        else:
            messages.info(request,'Username or Password Incorrect')
            return redirect('managersignin')
    return render(request,"manager/signin.html")


def managersignout(request):
    logout(request)
    return redirect('index')

def deleteturf(request,pk):
    edit=TurfList.objects.get(Turf_ID=pk)
    edit.delete()
    messages.info(request,"deleted")
    return redirect("turf_detail")

Area_choices=(
    ('Calicut','Calicut'),
    ('Malappuram','Malappuram'),
)


def add_turf(request):
    if request.method == 'POST':
        form = TurfDetailsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.info(request, "Successfully Added")
            return redirect('turf_detail')
    else:
        form = TurfDetailsForm()

    return render(request, "manager/add_turf.html", {'form': form, 'Area_choices': Area_choices})


def edit_turf(request,tid):
    edit_turf=TurfList.objects.get( Turf_ID=tid)
    if request.method == "POST":
        edit_turf.Turf_name=request.POST["Turf_name"]
        edit_turf.Turf_address=request.POST["Turf_address"]
        edit_turf.Turf_price=request.POST["Turf_price"]
        edit_turf.Turf_caption=request.POST["Turf_caption"]
        if "Turf_image" in request.FILES:
            edit_turf.Turf_image=request.FILES["Turf_image"]
        edit_turf.save()
        return redirect("turf_detail")
    return render(request,"manager\edit_turf.html",{"edit_turf":edit_turf}) 
from django.shortcuts import render, get_object_or_404
from .models import ManagerProfile


@login_required
def manager_profiles(request):
    manager_profile = get_object_or_404(ManagerProfile, user=request.user)
    return render(request, 'manager/manager_profiles.html', {'manager_profile': manager_profile})


def send_message_to_user(request):
    if request.method == "POST":
        manager = get_object_or_404(ManagerProfile, user=request.user)
        user_id = request.POST.get("user_id")  # Assuming you have a hidden input with user_id in your form
        user = get_object_or_404(User, id=user_id)
        message_text = request.POST["message"]

        # Create a new message with reply set to False for new messages to users
        Message.objects.create(message=message_text, manager=manager, user=user, reply=False)

        messages.info(request, "Message Sent")
        return redirect("view_manager_messages")

    # Handle GET requests or other cases
    return redirect("view_manager_messages")


def view_manager_messages(request):
    manager = get_object_or_404(ManagerProfile, user=request.user)
    user_messages = Message.objects.filter(manager=manager, reply=False)
    reply_messages = Message.objects.filter(manager=manager, reply=True)
    user_messages_count = user_messages.count()
    reply_messages_count = reply_messages.count()
    return render(request, "manager/view-messages.html", {
        "user_messages": user_messages,
        "reply_messages": reply_messages,
        "user_messages_count": user_messages_count,
        "reply_messages_count": reply_messages_count
    })

def reply_message(request, id):
    if request.method == "POST":
        manager = get_object_or_404(ManagerProfile, user=request.user)
        user = get_object_or_404(User, id=id)
        message_text = request.POST["message"]

        # Create a new message with reply set to True for user's sent messages
        Message.objects.create(message=message_text, manager=manager, user=user, reply=True)

        messages.info(request, "Message Sent")
        return redirect("view_manager_messages")
