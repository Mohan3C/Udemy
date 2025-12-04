from django.shortcuts import render
from rest_framework import viewsets,filters, serializers
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication


from .models import *
from .serializers import *
from .permissions import Isstudent
from rest_framework import serializers


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':      # only registration open
            return [AllowAny()]
        return [IsAuthenticated()] 
    
    @action(detail=False,methods=["get"])
    def me(self,request):
        return Response(UserSerializer(request.user).data)
    

class CategoryViewSet(viewsets.ModelViewSet):
    queryset=Category.objects.all()
    serializer_class=Categoryserializer
    search_fields=['name']
    filter_backends=[filters.SearchFilter]

class CourseViewSet(viewsets.ModelViewSet):
   # permission_classes = [IsAuthenticated]
    queryset=Course.objects.all()
    serializer_class=CourseSerializer
    search_fields=['title','description']
    filter_backends=[filters.SearchFilter]

    

class TopicViewSet(viewsets.ModelViewSet):
    queryset=Topic.objects.all()
    serializer_class=TopicSerializer
    search_fields=['course','content','title']
    filter_backends=[filters.SearchFilter]

class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset=SubCategory.objects.all()
    serializer_class=SubCategorySerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset=Payment.objects.all()
    serializer_class=PaymentSerializer

    
class EnrollCourseViewSet(viewsets.ModelViewSet):
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


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class HomepageAPIView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        courses = Course.objects.all()

        return Response(
            {
                "categories": Categoryserializer(categories, many=True).data,
                "courses": HomepageCourseSerializer(courses, many=True).data,
            })

class CourseDetailsAPIView(RetrieveAPIView):
    # def get(self, request, pk):
    #     courses = Course.objects.get(pk=pk)

    #     serializer = Coursedetailsserializer(courses)
    #     return Response(serializer.data)
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer

class WishlistViewSet(viewsets.ModelViewSet):
    queryset=Wishlist.objects.all()
    serializer_class=Wishlistserializer
    permission_classes=[IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        user=self.request.user
        course=serializer.validated_data["course"]

        if Wishlist.objects.filter(user=user, course=course).exists():
            raise serializers.ValidationError("Course already in wishlist.")
        
        if EnrollCourse.objects.filter(user=user, course=course).exists():
            raise serializers.ValidationError("You are already enrolled in this course.")
        
        serializer.save(user=user)
        
