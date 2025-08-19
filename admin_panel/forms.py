from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Customer,Role




class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import EmployeeRole, Role

class EmployeeCreateForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter email'
        })
    )
    role = forms.ModelChoiceField(
        queryset=Role.objects.all(),
        empty_label="Choose Role",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    profile_picture = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )
    mobile = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter mobile number'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        # Save user instance
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

            # Create EmployeeRole instance linked to this user
            EmployeeRole.objects.create(
                user=user,
                role=self.cleaned_data['role'],
                mobile=self.cleaned_data['mobile'],
                profile_picture=self.cleaned_data['profile_picture']
            )

        return user

class EmployeeEditForm(forms.ModelForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'})
    )
    role = forms.ModelChoiceField(
        queryset=Role.objects.all(),
        empty_label="Choose Role",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    profile_picture = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )
    mobile = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter mobile number'})
    )

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        # Extract and pop the user instance and profile instance
        self.employee_role = kwargs.pop('employee_role', None)
        super().__init__(*args, **kwargs)

        if self.employee_role:
            self.fields['role'].initial = self.employee_role.role
            self.fields['mobile'].initial = self.employee_role.mobile
            self.fields['profile_picture'].initial = self.employee_role.profile_picture

    def save(self, commit=True):
        user = super().save(commit=commit)
        if self.employee_role:
            self.employee_role.role = self.cleaned_data['role']
            self.employee_role.mobile = self.cleaned_data['mobile']
            if self.cleaned_data.get('profile_picture'):
                self.employee_role.profile_picture = self.cleaned_data['profile_picture']
            if commit:
                self.employee_role.save()
        return user

