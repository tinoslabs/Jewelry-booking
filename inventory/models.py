from django.db import models



class Category(models.Model):
    CATEGORY_CHOICES = [
        ('Gold', 'Gold'),
        ('Diamond', 'Diamond'),
        ('Silver', 'Silver'),
        ('pearl', 'Pearl'),
    ]

    name = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)

    def __str__(self):
        return self.name

# SubCategory Model
class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)  # ← was CharFied, now fixed
    category_code = models.CharField(max_length=20, unique=True)
    image = models.ImageField(upload_to='subcategory_images/', blank=True, null=True)

    def __str__(self):
        return self.name

# Product Model
class Product(models.Model):
    name = models.CharField(max_length=100)
    product_code = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f"Image for {self.product.name}"
    
    
class FeaturedProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='featured_entries')
    is_active = models.BooleanField(default=True)  # control visibility
    featured_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Featured: {self.product.name}"
