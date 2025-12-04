
from django.contrib import admin
from django.urls import path,include
from app.views import *
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token


router=routers.DefaultRouter()
router.register(r'User', UserViewSet)
router.register(r'admin/category',CategoryViewSet, basename='admincategory')
router.register(r'course',CourseViewSet)
router.register(r'topic',TopicViewSet)
router.register(r'subCategory',SubCategoryViewSet)
router.register(r'cart',CartViewSet)
router.register(r'enrollCourse',EnrollCourseViewSet)
router.register(r'payment',PaymentViewSet)

router.register(r'notification',notificationViewSet,basename="notification")

router.register(r'wishlist',WishlistViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api-auth/', include('rest_framework.urls')),
    path("api/login/",obtain_auth_token),

    # user created APIs 
    path('api/', include(router.urls)),
    path('course/<int:pk>/detail/', CourseDetailsAPIView.as_view(), name='course-details'),





] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

