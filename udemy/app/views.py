from django.shortcuts import render
from rest_framework import viewsets,filters
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.contrib.auth.models import User


from .models import *
from .serializers import *


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':      # only registration open
            return [AllowAny()]
        return [IsAuthenticated()] 
    

class Categoryviewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
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


