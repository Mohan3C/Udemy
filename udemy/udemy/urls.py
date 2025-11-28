
from django.contrib import admin
from django.urls import path,include
from app.views import *
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

router=routers.DefaultRouter()
router.register(r'User', Userviewset)
router.register(r'Category',Categoryviewset)
router.register(r'Course',Courseviewset)
router.register(r'Topic',Topicviewset)
router.register(r'Programminglanguage',Programminglangviewset)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    # user created APIs 

    path('', include(router.urls)),



] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

