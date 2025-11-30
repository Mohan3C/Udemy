from django.shortcuts import render
from rest_framework import viewsets
from .models import Category,Course,Topic,Programminglanguage
from .serializers import *


# Create your views here.
class Userviewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = Userserializer

class Categoryviewset(viewsets.ModelViewSet):
    queryset=Category.objects.all()
    serializer_class=Categoryserializer

class Courseviewset(viewsets.ModelViewSet):
    queryset=Course.objects.all()
    serializer_class=Courseserializer

class Topicviewset(viewsets.ModelViewSet):
    queryset=Topic.objects.all()
    serializer_class=Topicserializer

class Programminglangviewset(viewsets.ModelViewSet):
    queryset=Programminglanguage.objects.all()
    serializer_class=Programminglanguageserializer


