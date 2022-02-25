from email import message
import this
from django.contrib.auth.models import Group
from unicodedata import category
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.forms import PasswordInput, inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.template import context
from .decorators import *
from home.decorators import authenticated_user
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from .filters import *
import sweetify
# Create your views here.



@login_required(login_url="login")
@allowedUsers(allowed_roles=["customer"])
def OrderPage(request):
    orders1=request.user.customer.order_set.filter(status='Pending')
    orders2=request.user.customer.order_set.filter(status='Out for delivery')
    orders3=request.user.customer.order_set.filter(status='Delivered')
    total=0
    for order in orders1:
        total+=((order.quantity)*(order.product.price))
    for order in orders2:
        total+=order.product.price
    context={'orders1':orders1,'orders2':orders2,'total':total,'orders3':orders3}
    return render(request,'home/orders.html',context)


@allowedUsers(allowed_roles=['admin'])
def admin_panel(request):
    customers=Customer.objects.all()
    orders=Order.objects.all().order_by('date_created')
    filteruser=UserFilter(request.GET, queryset=customers)
    customers=filteruser.qs
    context={'customers':customers,'orders':orders,'form':filteruser,}
    return render(request,'home/admin_panel.html',context)

@login_required(login_url='homeNotlogin')
def home(request):
    print(Customer.user)
    if request.method=="POST":
        feed=request.POST.get('message')
        cust=request.user.customer
        Message.objects.create(customer=cust,suggestion=feed)
    group=None
    if request.user.groups.exists():
        group=request.user.groups.all()[0].name
        
    if group=="admin":
        return redirect('admin_panel')
    else:
        name=request.user.customer
        context={"islogin":True,"name":name}
        return render(request,'home/index.html',context)

def homeNotlogin(request):
    return render(request,'home/index.html',{
        "islogin":False
    })

@authenticated_user
def loginPage(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request,"Username or password is incorrect")
    return render(request,'home/login.html')

@authenticated_user
def register(request):
    form=CreateUserForm()
    messa=''
    if request.method == "POST":
        form=CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            try:
                Customer.objects.create(user=user,name=user.username,email=user.email)
                messages.success(request,'Account created successfully for '+ username)
                return redirect('login')
            except:
                u = User.objects.get(username = user.username)
                u.delete()
                messa = 'E-mail already exists'
           
    return render(request,'home/register.html',{
            'form':form, 'messa':messa
        })

def logoutUser(request):
    logout(request)
    return redirect('homeNotlogin')


def products(request):
    group=request.user.groups.all()[0].name
    print(group=="customer")
    products=Product.objects.all()
    orders=Order.objects.all()
    filterproduct=ProductFilter(request.GET, queryset=products)
    products=filterproduct.qs
    context={'products':products,'orders':orders,'group':group,'filter':filterproduct}
    return render(request,'home/products.html',context)

@allowedUsers(allowed_roles=['admin'])
def customer(request,pk_test):
    customer=Customer.objects.get(id=pk_test)
    orders=customer.order_set.all()
    msg=customer.message_set.last()
    context={'customer':customer,'orders':orders,'msg':msg,}
    return render(request,'home/customer.html',context)

def productpage(request,pk_test):
    product=Product.objects.get(id=pk_test)
    context={'product':product}
    return render(request,'home/productpage.html',context)

@allowedUsers(allowed_roles=['admin'])
def updateOrder(request,pk):
    order=Order.objects.get(id=pk)
    customer=order.customer
    form=OrderForm(instance=order)
    if request.method=="POST":
        form=OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            sweetify.success(request, 'Changes saved successfully!')
            #return redirect('admin_panel')
    context={'form':form,'customer':customer,'header':'Update order','order':True}
    return render(request,'home/form.html',context)

@allowedUsers(allowed_roles=['admin'])
def updateProduct(request,pk):
    product=Product.objects.get(id=pk)
    form=ProductForm(instance=product)
    if request.method=="POST":
        form=ProductForm(request.POST,request.FILES,instance=product)
        if form.is_valid():
            form.save()
            sweetify.success(request, 'Changes saved successfully!')
            #return redirect('products')
    context={'form':form,'header':'Update product','zxs':True}
    return render(request,'home/form.html',context)

def buyNow(request,pk):
    product=Product.objects.get(id=pk)
    if request.method=="POST":
        quantity=request.POST.get('quantity')
        Order.objects.create(product=product,customer=request.user.customer,price=product.price,quantity=quantity,status='Pending')
        sweetify.success(request, 'Order placed successfully!')
    else:
        quantity=1
        Order.objects.create(product=product,customer=request.user.customer,price=product.price,quantity=quantity,status='Pending')
        sweetify.success(request, 'Order placed successfully!')
    return redirect('products')

@allowedUsers(allowed_roles=['admin'])
def addProduct(request):
    form=ProductForm()
    if request.method=="POST":
        form=ProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            sweetify.success(request, 'Changes saved successfully!')
            return redirect('addProduct')
    context={'form':form,'header':'Add product','zxs':True}
    return render(request,'home/form.html',context)

def deleteOrder(request,pk):
    order=Order.objects.get(id=pk)
    order.delete()
    return redirect('admin_panel')

def deletePending(request,pk):
    order=Order.objects.get(id=pk)
    order.delete()
    sweetify.error(request, 'Order deleted!')
    return redirect('orders')

def deleteProduct(request,pk):
    product=Product.objects.get(id=pk)
    product.delete()
    sweetify.success(request, 'Product deleted successfully')
    return redirect('products')


def updateCustomer(request):
    customer=Customer.objects.get(user=request.user)
    form=CustomerForm(instance=customer)
    if request.method=="POST":
        form=CustomerForm(request.POST,request.FILES,instance=customer)
        if form.is_valid():
            form.save()
            sweetify.success(request, 'Changes saved successfully!')
            #return redirect('updateCustomer')
    context={'form':form,'header':'SETTINGS','customer':customer,'settings':True}
    return render(request,'home/form.html',context)

def deleteProfile(request):
    customer=Customer.objects.get(user=request.user)
    customer.SetUserImageDefault()
    return redirect('updateCustomer')
    

  


