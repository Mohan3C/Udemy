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

    class Meta:
        model=Course
        fields= ['id','title','description','image','price','author','category','language']
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['author'] = UserSerializer(instance.author).data
        rep['category'] = Categoryserializer(instance.category).data
        return rep
    

# class HomepageCourseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Course
#         fields = ['id','title', 'image','price']

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model=Topic
        fields="__all__"

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=SubCategory
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

class CartSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title',read_only = True)
    course_price = serializers.IntegerField(source='course.price',read_only = True)

    class Meta:
        model = Cart
        fields = ['user','course','course_title','course_price','added_at']

class Cartitemserializer(serializers.ModelSerializer):
    course_title=serializers.CharField(source="course.title",read_only=True)

    class Meta:
        model=Cartitem
        fields=['id','cart','course','course_title','added_at']
        read_only_fields=['cart']

        
# class CourseDetailSerializer(serializers.ModelSerializer):
#     category = serializers.StringRelatedField()
#     class Meta:
#         model = Course
#         fields = ['id','title','description','category','author','user']

#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         representation['category'] = Categoryserializer(instance.category).data
#         return representation

class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = "__all__"