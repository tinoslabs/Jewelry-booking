from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from .models import Customer, EmployeeRole, Permission, RolePermission
from .forms import CustomerForm,EmployeeCreateForm
from .forms import EmployeeEditForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from core.models import UserProfile
from django.contrib import messages
from user.models import Order
from django.contrib.auth import get_user_model
# from core.models import EmployeeRole

@login_required
def admin_dashboard(request):
    return render(request, 'admin-pages/dashboard.html')

@login_required
def manage_products(request):
    products = Product.objects.all()
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_products')
    return render(request, 'admin-pages/manage_products.html', {'form': form, 'products': products})



@login_required
def manage_orders(request):
    orders = Order.objects.all()
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_orders')
    return render(request, 'admin-pages/manage_orders.html', {'form': form, 'orders': orders})

@login_required
def manage_customers(request):
    customers = Customer.objects.all()
    form = CustomerForm()
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_customers')
    return render(request, 'admin-pages/manage_customers.html', {'form': form, 'customers': customers})


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import EmployeeRole, Permission, RolePermission  # Adjust as per your models

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Role, Permission, RolePermission

@login_required
def create_permission(request):
    roles = Role.ROLE_CHOICES

    permissions_dict = {
        "Users Management": ["View", "Create", "Edit", "Delete", "View all records of all users"],
        "User Permission": ["View", "Create", "Edit", "Delete"],
        "Products": ["View", "Create", "Edit", "Delete", "Barcode", "Import Products"],
        "Adjustment": ["View", "Create", "Edit", "Delete"],
        "Transfer": ["View", "Create", "Edit", "Delete"],
        "Expenses": ["View", "Create", "Edit", "Delete"],
        "Sales": ["View", "Create", "Edit", "Delete"],
        "Purchase": ["View", "Create", "Edit", "Delete"],
        "Quotations": ["View", "Create", "Edit", "Delete"],
        "Sales Return": ["View", "Create", "Edit", "Delete"],
        "Purchase Return": ["View", "Create", "Edit", "Delete"],
        "Payment Sales": ["View", "Create", "Edit", "Delete"],
        "Payments Purchase": ["View", "Create", "Edit", "Delete"],
        "Payments Return": ["View", "Create", "Edit", "Delete"],
        "Customer list": ["View", "Create", "Edit", "Delete"],
        "Supplier List": ["View", "Create", "Edit", "Delete"],
        "Reports": ["View", "Create", "Edit", "Delete"]
    }

    if request.method == 'POST':
        role_key = request.POST.get('role')
        selected_permissions = request.POST.getlist('permissions')

        # Get or create the Role instance
        role_instance, _ = Role.objects.get_or_create(name=role_key)

        # Clear existing permissions for that role
        RolePermission.objects.filter(role=role_instance).delete()

        # Save new permissions
        for perm_code in selected_permissions:
            perm, _ = Permission.objects.get_or_create(name=perm_code)
            RolePermission.objects.create(role=role_instance, permission=perm)

        return redirect('manage_permissions')

    return render(request, 'admin-pages/create_permission.html', {
        'roles': roles,
        'permissions_dict': permissions_dict
    })
 

@login_required
def edit_role_permissions(request, role_id):
    role = get_object_or_404(Role, id=role_id)

    permissions_dict = {
        "Users Management": ["View", "Create", "Edit", "Delete", "View all records of all users"],
        "User Permission": ["View", "Create", "Edit", "Delete"],
        "Products": ["View", "Create", "Edit", "Delete", "Barcode", "Import Products"],
        "Adjustment": ["View", "Create", "Edit", "Delete"],
        "Transfer": ["View", "Create", "Edit", "Delete"],
        "Expenses": ["View", "Create", "Edit", "Delete"],
        "Sales": ["View", "Create", "Edit", "Delete"],
        "Purchase": ["View", "Create", "Edit", "Delete"],
        "Quotations": ["View", "Create", "Edit", "Delete"],
        "Sales Return": ["View", "Create", "Edit", "Delete"],
        "Purchase Return": ["View", "Create", "Edit", "Delete"],
        "Payment Sales": ["View", "Create", "Edit", "Delete"],
        "Payments Purchase": ["View", "Create", "Edit", "Delete"],
        "Payments Return": ["View", "Create", "Edit", "Delete"],
        "Customer list": ["View", "Create", "Edit", "Delete"],
        "Supplier List": ["View", "Create", "Edit", "Delete"],
        "Reports": ["View", "Create", "Edit", "Delete"]
    }

    # Get current permissions assigned to the role
    existing_permissions = RolePermission.objects.filter(role=role).values_list('permission__name', flat=True)

    if request.method == 'POST':
        selected_permissions = request.POST.getlist('permissions')

        # Delete old permissions
        RolePermission.objects.filter(role=role).delete()

        # Add new ones
        for perm_code in selected_permissions:
            perm, _ = Permission.objects.get_or_create(name=perm_code)
            RolePermission.objects.create(role=role, permission=perm)

        return redirect('manage_permissions')

    return render(request, 'admin-pages/edit_permission.html', {
        'role': role,
        'permissions_dict': permissions_dict,
        'existing_permissions': existing_permissions
    })
    
from django.contrib import messages
from .models import EmployeeRole, RolePermission
from django.contrib import messages

@login_required
def delete_role(request, role_id):
    role = get_object_or_404(Role, id=role_id)

    # Delete all associated RolePermissions
    RolePermission.objects.filter(role=role).delete()

    # Then delete the Role itself
    role.delete()

    messages.success(request, "Role and its permissions deleted successfully.")
    return redirect('manage_permissions')


@login_required
def manage_permissions(request):
    roles = Role.objects.all().order_by('-id')  # Recent roles first

    data = []
    for role in roles:
        permissions = RolePermission.objects.filter(role=role).select_related('permission')
        perm_names = [perm.permission.name for perm in permissions]

        data.append({
            'role_id': role.id,
            'role_name': role.get_name_display(),  # This uses the human-readable label
            'permissions': perm_names,
            'status': 'Active',  # Or dynamically set a status if needed
        })

    return render(request, 'admin-pages/manage_permissions.html', {'data': data})


# def create_employee(request):
#     if request.method == 'POST':
#         form = EmployeeCreateForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save() 
#             return HttpResponse('User Created Successfully')
#         else:
#             print("Form Errors:", form.errors)  

#     else:
#         form = EmployeeCreateForm()

#     return render(request, 'admin-pages/new_user.html', {'form': form})

def create_employee(request):
    if request.method == 'POST':
        form = EmployeeCreateForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()

            # ✅ Create UserProfile so system knows this is an employee
            UserProfile.objects.create(
                user=user,
                role='employee'
            )

            # ✅ Create EmployeeRole
            EmployeeRole.objects.create(
                user=user,
                role=form.cleaned_data['role'],
                mobile=form.cleaned_data['mobile'],
                profile_picture=form.cleaned_data.get('profile_picture'),
                status=True
            )

            messages.success(request, "Employee created successfully.")
            return redirect('employee_list')
    else:
        form = EmployeeCreateForm()
    return render(request, 'admin-pages/new_user.html', {'form': form})



def edit_employee(request, user_id):
    user = get_object_or_404(User, id=user_id)
    employee_role = get_object_or_404(EmployeeRole, user=user)

    if request.method == 'POST':
        form = EmployeeEditForm(request.POST, request.FILES, instance=user, employee_role=employee_role)
        if form.is_valid():
            form.save()
            return redirect('manage_employees')  # Replace with your URL name
    else:
        form = EmployeeEditForm(instance=user, employee_role=employee_role)

    return render(request, 'admin-pages/edit_employee.html', {
        'form': form,
        'user_profile': employee_role  # To show existing image
    })


@login_required
def delete_employee(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('manage_employees')


def manage_employees(request):
    employees = EmployeeRole.objects.select_related('user', 'role').all()
    return render(request, 'admin-pages/manage_employees.html', {'employees': employees})



User = get_user_model()

@login_required
def order_list(request):
    # Fetch all orders with related items and users
    orders = Order.objects.prefetch_related("items__product").select_related("user").order_by("-created_at")

    # Fetch all users for listing
    users = User.objects.all().order_by("username")

    context = {
        "orders": orders,
        "users": users,
    }
    return render(request, "admin-pages/order_list.html", context)

def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    messages.success(request, "Order deleted successfully.")
    return redirect('order_list')  # replace with your order list URL name




    




