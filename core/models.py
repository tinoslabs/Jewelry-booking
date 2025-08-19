from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('superadmin', 'Super Admin'),
        ('admin', 'Admin'),
        ('employee', 'Employee'),
        ('user', 'User'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return f"{self.user.username} - {self.role}"
     
class Blog(models.Model):
    blog_heading = models.CharField(max_length=100)
    blog_details = models.TextField(null=True, blank=True)
    main_image = models.ImageField(upload_to='images/')
    date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.blog_heading
