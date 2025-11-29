from rest_framework import serializers,viewsets,routers
from .models import Category,Course,Topic,Programminglanguage
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class Categoryserializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields="__all__"

class Courseserializer(serializers.ModelSerializer):
    class Meta:
        model=Course
        fields="__all__"

class Topicserializer(serializers.ModelSerializer):
    class Meta:
        model=Topic
        fields="__all__"

class Programminglanguageserializer(serializers.ModelSerializer):
    class Meta:
        model=Programminglanguage
        fields="__all__"