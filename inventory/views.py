from django.shortcuts import render, redirect, get_object_or_404
from .forms import CategoryForm, SubCategoryForm, ProductForm, FeaturedProductForm
from .models import Category, SubCategory, Product,ProductImage, FeaturedProduct

# def add_category(request):
#     form = CategoryForm(request.POST or None)
#     if form.is_valid():
#         form.save()
#         return redirect('view_categories')
#     return render(request, 'inventory/add_category.html', {'form': form})

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('view_categories')
    else:
        form = CategoryForm()
    return render(request, 'inventory/add_category.html', {'form': form})

# def update_category(request, pk):
#     category = get_object_or_404(Category, pk=pk)
#     form = CategoryForm(request.POST or None, instance=category)
#     if form.is_valid():
#         form.save()
#         return redirect('view_categories')
#     return render(request, 'inventory/update_category.html', {'form': form, 'category': category})

def update_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    form = CategoryForm(request.POST or None, request.FILES or None, instance=category)
    if form.is_valid():
        form.save()
        return redirect('view_categories')
    return render(request, 'inventory/update_category.html', {'form': form, 'category': category})


def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    
    category.delete()
    return redirect('view_categories')
    
import uuid

def generate_subcategory_code():
    return f"SUB-{uuid.uuid4().hex[:6].upper()}"

def add_subcategory(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        category_id = request.POST.get('category')
        name = request.POST.get('name')
        image = request.FILES.get('image')

        if category_id and name:
            category = Category.objects.get(id=category_id)
            subcategory_code = generate_subcategory_code()

            SubCategory.objects.create(
                category=category,
                name=name,
                category_code=subcategory_code,
                image=image
            )
            return redirect('view_subcategories')

    return render(request, 'inventory/add_subcategory.html', {'categories': categories})


def edit_subcategory(request, id):
    subcategory = get_object_or_404(SubCategory, id=id)
    form = SubCategoryForm(request.POST or None, request.FILES or None, instance=subcategory)
    categories = Category.objects.all()
    
    if form.is_valid():
        form.save()
        return redirect('view_subcategories')
    
    return render(request, 'inventory/edit_subcategory.html', {
        'form': form,
        'subcategory': subcategory,
        'categories': categories
    })

# Delete Subcategory
def delete_subcategory(request, id):
    subcategory = get_object_or_404(SubCategory, id=id)
    subcategory.delete()
    return redirect('view_subcategories')
    


def add_product(request):
    form = ProductForm(request.POST or None)
    categories = Category.objects.all()

    if request.method == 'POST':
        if form.is_valid():
            product = form.save(commit=False)
            product.product_code = f"P-{uuid.uuid4().hex[:8].upper()}"
            product.save()

            # Handle multiple image uploads
            for img in request.FILES.getlist('product_images'):
                ProductImage.objects.create(product=product, image=img)

            return redirect('view_products')

    return render(request, 'inventory/add_product.html', {
        'form': form,
        'categories': categories
    })
    
    
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    categories = Category.objects.all()
    form = ProductForm(request.POST or None, instance=product)

    if request.method == 'POST':
        if form.is_valid():
            updated_product = form.save()
            
            # Handle new uploaded images
            for img in request.FILES.getlist('product_images'):
                ProductImage.objects.create(product=updated_product, image=img)

            return redirect('view_products')

    return render(request, 'inventory/edit_product.html', {
        'form': form,
        'categories': categories,
        'product': product,
    })
    
    
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('view_products')


from django.http import JsonResponse

def get_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = SubCategory.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse(list(subcategories), safe=False)


def view_categories(request):
    categories = Category.objects.all()
    return render(request, 'inventory/view_categories.html', {'categories': categories})


def view_subcategories(request):
    subcategories = SubCategory.objects.select_related('category').all()
    return render(request, 'inventory/view_subcategories.html', {'subcategories': subcategories})


def view_products(request):
    products = Product.objects.select_related('subcategory__category')  # For efficient joins
    return render(request, 'inventory/view_products.html', {'products': products})


def inventory_dashboard(request):
    # This view can be used to render a dashboard page
    return render(request, 'inventory/inventory_dashboard.html')


# CREATE Featured Product
def create_featured_product(request):
    if request.method == "POST":
        form = FeaturedProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('featured_product_list')
    else:
        form = FeaturedProductForm()
    return render(request, 'inventory/create_featured.html', {'form': form})

# LIST Featured Products
def featured_product_list(request):
    featured_products = FeaturedProduct.objects.select_related('product').all()
    return render(request, 'inventory/featured_list.html', {'featured_products': featured_products})

# UPDATE Featured Product
def update_featured_product(request, pk):
    featured = get_object_or_404(FeaturedProduct, pk=pk)
    if request.method == "POST":
        form = FeaturedProductForm(request.POST, instance=featured)
        if form.is_valid():
            form.save()
            return redirect('featured_product_list')
    else:
        form = FeaturedProductForm(instance=featured)
    return render(request, 'inventory/update_featured.html', {'form': form})

# DELETE Featured Product
def delete_featured_product(request, pk):
    featured = get_object_or_404(FeaturedProduct, pk=pk)
    if request.method == "POST":
        featured.delete()
        return redirect('featured_product_list')
    return render(request, 'inventory/delete_confirm.html', {'featured': featured})



