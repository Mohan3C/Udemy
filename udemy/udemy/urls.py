
from django.contrib import admin
from django.urls import path,include
from app.views import *
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token


router=routers.DefaultRouter()
router.register(r'User', UserViewSet)
router.register(r'admin/category',CategoryViewset, basename='admincategory')
router.register(r'Course',CourseViewset)
router.register(r'Topic',TopicViewset)
router.register(r'SubCategory',SubCategoryViewSet)
router.register(r'Cart',Cartviewset)
router.register(r'EnrollCourse',Enrollmentviewset)
router.register(r'Payment',Paymentviewset)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api-auth/', include('rest_framework.urls')),
    path("api/login/",obtain_auth_token),

    # user created APIs 
    path('api/', include(router.urls)),
    path('', HomepageAPIView.as_view(), name= 'home'),
    path('course/<int:pk>/detail/', CourseDetailsAPIView.as_view(), name='course-details')




] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

