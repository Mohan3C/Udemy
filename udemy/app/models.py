from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
   name = models.CharField(max_length=100)

   def __str__(self):
       return self.name

class Course(models.Model):
    category = models.ForeignKey(Category,related_name='category', null=True, blank=True ,on_delete=models.CASCADE) 
    title = models.CharField(max_length=150)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    image = models.ImageField(upload_to='media/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    language = models.CharField(max_length=50, default='English')
    published = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
class Topic(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    content = models.TextField()

    def __str__(self):
        return self.title

class Programminglanguage(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


