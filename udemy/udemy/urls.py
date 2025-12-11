
from django.contrib import admin
from django.urls import path,include
from app.views import *
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="My API Documentation",
        default_version='v1',
        description="API description",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)



router=routers.DefaultRouter()
router.register(r'User', UserViewSet)
router.register(r"teacher/register", TeacherViewSet, basename= "teacher")
router.register(r'category',CategoryViewSet, basename='admincategory')
router.register(r'course',CourseViewset)
router.register(r'topic',TopicViewSet)

router.register(r'enrollCourse',EnrollCourseViewSet)
router.register(r'buy', PurchsedViewSet, basename="purchased")
router.register(r'payment',PaymentViewSet)

router.register(r'notification',notificationViewSet,basename="notification")
router.register(r'wishlist',WishlistViewSet)
router.register(r'coupon', CouponViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api-auth/', include('rest_framework.urls')),
    path("api/login/",obtain_auth_token),

    # user created APIs 
    path('api/', include(router.urls)),
    path('course/<int:pk>/detail/', CourseDetailsAPIView.as_view(), name='course-details'),
    path('api/addtocart/', AddToCartAPIView.as_view(), name="add-to-cart"),
    path('pay/', pay, name="paymentsuccess"),

    # for swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc-ui'),

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

