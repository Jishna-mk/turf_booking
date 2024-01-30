from django.shortcuts import render,redirect,get_object_or_404
from .forms import UserAddForm
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from manager_app.models import TurfList
from .models import Booking,Message
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from manager_app .models import ManagerProfile
from .decorators import user_only
# Create your views here.

def index(request):
    return render(request,"index.html")
def about(request):
    return render(request,"about.html")
def contact(request):
    return render(request,"contact.html")
def service(request):
    return render(request,"service.html")

def viewpage(request):
    return render(request,"view.html")

def view_detail(request,Turf_ID):
    turf=get_object_or_404(TurfList,pk=Turf_ID)

    return render(request,"view_turf.html",{'turf':turf})

def turf_detail(request):
    turfs=TurfList.objects.all().order_by("-Turf_ID")
    return render(request,"manager/manager_index.html",{"all_turf":turfs})
     
Area_choices = (
    ('Calicut', 'Calicut'),
    ('Malappuram', 'Malappuram'),
)

def location_view(request, loc_code):
    location_turfs = []
    context = {}  # Initialize context outside the loop

    for code, name in Area_choices:
        if code == loc_code:
            turfs = TurfList.objects.filter(Turf_area=code)
            location_turfs.append({'location_name': name, 'turfs': turfs})
            break

    context['location_turfs'] = location_turfs
    return render(request, 'location_turf.html', context)
    

def signup(request):
    if request.method == "POST":
        print("Form submitted:", request.POST)
    form = UserAddForm(request.POST)
    if form.is_valid():
        user = form.save()
        group = Group.objects.get(name='users')
        user.groups.add(group)
        login(request, user)
        messages.info(request, "User Created")
        return redirect('signin')
    else:
        print("Form errors:", form.errors)

    return render(request, "signup.html", {"form": form})




def signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("viewpage")
        else:
            messages.error(request, "Username or password incorrect")
    
    # If the request is not POST or authentication fails, render the login page.
    return render(request, "login.html")


def signout(request):
    logout(request)
    return redirect("signin")


# views.py
from datetime import timedelta

def booking_details(request):
    time_threshold = timezone.now() - timedelta(days=1)
    bookings = Booking.objects.filter(user=request.user, start_time__gte=time_threshold).order_by('-start_time')
    return render(request, 'my_booking.html', {'bookings': bookings})



# views.py
from django.utils import timezone
def book_turf(request, turf_id):
    turf = get_object_or_404(TurfList, Turf_ID=turf_id)

    if request.method == 'POST':
        game = request.POST.get('game')
        date = request.POST.get('date')
        start_time_str = request.POST.get('start_time')
        end_time_str = request.POST.get('end_time')
        phone_number = request.POST.get('phone_number')
        timezone_offset = request.POST.get('timezone_offset')

        # Convert start_time and end_time to datetime objects with correct timezone
        start_time = timezone.make_aware(timezone.datetime.combine(timezone.now().date(), timezone.datetime.strptime(start_time_str, '%H:%M').time()))
        end_time = timezone.make_aware(timezone.datetime.combine(timezone.now().date(), timezone.datetime.strptime(end_time_str, '%H:%M').time()))

        # Check if the selected time slot is already booked for the same game and date
        if Booking.objects.filter(turf=turf, game=game, date=date, start_time__lt=end_time, end_time__gt=start_time).exists():
            error_message = 'This time slot is already booked. Please select another slot.'
            return render(request, 'view_turf.html', {'turf': turf, 'error_message': error_message})

        # Create a Booking instance
        booking = Booking(
            user=request.user,
            turf=turf,
            game=game,
            start_time=start_time,
            end_time=end_time,
            date=date,
            phone_number=phone_number,
        )
        booking.save()

        return redirect('booking_details')  # Redirect to the booking details page

    return render(request, 'user_booking.html', {'turf': turf})


def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.delete()
    return redirect('booking_details')


def view_managers(request):
    manager_profiles = ManagerProfile.objects.all().order_by("-id")
    return render(request, 'view_managers.html', {'manager_profiles': manager_profiles})
@user_only 
def send_message(request, id):
    if request.method == "POST":
        message = request.POST["message"]
        user = User.objects.get(id=id)
        manager = ManagerProfile.objects.get(user=user)
        f = Message(message=message, manager=manager, user=request.user)
        f.save()
        messages.info(request, "Message Sent")
        return redirect("view_messages")
@user_only    
def view_messages(request):
    user_messages = Message.objects.filter(user=request.user).exclude(reply=True)
    reply_messages = Message.objects.filter(user=request.user).exclude(reply=False)
    user_messages_count = user_messages.count()
    reply_messages_count = reply_messages.count()
    return render(request, "messages/view-messages.html",{"user_messages":user_messages,"reply_messages":reply_messages,"user_messages_count":user_messages_count,"reply_messages_count":reply_messages_count})    