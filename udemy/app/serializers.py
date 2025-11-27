from rest_framework import serializers,viewsets,routers
from .models import Category,Course,Topic,Programminglanguage

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