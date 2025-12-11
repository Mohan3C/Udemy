from django.contrib import admin
from .models import *

# Register your models here.
#admin.site.register(User)
admin.site.register(UserRole)
admin.site.register(Course)
admin.site.register(Category)
admin.site.register(Topic)
admin.site.register(Payment)
admin.site.register(Cart)
admin.site.register(Cartitem)
admin.site.register(Coupon)
admin.site.register(Notification)
admin.site.register(Wishlist)
admin.site.register(EnrollCourse)
admin.site.register(Order)

