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
from .forms import CreateCustomUserForm, EditCustomUserForm, PasswordChangeForm


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
  
def register(request):
    if request.method == 'POST':
        form = CreateCustomUserForm(request.POST)
        if form.is_valid():
            # user = form.save()
            # my_user = CustomUser.objects.create(user)
            # my_user.save()
            form.save()
            return redirect('base:login')
        else:
            messages.info(request, "invalid form")
    else:
        form = CreateCustomUserForm()

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
    form = EditCustomUserForm(request.POST, instance = request.user)
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
    form = EditCustomUserForm(instance = request.user)
    form_password = PasswordChangeForm(request.user)
  return render(request, "base/edit_profile.html", {'form':form, 'form_password':form_password,'user':request.user})
    
  # return HttpResponse("test")


# def IndexView(generic.ListView):
#   template_name = "base/index.html"
#   context_object_name = "latest_question_list"
  