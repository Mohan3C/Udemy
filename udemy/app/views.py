from django.shortcuts import render
from rest_framework import serializers,viewsets
from rest_framework.response import Response
from .serializer import *

from .models import *

# Create your views here.

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer