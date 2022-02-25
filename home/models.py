from django.contrib.auth.models import User
from pyexpat import model
import datetime
from sre_constants import CATEGORY
from telnetlib import STATUS
from tkinter import CASCADE
from django.db import models
from django.forms import ImageField

# Create your models here.
class Customer(models.Model):
    user=models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    profile_pic=models.ImageField(default='user.png',null=True,blank=False)
    name=models.CharField(max_length=100,null=True)
    phone=models.CharField(max_length=100,null=True,blank=True)
    email=models.CharField(max_length=100,null=True,unique=True)
    date_created=models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.name

    def SetUserImageDefault(self):
        self.profile_pic.delete(save=False)
        self.profile_pic = 'user.png'
        self.save()

class Product(models.Model):
    CATEGORY=(
        ('Starter','Starter'),
        ('Meal','Meal'),
        ('Dessert','Dessert'),
        ('Snack','Snack'),
    )
    name=models.CharField(max_length=100,null=True)
    image=models.ImageField(null=True,blank=True)
    price=models.FloatField(null=True)
    category=models.CharField(max_length=100,null=True,choices=CATEGORY)
    description=models.CharField(max_length=100,null=True)
    date_created=models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS=(
        ('Pending','Pending'),
        ('Out for delivery','Out for delivery'),
        ('Delivered','Delivered'),
    )
    product=models.ForeignKey(Product, null=True,on_delete=models.SET_NULL)
    customer=models.ForeignKey(Customer, null=True,on_delete=models.SET_NULL)
    price=models.FloatField(null=True)
    quantity=models.IntegerField(default=1,null=True,blank=True)
    date_created=models.DateTimeField(auto_now_add=True,null=True)
    status=models.CharField(max_length=100,null=True,choices=STATUS)

class Message(models.Model):
    customer=models.ForeignKey(Customer, null=True,on_delete=models.SET_NULL)
    suggestion=models.CharField(max_length=300,null=True)