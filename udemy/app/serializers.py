from rest_framework import serializers,viewsets,routers
from .models import *
from django.contrib.auth.models import User
from rest_framework.generics import RetrieveAPIView

class VerifyUserProfile(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = "__all__"
        extra_kwargs = {
            "user":{"read_only":True}
        }

class UserSerializer(serializers.ModelSerializer):

    role = VerifyUserProfile(read_only = True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password','role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    


class UserRoleSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = UserRole
        fields = ['id', 'username', 'role']

class Categoryserializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields="__all__"

class CourseSerializer(serializers.ModelSerializer):
    author = UserRoleSerializer(read_only=True)
    category = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model=Course
        fields= ['id','category','title','description','image','price','author','language']

class HomepageCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id','title', 'image','price']

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model=Topic
        fields="__all__"

class Programminglanguageserializer(serializers.ModelSerializer):
    class Meta:
        model=Programminglanguage
        fields="__all__"

class PaymentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source = "user.username", read_only = True)
    course_title = serializers.CharField(source = 'course.title', read_only = True)
    class Meta:
        model = Payment
        fields = ['id','user','username', 'course','course_title','amount','order_id','payment_id','signature','status','created_at']
        read_only_fields = ['id','username','course_title','created_at']

class EnrollmentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source = 'user.username', read_only = True)
    course_title = serializers.CharField(source = 'course.title' , read_only = True)

    class Meta:
        model = EnrollCourse
        fields = ['user', 'username', 'course','course_title','progress','completed_topics','enrolled_at']
        read_only_fields = ['username','course_title','enrolled_at','progress']

class CourseDetailSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    category = serializers.StringRelatedField()
    class Meta:
        model = Course
        fields = ['id','title','description','category','author']