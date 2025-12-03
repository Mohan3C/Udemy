
from django.contrib import admin
from django.urls import path,include
from app.views import *
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token


router=routers.DefaultRouter()
router.register(r'User', UserViewSet)
router.register(r'Category',Categoryviewset)
router.register(r'Course',Courseviewset)
router.register(r'Topic',Topicviewset)
router.register(r'SubCategory',SubCategoryViewSet)
router.register(r'Cart',Cartviewset)
router.register(r'EnrollCourse',Enrollmentviewset)


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api-auth/', include('rest_framework.urls')),
    path("api/login/",obtain_auth_token),

    # user created APIs 

    path('', include(router.urls)),



] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

