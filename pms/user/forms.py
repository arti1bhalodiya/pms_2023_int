from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import User


class ManagerRegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
        # widgets = {
        #      'username' : forms.TextInput(attrs={'class':'form-control','placeholder':'UserName'}),
        #      'email' : forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}),
        #      'password1' : forms.PasswordInput(attrs={'class':'form-control','placeholder':'password'}),
        #      'password2' : forms.PasswordInput(attrs={'class':'password','placeholder':'password'}),
        #  }
       
        
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_manager1 = True
        user.save()
        return user    


class DeveloperRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
        # widgets = {
        #      'username' : forms.TextInput(attrs={'class':'form-control','placeholder':'username'}),
        #      'email' : forms.EmailInput(attrs={'class':'form-control','placeholder':'email'}),
        #      'password1' : forms.PasswordInput(attrs={'class':'form-control','placeholder':'password'}),
        #      'password2' : forms.PasswordInput(attrs={'class':'form-control','placeholder':'reenter password'}),
        #  }

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_developer = True
        user.save()
        return user       
    
    
# class SignUpForm(forms.Form):
#     CHOICES = (
#         ('manager', 'Manager'),
#         ('developer', 'Developer'),
#     )
#     account_type = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)