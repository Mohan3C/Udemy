from django.shortcuts import render
from rest_framework import viewsets,filters, serializers
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from .permissions import IsTeacher
from rest_framework.parsers import MultiPartParser, FormParser



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
    

class CategoryViewset(viewsets.ModelViewSet):
    queryset=Category.objects.all()
    serializer_class=Categoryserializer
    search_fields=['name']
    filter_backends=[filters.SearchFilter]
    
    def get_permissions(self):
        if self.action in['create','update','destroy']:
            return [IsAuthenticated(), IsTeacher()]
        return [IsAuthenticated()]

class CourseViewset(viewsets.ModelViewSet):
    queryset=Course.objects.all()
    serializer_class=CourseSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        user = self.request.user
        if user.role == 'teacher':
            return Course.objects.filter(teacher=user)
        return Course.objects.all()

    search_fields=['title','description']
    filter_backends=[filters.SearchFilter]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.action in['create','update','destroy']:
            return[IsAuthenticated(), IsTeacher()]
        return [IsAuthenticated()]
    

class TopicViewset(viewsets.ModelViewSet):
    queryset=Topic.objects.all()
    serializer_class=TopicSerializer
    search_fields=['course','content','title']
    filter_backends=[filters.SearchFilter]

class Programminglangviewset(viewsets.ModelViewSet):
    queryset=Programminglanguage.objects.all()
    serializer_class=Programminglanguageserializer

# class HomepageAPIView(APIView):
#     def get(self, request):
#         categories = Category.objects.all()
#         courses = Course.objects.all()

#         return Response(
#             {
#                 "categories": Categoryserializer(categories, many=True).data,
#                 "courses": HomepageCourseSerializer(courses, many=True).data,
#             })

# class CourseDetailsAPIView(RetrieveAPIView):
    
#     queryset = Course.objects.all()
#     serializer_class = CourseDetailSerializer