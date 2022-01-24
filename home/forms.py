from enum import unique
from pyexpat import model
from django.forms import ModelForm, fields, forms
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import * 

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        exclude=['product','customer']

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude=['user','email','date_created']

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class CreateUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']
        unique=('email')
        widgets = {
            'myfield': forms.TextInput(attrs={'class': 'myfieldclass'}),
        }

