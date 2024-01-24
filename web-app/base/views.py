# from multiprocessing import context
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
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
from .forms import *



def login(request):
  if request.user.is_authenticated:
    return HttpResponseRedirect(reverse("base:index"))
  else:
    if request.method == "POST":
      username = request.POST.get("username")
      password = request.POST.get("password")
      user = auth.authenticate(username = username, password = password)    
def index(request):
  return HttpResponse("test")

def init_page(request):
  return render(request, "base/init_page.html")

# def IndexView(generic.ListView):
#   template_name = "base/index.html"
#   context_object_name = "latest_question_list"
  