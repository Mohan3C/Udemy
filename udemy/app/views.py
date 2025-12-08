from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets,filters, serializers,permissions, status
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from .permissions import IsTeacher, Isstudent
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
    
    def perform_create(self, serializer):
        user = serializer.save()

        title = f"welcome, {user.username}"
        message = """Welcome to our platform!
                We’re glad to have you here. Your account is now ready, and you can start exploring all features right away.
                If you ever need help, our support team is always here for you.
                Enjoy your journey with us! """

        create_notification(user,title,message)

    @action(detail=False,methods=["get"])
    def me(self,request):
        return Response(UserSerializer(request.user).data)

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(role__role='teacher')
    serializer_class = UserSerializer
    def create(self, request):
        serializer = TeacherSerializer(data=request.data)

        if serializer.is_valid():
            teacher = serializer.save()
            return Response(
                {
                    "message":"Teacher registered successfully",
                    "teacher_id": teacher.id,
                    "teacher_name": teacher.username,
                    "Role" : teacher.role
                },
            status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       

class CategoryViewSet(viewsets.ModelViewSet):
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
    

class TopicViewSet(viewsets.ModelViewSet):
    queryset=Topic.objects.all()
    serializer_class=TopicSerializer
    search_fields=['course','content','title']
    filter_backends=[filters.SearchFilter]

class PurchsedViewSet(viewsets.ModelViewSet):
    
    serializer_class = PurchasedSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

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

class CourseDetailsAPIView(RetrieveAPIView):
    
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer


class notificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        notification = Notification.objects.filter(user=self.request.user).order_by("-created_at")
        return notification
    
    def mark_read(self,request,pk=None):
        notification = self.get_object()
        notification.is_read = True 
        notification.save()

        return Response({"status":"read"},status=status.HTTP_200_OK)
    

def create_notification(user,title,message):
    if user.is_anonymous:
        return
    Notification.objects.create(user=user,title=title,message=message)


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
        

class AddToCartAPIView(APIView):
    def post(self, request):
        user = request.user
        course_id = request.data.get('course_id')

        if not course_id:
            return Response ({"error":"Course Id is required"},status=status.HTTP_400_BAD_REQUEST)
        
        course = get_object_or_404(Course, id=course_id)

        cart,_ = Cart.objects.get_or_create(user=user)

        if Cartitem.objects.filter(cart=cart, course= course).exists():
            return Response({"error":"Course already exist "})

        cart_item = Cartitem.objects.create(cart=cart, course=course)

        serializer = Cartitemserializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)