from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserRole


@receiver(post_save,sender=User)
def create_user_role(sernder,instance,created,**kwargs):
    if created:
        UserRole.objects.create(user=instance,role="student")

#Every new user automatically becomes a student
#No manual role creation required
#Role always exists

