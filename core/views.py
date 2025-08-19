from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm,AdminCreateForm
from .models import UserProfile
from core.models import User

from admin_panel.forms import CustomerForm,EmployeeCreateForm
from admin_panel.models import EmployeeRole, Permission, RolePermission,Customer

# Registration for customers

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user, role='user')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'core/register.html', {'form': form})

# Login view
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'core/login.html')


def user_logout(request):
    logout(request)
    return redirect('login') 
@login_required
def dashboard(request):
    try:
        profile = request.user.userprofile  # For superadmin, admin, normal user
        context = {'role': profile.role}

        if profile.role == 'superadmin':
            return render(request, 'core/dashboard_superadmin.html', context)
        elif profile.role == 'admin':
            return render(request, 'admin-pages/dashboard.html', context)
        elif profile.role == 'user':
            return render(request, 'core/dashboard_user.html', context)
        elif profile.role == 'employee':  # ✅ Add this check
            try:
                emp_role_obj = EmployeeRole.objects.get(user=request.user)
                context = {'emp_role': emp_role_obj.role}

                role_perms = RolePermission.objects.filter(role=emp_role_obj.role).values_list('permission__name', flat=True)

                if 'inventory' in role_perms:
                    return render(request, 'employee-pages/dashboard_inventory.html', context)
                elif 'orders' in role_perms:
                    return render(request, 'employee-pages/dashboard_orders.html', context)
                elif 'sales' in role_perms:
                    return render(request, 'employee-pages/dashboard_sales.html', context)
                else:
                    return HttpResponse("You do not have access to any dashboard.")
            except EmployeeRole.DoesNotExist:
                return HttpResponse("Employee role not assigned.")
    except UserProfile.DoesNotExist:
        return HttpResponse("No profile found for this user.")

    return HttpResponse("Something went wrong.")


# @login_required
# def dashboard(request):
#     try:
#         profile = request.user.userprofile  # For superadmin, admin, normal user
#         context = {'role': profile.role}

#         if profile.role == 'superadmin':
#             return render(request, 'core/dashboard_superadmin.html', context)
#         elif profile.role == 'admin':
#             return render(request, 'admin-pages/dashboard.html', context)
#         elif profile.role == 'user':
#             return render(request, 'core/dashboard_user.html', context)

#     except UserProfile.DoesNotExist:
#         # This means it's probably an employee
#         try:
#             emp_role_obj = EmployeeRole.objects.get(user=request.user)
#             context = {'emp_role': emp_role_obj.role}

#             # Redirect to permission-based dashboard
#             role_perms = RolePermission.objects.filter(role=emp_role_obj.role).values_list('permission__name', flat=True)

#             if 'inventory' in role_perms:
#                 return render(request, 'employee-pages/dashboard_inventory.html', context)
#             elif 'orders' in role_perms:
#                 return render(request, 'employee-pages/dashboard_orders.html', context)
#             elif 'sales' in role_perms:
#                 return render(request, 'employee-pages/dashboard_sales.html', context)
#             else:
#                 return HttpResponse("You do not have access to any dashboard.")

#         except EmployeeRole.DoesNotExist:
#             return HttpResponse("No profile found for this user.")

#     return HttpResponse("Something went wrong.")




# @login_required
# def dashboard(request):
#     profile = request.user.userprofile
#     context = {'role': profile.role}
#     if profile.role == 'superadmin':
#         return render(request, 'core/dashboard_superadmin.html', context)
#     elif profile.role == 'admin':
#         return render(request, 'admin-pages/dashboard.html', context)
#     elif profile.role == 'employee':
#         emp_role = EmployeeRole.objects.get(user=request.user).role
#         context['emp_role'] = emp_role
#         return render(request, 'core/dashboard_employee.html', context)
#     else:
#         return render(request, 'core/dashboard_user.html', context)

# Create Employee by Admin


@login_required
def create_employee(request):
    if request.user.userprofile.role != 'admin':
        return redirect('dashboard')

    if request.method == 'POST':
        form = EmployeeCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user, role='employee')
            EmployeeRole.objects.create(user=user, role=form.cleaned_data['role'])
            return redirect('dashboard')
    else:
        form = EmployeeCreateForm()
    return render(request, 'core/create_employee.html', {'form': form})



@login_required
def create_admin(request):
    if request.user.userprofile.role != 'superadmin':
        return redirect('dashboard')  # Restrict access

    if request.method == 'POST':
        form = AdminCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user, role='admin')
            return redirect('dashboard')
    else:
        form = AdminCreateForm()
    return render(request, 'core/create_admin.html', {'form': form})


def create_profile(request):
    return render(request, 'core/create_profile.html')

# def permission(request):

#     return render(request, 'admin-pages/create_permission.html')

# def group_permission(request):   
#     return render(request, 'admin-pages/grouppermissions.html')

# def new_user(request):
#     return render(request, 'admin-pages/new_user.html')


