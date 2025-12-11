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
from django.utils.crypto import get_random_string
import razorpay
from django.conf import settings



razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

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
    queryset = Order.objects.all()
    serializer_class = PurchasedSerializer
    permission_classes = [IsAuthenticated]
   
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course")

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=404)
    
        # check course already purchase 
        if Order.objects.filter(user=user, course=course, status="paid").exists():
            return Response({"error":"you already purchased this course"}, status=400)
        
        #check course order already created or not 
        existing_order = Order.objects.filter(user=user, course=course, status="pending").first()
        if existing_order:
            return Response(
                {"error":"order already created ",
                 "amount":existing_order.amount,
                "order_id":existing_order.order_id }
                )
        
        amount = int(course.price * 100)
        raz_order = razorpay_client.order.create({"amount":amount, "currency":"INR","payment_capture":1})
        
        # create order for purchased course
        order = Order.objects.create(
            user=user, course=course,
            amount=amount, 
            order_id=raz_order["id"], 
            status="pending"
        )
        return Response({
            "message":"Order Created",
            "order_id":order.order_id,
            "amount":amount,
            "key":settings.RAZORPAY_KEY_ID

        })

        # serializer = PurchasedSerializer(order)

        # return Response({"message":"course purchase successfully ", "data":serializer.data},status=201)


class PaymentViewSet(viewsets.ViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    @action(detail=False, methods=['post'])
    def verify(self, request):

        order_id = request.data.get('razorpay_order_id')
        payment_id = request.data.get('razorpay_payment_id')
        signature = request.data.get('razorpay_signature')

        try:
            order = Order.objects.get(order_id=order_id)
        except Order.DoesNotExist:
            return Response({"error":"Invalid order"}, status=400)

        data = {
            "razorpay_order_id": order_id,
            "razorpay_payment_id": payment_id,
            "razorpay_signature": signature
        }

        try:
            razorpay_client.utility.verify_payment_signature(data)
        except:
            return Response({'error':'payment is not verify'})
        
        payment = Payment.objects.create(
                order=order,
                razorpay_order_id = order_id,
                razorpay_payment_id=payment_id,
                razorpay_signature=signature,
                status="success"
            )
        
        
        # update order status
        order.status = "paid"
        order.save()
        print("payment")

        # create enrolled course
       
        enrolled = EnrollCourse.objects.create(user = order.user, course = order.course, order=order)
        
        print(enrolled)
      
        return Response({"message":"Payment verified"}, status=200)



def pay(request):
    return render(request, "payment.html")


class EnrollCourseViewSet(viewsets.ModelViewSet):
    queryset=EnrollCourse.objects.all()
    serializer_class=EnrollmentSerializer
    permission_classes=[IsAuthenticated]
    
    def get_queryset(self):
        return EnrollCourse.objects.filter(user=self.request.user)
    
    

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

        cart,_ = Cart.objects.get_or_create(user_id=user)

        if Cartitem.objects.filter(cart=cart, course= course).exists():
            return Response({"error":"Course already exist "})

        cart_item = Cartitem.objects.create(cart=cart, course=course)

        serializer = Cartitemserializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer