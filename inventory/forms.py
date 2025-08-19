from django import forms
from .models import Category, SubCategory, Product, FeaturedProduct


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'image']
        widgets = {
            'name': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
 
        
class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['category', 'name', 'image']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

     
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'subcategory']
        
        
class FeaturedProductForm(forms.ModelForm):
    class Meta:
        model = FeaturedProduct
        fields = ['product', 'is_active']
