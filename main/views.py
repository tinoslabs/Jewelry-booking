from django.shortcuts import render, redirect, get_object_or_404
from inventory.forms import CategoryForm, SubCategoryForm, ProductForm
from inventory.models import Category, SubCategory, Product,ProductImage
from django.db.models import Prefetch
from core.models import UserProfile, Blog
from core.forms import UserProfile, BlogForm
# Create your views here.

# def index(request):
#     categories = Category.objects.all()
#     subcategories = SubCategory.objects.prefetch_related('products__images').all().order_by('name')
#     return render(request, 'index.html', {'categories': categories,'subcategories': subcategories})

def index(request):
    categories = Category.objects.all()
    
    subcategories = SubCategory.objects.values_list('name', flat=True).distinct()
    blogs = Blog.objects.all()

    # Build dictionary of subcategory name → products
    subcategory_products = {}
    for sub_name in subcategories:
        # Get all products for this subcategory name (across all categories)
        products = Product.objects.filter(subcategory__name=sub_name).select_related('subcategory').prefetch_related('images')
        subcategory_products[sub_name] = products

    return render(request, 'subcategory_products.html', {'categories': categories,
        'subcategory_products': subcategory_products, 'blogs': blogs,
    })

def index(request):
    datas = Product.objects.all()
    return render(request, 'index.html',{'datas': datas})


def index(request):
    categories = Category.objects.all()
    datas = Product.objects.all()
    # Step 1: Get unique subcategory names
    unique_names = SubCategory.objects.values_list('name', flat=True).distinct()
    blogs = Blog.objects.all()

    # Step 2: Create a list of "virtual" subcategory objects with merged products
    subcategory_groups = []
    for name in unique_names:
        subcats = SubCategory.objects.filter(name=name)
        products = Product.objects.filter(subcategory__in=subcats).prefetch_related('images')
        
        # Create a dummy object with only name and products attributes
        class GroupedSubCategory:
            pass

        group = GroupedSubCategory()
        group.name = name
        group.products = products
        subcategory_groups.append(group)

    return render(request, 'index.html', {'categories': categories,'subcategories': subcategory_groups,'blogs': blogs,'datas': datas})


def product_details(request):
    return render(request, 'product-details.html')


def products_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(subcategory__category=category).prefetch_related('images')

    return render(request, 'products.html', {
        'category': category,
        'products': products
    })
    
    
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    images = product.images.all()  # Assumes a related name `images` in your ProductImage model
    return render(request, 'product-details.html', {'product': product, 'images': images})

def cart(request):
    # Placeholder for cart functionality
    return render(request, 'cart.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact-us.html')
