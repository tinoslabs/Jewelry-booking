from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username
    

from django.db import models

class Role(models.Model):
    ROLE_CHOICES = (
        ('inventory', 'Inventory Manager'),
        ('orders', 'Order Handler'),
        ('sales', 'Sales Manager'),
    )
    name = models.CharField(max_length=20, choices=ROLE_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()  # Show human-readable name

class Permission(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.role} - {self.permission}"


class EmployeeRole(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15,blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    status = models.BooleanField(default=True)  # Active=True, Restricted=False

    def __str__(self):
        return f"{self.user.username} - {self.role}"




