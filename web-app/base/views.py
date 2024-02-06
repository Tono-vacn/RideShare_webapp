# from multiprocessing import context
from typing import Any
from django.db import transaction
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
from django.views.decorators.cache import never_cache

from firsthomework import settings
# Create your views here.

from .models import *
from .forms import CreateDriverForm,CreatePassengerForm, PasswordChangeForm, EditDriverForm, EditPassengerForm, CreatDriverForm_ADD, RideRequestForm, ShareForm


import os.path
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

def gmail_authenticate():
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']
    creds = None
    # token.json stored user access and refresh tokens
    credentials_path = os.path.join(settings.BASE_DIR, 'credentials.json')
    
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # Authentication if no valid credentials are available
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # This credentials.json is the credential you download from Google API portal when you 
            # created the OAuth 2.0 Client IDs
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES)
            # this is the redirect URI which should match your API setting, you can 
            # find this setting in Credentials/Authorized redirect URIs at the API setting portal
            print("Starting local server...")
            creds = flow.run_local_server(host='localhost', port=8080)
            print("Local server started.")
        # Save vouchers for later use
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)
  
def send_message(service, sender, to, subject, msg_html):
    message = MIMEMultipart('alternative')
    message['from'] = sender
    message['to'] = to
    message['subject'] = subject

    msg = MIMEText(msg_html, 'html')
    message.attach(msg)

    raw = base64.urlsafe_b64encode(message.as_bytes())
    raw = raw.decode()
    body = {'raw': raw}

    message = (service.users().messages().send(userId="me", body=body).execute())
    print(f"Message Id: {message['id']}")

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

@never_cache   
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
      
@transaction.atomic
def request_ride(request, id):
  if request.method == "POST":
    form = RideRequestForm(request.POST)
    if form.is_valid():
      ride = form.save(commit = False)
      ride.owner = request.user
      if ride.shared:
        #add code here
        ride_group = Group.objects.create(sharer = ride.owner, total_group_num = ride.owner_passenger_num, order = ride)
        ride.ride_group = ride_group

      ride.save()
      # ride.owner = request.user
      # ride.save()
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
  confirmed_rec = Ride.objects.filter(owner = cur_user, ride_status = "CONFIRMED")
  open_rec = Ride.objects.filter(owner = cur_user, ride_status = "OPEN")
  completed_rec = Ride.objects.filter(owner = cur_user, ride_status = "COMPLETED")
  cancelled_rec = Ride.objects.filter(owner = cur_user, ride_status = "CANCELLED")
  # confirmed_rec = all_rec.filter(ride_status = "CONFIRMED")
  # open_rec = all_rec.filter(ride_status = "OPEN")
  # completed_rec = all_rec.filter(ride_status = "COMPLETED")
  # cancelled_rec = all_rec.filter(ride_status = "CANCELLED")
  if request.method == 'POST':
    ride_status = request.POST.get("all_open_or_confirmed")
    if ride_status == "ALL":
      return render(request, "base/view_my_ride.html", {'all_rec':all_rec, 'user':cur_user, 'ride_status':ride_status, 'view_status':"owned"})
    elif ride_status == "CONFIRMED":
      return render(request, "base/view_my_ride.html", {'all_rec':confirmed_rec, 'user':cur_user, 'ride_status':ride_status, 'view_status':"owned"})
    elif ride_status == "OPEN":
      return render(request, "base/view_my_ride.html", {'all_rec':open_rec, 'user':cur_user, 'ride_status':ride_status, 'view_status':"owned"})
    elif ride_status == "COMPLETED":
      return render(request, "base/view_my_ride.html", {'all_rec':completed_rec, 'user':cur_user, 'ride_status':ride_status, 'view_status':"owned"})
    elif ride_status == "CANCELLED":
      return render(request, "base/view_my_ride.html", {'all_rec':cancelled_rec, 'user':cur_user, 'ride_status':ride_status, 'view_status':"owned"})
    else:
      messages.info(request, "invalid view request")
  return render(request, "base/view_my_ride.html", {'all_rec':all_rec, 'user':cur_user, 'ride_status':ride_status, 'view_status':"owned"})

@transaction.atomic
def edit_my_ride(request, id, ride_id):
  cur_user = request.user
  # ride:Ride = get_object_or_404(Ride, id = ride_id)
  ride:Ride = Ride.objects.get(id=ride_id)
  old_ride_group = ride.ride_group
  old_ride_num = ride.owner_passenger_num
  old_shared = ride.shared
  if request.method == "POST":
    form = RideRequestForm(request.POST)
    if form.is_valid():
      # form.save()
      ride.destination = form.cleaned_data["destination"]
      ride.start = form.cleaned_data["start"]
      ride.arrival_time = form.cleaned_data["arrival_time"]
      ride.pick_up_time = form.cleaned_data["pick_up_time"]
      ride.shared = form.cleaned_data["shared"]
      ride.owner_passenger_num = form.cleaned_data["owner_passenger_num"]
      ride.extra_request = form.cleaned_data["extra_request"]
      if ride.shared and not old_shared:
        ride.ride_group = Group.objects.create(sharer = ride.owner, total_group_num = ride.owner_passenger_num, order = ride)
      elif not ride.shared and old_shared:
        if old_ride_group:
          old_ride_group.delete()
        ride.ride_group = None
      elif ride.shared and old_shared:
        ride.ride_group.total_group_num += (ride.owner_passenger_num-old_ride_num)
        ride.ride_group.save()
      ride.save()
      return redirect("base:view_my_ride", id = id)
    else:
      messages.info(request, "invalid form")
  else:
    form = RideRequestForm(instance = ride)
  return render(request, "base/edit_my_ride.html", {'form':form, 'user':cur_user})

def cancel_ride(request,id,ride_id):
  cancelled_ride = Ride.objects.get(id=ride_id)
  # cur_user = cancelled_ride.owner
  # for sharer in cancelled_ride.ride_group.companions.all():
  #     sharer.total_sharers = None
  #     sharer.save()
  if cancelled_ride.ride_group:
    cancelled_ride.ride_group.delete()
  cancelled_ride.delete()
  return redirect('base:view_my_ride',id=id)

def view_open_ride(request, id):
  cur_user = CustomUser.objects.get(id = id)
  open_rec = Ride.objects.filter(ride_status = "OPEN", vehicle_type = cur_user.vehicle_type)
  return render(request, "base/view_open_ride.html", {'open_rec':open_rec, 'user':cur_user, 'capacity':cur_user.max_passenger})
# return HttpResponse("test")

def request_join_ride(request,id):
  cur_user = CustomUser.objects.get(id = id)
  form = ShareForm(request.POST)
  if request.method == "POST":
    if form.is_valid():
      start = form.cleaned_data["start"]
      destination = form.cleaned_data["destination"]
      start_time = form.cleaned_data["start_time"]
      end_time = form.cleaned_data["end_time"]
      passenger_num = form.cleaned_data["passenger_num"]
      
      #
      
      all_ride_raw = Ride.objects.filter(start = start, destination = destination, shared = True)
      return render(request, "base/available_ride_to_join.html", {'all_rec':all_ride_raw, 'user':cur_user, 'earliest':start_time, 'latest':end_time, 'destination':destination,'passenger_num':passenger_num, 'user':cur_user})
    else:
      messages.info(request, "invalid form")
  return render(request, "base/request_share_ride.html", {'form':form, 'cur_user':cur_user})

@transaction.atomic
def join_ride(request,id,ride_id, share_passenger_num):
  cur_user = CustomUser.objects.get(id = id)
  ride = Ride.objects.get(id = ride_id)
  if ride.ride_group:
    ride.ride_group.total_group_num += share_passenger_num
    ride.ride_group.companions.add(cur_user)
    #newly added record
    share_rec = ShareGroupNumberRecord.objects.create(group = ride.ride_group, order = ride, sharer = cur_user, share_num = share_passenger_num)
    ride.ride_group.save()
    ride.save()
  else:
    messages.info(request, "wrong group status")
  # return redirect('base:index',id=id)
  return redirect('base:view_joined_ride', id = id)
  
def view_joined_ride(request, id):
  cur_user = CustomUser.objects.get(id = id)
  all_rec = Ride.objects.filter(ride_group__companions = cur_user)
  confirmed_rec = Ride.objects.filter(ride_group__companions = cur_user, ride_status = "CONFIRMED")
  open_rec = Ride.objects.filter(ride_group__companions = cur_user, ride_status = "OPEN")
  completed_rec = Ride.objects.filter(ride_group__companions = cur_user, ride_status = "COMPLETED")
  cancelled_rec = Ride.objects.filter(ride_group__companions = cur_user, ride_status = "CANCELLED")
  if request.method == 'POST':
    ride_status = request.POST.get("all_open_or_confirmed")
    if ride_status == "ALL":
      return render(request, "base/view_my_ride.html", {'all_rec':all_rec, 'user':cur_user, 'ride_status':ride_status, 'view_status':"joined"})
    elif ride_status == "CONFIRMED":
      return render(request, "base/view_my_ride.html", {'all_rec':confirmed_rec, 'user':cur_user, 'ride_status':ride_status, 'view_status':"joined"})
    elif ride_status == "OPEN":
      return render(request, "base/view_my_ride.html", {'all_rec':open_rec, 'user':cur_user, 'ride_status':ride_status, 'view_status':"joined"})
    elif ride_status == "COMPLETED":
      return render(request, "base/view_my_ride.html", {'all_rec':completed_rec, 'user':cur_user, 'ride_status':ride_status, 'view_status':"joined"})
    elif ride_status == "CANCELLED":
      return render(request, "base/view_my_ride.html", {'all_rec':cancelled_rec, 'user':cur_user, 'ride_status':ride_status, 'view_status':"joined"})
    else:
      messages.info(request, "invalid view request")
  return render(request, "base/view_my_ride.html", {'all_rec':all_rec, 'user':cur_user, 'ride_status':"ALL", 'view_status':"joined"})

@transaction.atomic
def quit_ride(request,id,ride_id):
  cur_user = CustomUser.objects.get(id = id)
  ride = Ride.objects.get(id = ride_id)
  if ride.ride_status == "CONFIRMED":
    messages.info(request, "ride already confirmed, unable to quit!")
    return redirect('base:view_joined_ride', id = id)
  if ride.ride_group:
    rec = ShareGroupNumberRecord.objects.get(order = ride, sharer = cur_user)  
    ride.ride_group.total_group_num -= rec.share_num
    ride.ride_group.companions.remove(cur_user)
    ride.ride_group.save()
    ride.save()
    rec.delete()
    return redirect('base:view_joined_ride', id = id)
  # else:
  messages.info(request, "wrong group status")
  return redirect('base:view_joined_ride', id = id)

@transaction.atomic
def confirm_ride(request, id, ride_id):
  cur_user = CustomUser.objects.get(id = id)
  ride = get_object_or_404(Ride, id = ride_id)
  if ride.ride_group and ride.ride_group.total_group_num > cur_user.max_passenger:
    messages.info(request, "not enough capacity")
    return render(request, "base/error_state.html", {'user':cur_user})
  
  if ride.ride_status == "OPEN":
    ride.ride_status = "CONFIRMED"
    ride.driver = cur_user
    ride.save()
    
    service = gmail_authenticate()
    
    subject = "[Ride Service]Order Confirmation"
    mail_source = settings.EMAIL_HOST_USER
    msg = f"<h1>Your ride order has been confirmed by driver: {cur_user.username}.</h1>"
    email_ = ride.owner.email if ride.owner else None
    # service = gmail_authenticate()
    send_message(service, "tonyjyc58@gmail.com", email_, subject, msg)
    if ride.ride_group and ride.ride_group.companions:
      for sharer in ride.ride_group.companions.all():
        send_message(service, "tonyjyc58@gmail.com", sharer.email, subject, msg)
        # email_list.append(sharer.email)
    # send_mail(subject=subject, message=msg, from_email=mail_source, recipient_list=email_list)
    msg = f"<h1>Your have taken the ride: {str(ride)}.</h1>"
    # email_list = [cur_user.email]
    
    
    
    send_message(service, "tonyjyc58@gmail.com", cur_user.email, subject, msg)
    # send_mail(subject=subject, message=msg, from_email=mail_source, recipient_list=email_list)
    messages.info(request, "ride confirmed")
    return redirect('base:view_open_ride', id = id)
        
  else:
    messages.info(request, "This ride is not open for confirmation")
    return render(request, "base/error_state.html", {'user':cur_user})
  

def view_taken_ride(request, id):
  cur_user = CustomUser.objects.get(id = id)
  con_rec = Ride.objects.filter(driver = cur_user, ride_status = "CONFIRMED")
  # print(con_rec)
  return render(request, "base/view_my_ride.html", {'all_rec':con_rec, 'user':cur_user, 'ride_status':"Active", 'view_status':"confirmed"})

@transaction.atomic  
def complete_ride(request,id,ride_id):
  cur_user = CustomUser.objects.get(id = id)
  ride = get_object_or_404(Ride, id = ride_id)
  ride.ride_status = "COMPLETED"
  ride.save()
  # subject = "[Ride Service]Order Completion"
  # mail_source = settings.EMAIL_HOST_USER
  # msg = f"Your ride order has been completed by driver: {cur_user.username}."
  # email_list = [ride.owner.email] if ride.owner else []
  # if ride.ride_group and ride.ride_group.companions:
  #   for sharer in ride.ride_group.companions.all():
  #     email_list.append(sharer.email)
  # # send_mail(subject=subject, message=msg, from_email=mail_source, recipient_list=email_list)
  # msg = f"Your have completed the ride: {str(ride)}."
  # email_list = [cur_user.email]
  # # send_mail(subject=subject, message=msg, from_email=mail_source, recipient_list=email_list)
  service = gmail_authenticate()
  subject = "[Ride Service]Order Accomplished"
  mail_source = settings.EMAIL_HOST_USER
  msg = f"<h1>Your ride order has been completed by driver: {cur_user.username}.</h1>"
  email_ = ride.owner.email if ride.owner else None
  # service = gmail_authenticate()
  send_message(service, "tonyjyc58@gmail.com", email_, subject, msg)
  if ride.ride_group and ride.ride_group.companions:
    for sharer in ride.ride_group.companions.all():
      send_message(service, "tonyjyc58@gmail.com", sharer.email, subject, msg)
      # email_list.append(sharer.email)
  # send_mail(subject=subject, message=msg, from_email=mail_source, recipient_list=email_list)
  msg = f"<h1>Your have taken the ride: {str(ride)}.</h1>"
  # email_list = [cur_user.email]
    
    
    
  send_message(service, "tonyjyc58@gmail.com", cur_user.email, subject, msg)
  
  messages.info(request, "ride completed")
  return redirect('base:view_taken_ride', id = id)


def view_completed_ride(request, id):
  cur_user = CustomUser.objects.get(id = id)
  com_rec = Ride.objects.filter(driver = cur_user, ride_status = "COMPLETED")
  return render(request, "base/view_my_ride.html", {'all_rec':com_rec, 'user':cur_user, 'ride_status':"All", 'view_status':"completed"})
  
  
def view_ride_detail(request, id, ride_id):
  cur_user = CustomUser.objects.get(id = id)
  ride = get_object_or_404(Ride, id = ride_id)
  ride_group = ride.ride_group
  records = ShareGroupNumberRecord.objects.filter(order = ride)
  return render(request, "base/view_ride_detail.html", {'ride':ride, 'user':cur_user, 'ride_group':ride_group, 'records':records})
  
  
# def oauth2callback(request):
#     # 这里你将处理重定向，例如使用请求中的授权码来获取访问令牌
#     return HttpResponse('OAuth2 callback processed.')
  # return redirect('base:view_my_ride', id = id)
# def IndexView(generic.ListView):
#   template_name = "base/index.html"
#   context_object_name = "latest_question_list"
  