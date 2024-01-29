# from multiprocessing import context
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
# from .models import Question, Choice
from django.http import Http404
from django.urls import reverse
from django.views import generic
from django.contrib import auth,messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
# Create your views here.

from .models import *
from .forms import CreateDriverForm,CreatePassengerForm, PasswordChangeForm, EditDriverForm, EditPassengerForm, CreatDriverForm_ADD, RideRequestForm


def init_page(request):
  return render(request, "base/init_page.html")

def login(request):
  if request.user.is_authenticated:
    # return HttpResponseRedirect(reverse("base:index"))
    return redirect("base:index", id = request.user.id)
  else:
    if request.method == "POST":
      username = request.POST.get("username")
      password = request.POST.get("password")
      user = auth.authenticate(username = username, password = password) 
      if user is not None and user.is_active:
        auth.login(request, user)
        return redirect("base:index", id = user.pk)
      else:
        messages.info(request, "username or password not correct")
        # return HttpResponseRedirect(reverse("base:login"))
  return render(request, "base/login.html", locals())  

def logout(request):
  auth.logout(request)
  return redirect("base:login")
  # return HttpResponseRedirect(reverse("base:login"))   
  
def register(request, flag):
    if request.method == 'POST':
        form = CreatePassengerForm(request.POST) if flag == "Passenger" else CreateDriverForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            
            # my_user.save()
            user.user_cata = "Passenger" if flag == "Passenger" else "Driver"
            user.save()
            return redirect('base:login')
        else:
            messages.info(request, "invalid form")
    else:
        form = CreatePassengerForm() if flag == "Passenger" else CreateDriverForm()

    return render(request,'base/register.html',{'form':form})
   
def index(request, id):
  cur_user = CustomUser.objects.get(id = id)
  if cur_user.user_cata == "Passenger":
    return render(request, "base/index_passenger.html", {"cur_user": cur_user})
  else: #cur_user.user_cata == "Driver":
    return render(request, "base/index_driver.html", {"cur_user": cur_user})

def edit_profile(request, id):
  # cur_user = request.CustomUser
  if request.method == "POST":
    form = EditPassengerForm(request.POST, instance = request.user) if request.user.user_cata == "Passenger" else EditDriverForm(request.POST, instance = request.user)
    form_password = PasswordChangeForm(request.user, request.POST)
    if form.is_valid() and form_password.is_valid():
      # cur_user.email = form.cleaned_data["email"]
      # cur_user.phone_num = form.cleaned_data["phone_num"]
      # cur_user.user_cata = form.cleaned_data["user_cata"]
      form.save()
      form_password.save()
      return redirect("base:index", id = id)
    else:
      messages.info(request, "invalid form")
  else:
    form = EditPassengerForm(instance = request.user) if request.user.user_cata == "Passenger" else EditDriverForm(instance = request.user)
    form_password = PasswordChangeForm(request.user)
  return render(request, "base/edit_profile.html", {'form':form, 'form_password':form_password,'user':request.user})
    
    
def register_as_driver(request,id):
  # cur_user = get_object_or_404(CustomUser, id = id)
  cur_user = request.user
  if request.method == "POST":
    # cur_user.user_cata = "Driver"
    form = CreatDriverForm_ADD(request.POST, instance = cur_user)
    if form.is_valid():
      cur_user.user_cata = "Driver"
      form.save()
      return redirect("base:index", id = id)
    else:
      messages.info(request, "invalid form")
  else:
    form = CreatDriverForm_ADD(instance = cur_user)
  return render(request, "base/register_as_driver.html", {'form':form, 'user':cur_user})
      

def request_ride(request, id):
  if request.method == "POST":
    form = RideRequestForm(request.POST)
    if form.is_valid():
      ride = form.save(commit = False)
      ride.owner = request.user
      ride.save()
      return redirect("base:index", id = id)
    else:
      messages.info(request, "invalid form")
  else:
    form = RideRequestForm()
  return render(request, "base/request_ride.html", {'form':form, 'user':request.user})
      
def view_my_ride(request, id):
  cur_user = request.user
  ride_status = "ALL"
  all_rec = Ride.objects.filter(owner = cur_user)
  confirmed_rec = all_rec.filter(ride_status = "CONFIRMED")
  open_rec = all_rec.filter(ride_status = "OPEN")
  completed_rec = all_rec.filter(ride_status = "COMPLETED")
  cancelled_rec = all_rec.filter(ride_status = "CANCELLED")
  if request.method == 'POST':
    ride_status = request.POST.get("all_open_or_confirmed")
    if ride_status == "ALL":
      return render(request, "base/view_my_ride.html", {'all_rec':all_rec, 'user':cur_user, 'ride_status':ride_status})
    elif ride_status == "CONFIRMED":
      return render(request, "base/view_my_ride.html", {'all_rec':confirmed_rec, 'user':cur_user, 'ride_status':ride_status})
    elif ride_status == "OPEN":
      return render(request, "base/view_my_ride.html", {'all_rec':open_rec, 'user':cur_user, 'ride_status':ride_status})
    elif ride_status == "COMPLETED":
      return render(request, "base/view_my_ride.html", {'all_rec':completed_rec, 'user':cur_user, 'ride_status':ride_status})
    elif ride_status == "CANCELLED":
      return render(request, "base/view_my_ride.html", {'all_rec':cancelled_rec, 'user':cur_user, 'ride_status':ride_status})
    else:
      messages.info(request, "invalid view request")
  return render(request, "base/view_my_ride.html", {'all_rec':all_rec, 'user':cur_user, 'ride_status':ride_status})

def edit_my_ride(request, id, ride_id):
  cur_user = request.user
  ride = get_object_or_404(Ride, id = ride_id)
  if request.method == "POST":
    form = RideRequestForm(request.POST, instance = ride)
    if form.is_valid():
      form.save()
      return redirect("base:view_my_ride", id = id)
    else:
      messages.info(request, "invalid form")
  else:
    form = RideRequestForm(instance = ride)
  # return HttpResponse("test")


# def IndexView(generic.ListView):
#   template_name = "base/index.html"
#   context_object_name = "latest_question_list"
  