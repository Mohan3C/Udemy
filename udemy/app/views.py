from django.shortcuts import render
from rest_framework import viewsets,filters
from .models import Category,Course,Topic,Programminglanguage
from .serializers import *
from .permissions import Isstudent
from rest_framework import serializers


# Create your views here.
class Userviewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = Userserializer

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

class Paymentviewset(viewsets.ModelViewSet):
    queryset=Payment.objects.all()
    serializer_class=PaymentSerializer

    
class EnrollCourseviewset(viewsets.ModelViewSet):
    queryset=EnrollCourse.objects.all()
    serializer_class=EnrollmentSerializer
    permission_classes=[Isstudent]
    
    def get_queryset(self):
        return EnrollCourse.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        user=self.request.user
        course=serializer.validated_data['course']

        #prevent duplicate enrollment
        if EnrollCourse.objects.filter(user=user,course=course).exists():
            raise serializers.ValidationError("Already enrolled in this course")
        serializers.save(user=user,progress=0,completed_topics=[])
    # search_fields=['user_username','title']
    # filter_backends=[filters.SearchFilter]
    


