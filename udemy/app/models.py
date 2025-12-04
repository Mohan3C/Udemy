from django.db import models
from django.contrib.auth.models import User



# Create your models here.

class UserRole(models.Model):
    ROLES = (
        ('student', 'student'),
        ('teacher', 'teacher'),
        ('admin', 'admin')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='role')
    role = models.CharField(max_length=50, choices=ROLES, default='student')
    image = models.ImageField(upload_to="media/profile_picture/",blank=True,null=True)
    name = models.CharField(max_length=250,blank=True,default="User")
    bio = models.TextField(blank=True)
    mobile_no = models.CharField(max_length=10,blank=True,default="9999999999")

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    

class Category(models.Model):
   name = models.CharField(max_length=100)


   def __str__(self):
       return self.name
    

class SubCategory(models.Model):
    category = models.ForeignKey(Category, null=True, blank=True ,on_delete=models.CASCADE) 
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class Course(models.Model):
    category = models.ForeignKey(Category,related_name='category', null=True, blank=True ,on_delete=models.CASCADE) 
    subcategory = models.ForeignKey(SubCategory, null=True, blank=True ,on_delete=models.CASCADE) 
    title = models.CharField(max_length=150)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    image = models.ImageField(upload_to='course_cover/')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    discount_price = models.DecimalField(max_digits=6,decimal_places=2,null=True,blank=True)
    language = models.CharField(max_length=50, default='English')
    published = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_discount_price(self):
            return (self.price -self.discount_price)/self.price*100

        

class Topic(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='topics')
    title = models.CharField(max_length=150)
    content = models.TextField()


    def __str__(self):
        return self.title

class Payment(models.Model): 
   
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("success", "Success"),
        ("failed", "Failed"),
        ("refunded", "Refunded"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)

# recive payments details after enrolled course
    order_id = models.CharField(max_length=200, blank=True, null=True)
    payment_id = models.CharField(max_length=200, blank=True, null=True)
    signature = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}- {self.course} - {self.status}"
    
class EnrollCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    progress = models.FloatField(default=0)
    completed_topics = models.JSONField(default=list)

    def calculate_progress(self):
        total_topics = self.course.topics.count()
        if total_topics == 0:
            return 0.0
        
        completed = len(self.completed_topics)
        return round((completed/total_topics)* 100, 2)
    
    def save(self, *args, **kwargs):
        self.progress = self.calculate_progress

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"
    
class Coupon(models.Model):
    code=models.CharField(max_length=200)
    amount=models.DecimalField(max_digits=7,decimal_places=2)

    def __str__(self):
        return self.code
    
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    coupon=models.ForeignKey(Coupon,null=True,blank=True,on_delete=models.CASCADE)
    is_paid=models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
class Cartitem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="items")
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
       

    def __str__(self):
        return self.course.title

class Wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="wishlist_items")
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    
    class Meta:
        unique_together=("user","course")

    def __str__(self):
        return self.course.title



    


    
