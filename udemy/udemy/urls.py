
from django.contrib import admin
from django.urls import path,include
from app.views import *
from django.conf import settings
from django.conf.urls.static import static
router=routers.DefaultRouter()
router.register(r'Category',Categoryviewset)
router.register(r'Course',Courseviewset)
router.register(r'Topic',Topicviewset)
router.register(r'Programminglanguage',Programminglangviewset)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path("api/",include(router.urls)),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
