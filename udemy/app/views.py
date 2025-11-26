from django.shortcuts import render

from .models import *

# Create your views here.

def home(request):
    if request.method =="POST":
        name = request.POST.get("name")
        if name:
            obj = Name()
            obj.name= name
            obj.save()

    return render(request,"home.html")