from django.shortcuts import render
from rest_framework import viewsets,filters
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView



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

class HomepageAPIView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        courses = Course.objects.all()

        return Response(
            {
                "categories": Categoryserializer(categories, many=True).data,
                "courses": HomepageCourseserializer(courses, many=True).data,
            })

class CourseDetailsAPIView(APIView):
    def get(self, request, pk):
        courses = Course.objects.get(pk=pk)

        serializer = Courseserializer(courses)
        return Response(serializer.data)