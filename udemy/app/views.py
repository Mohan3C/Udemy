from django.shortcuts import render
from rest_framework import viewsets,filters
from .models import Category,Course,Topic,Programminglanguage
from .serializers import *

# Create your views here.
class Categoryviewset(viewsets.ModelViewSet):
    queryset=Category.objects.all()
    serializer_class=Categoryserializer
    search_fields=['name']
    filter_backends=[filters.SearchFilter]

class Courseviewset(viewsets.ModelViewSet):
    queryset=Course.objects.all()
    serializer_class=Courseserializer
    search_fields=['title','description']
    filter_backends=[filters.SearchFilter]


class Topicviewset(viewsets.ModelViewSet):
    queryset=Topic.objects.all()
    serializer_class=Topicserializer
    search_fields=['course','content','title']
    filter_backends=[filters.SearchFilter]

class Programminglangviewset(viewsets.ModelViewSet):
    queryset=Programminglanguage.objects.all()
    serializer_class=Programminglanguageserializer

