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
    
class TeacherSerializer(serializers.ModelSerializer):
    role = VerifyUserProfile(read_only = True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password','role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username= validated_data['username'],
            email= validated_data.get('email'),
            password= validated_data['password']
        )
        UserRole.objects.update_or_create(user=user, defaults={'role':'teacher'})
        
        return user
    

class UserRoleSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = UserRole
        fields = ['id', 'username', 'role']

class Categoryserializer(serializers.ModelSerializer):
    
    class Meta:
        model=Category
        fields=['id','name']

class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model=Course
        fields= ['id','title','description','image','price','discount_price','author','category','language']
        read_only_fields = ['author']
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['author'] = UserSerializer(instance.author).data
        rep['category'] = Categoryserializer(instance.category).data
        return rep

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model=Topic
        fields= "__all__"

    def validate(self, data):
        topic_type = data.get('topic_type')
        if isinstance(topic_type, str):
            topic_type = topic_type.strip('"').strip("'")
            data['topic_type'] = topic_type.lower()
        content = data.get('content')
        video = data.get('video')

        if topic_type == 'text':
            if not content or content.strip() == '':
                raise serializers.ValidationError("only insert text")
            data['video'] = None
        elif topic_type == 'video':
            if not video:
                raise serializers.ValidationError("only insert video file")
            data['content'] = None
        else:
            raise serializers.ValidationError("invalied topic_type")
        return data


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
        fields = ['user','course_title','course_price','added_at']

class Cartitemserializer(serializers.ModelSerializer):
    course_title=serializers.CharField(source="course.title",read_only=True)

    class Meta:
        model=Cartitem
        fields="__all__"
        read_only_fields=['cart']

class Wishlistserializer(serializers.ModelSerializer):
    course_title=serializers.CharField(source="course.title",read_only=True)

    class Meta:
        model=Wishlist
        fields=["id","user","course","course_title"]
        read_only_fields=["user"]


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = "__all__"