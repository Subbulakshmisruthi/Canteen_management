
from django.shortcuts import render,redirect
from django.http import HttpResponse
def authenticated_user(view_func):
    def wrapper_func(request, *args, **kargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kargs)
    return wrapper_func

def allowedUsers(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kargs):
            group=None
            if request.user.groups.exists():
                group=request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kargs)
            else:
                return HttpResponse("YOU ARE NOT AUTHORIZED TO VIEW THIS PAGE. DO SIGN IN WITH A AUTHORIZED USERID AND ACCESS THE PAGE.")
        return wrapper_func
    return decorator

def customerOnly(view_func):
    def wrapper_func(request, *args, **kargs):
        group=None
        if request.user.groups.exists():
            group=request.user.groups.all()[0].name
        
        if group=="admin":
            return redirect('admin_panel')
        if group=="customer":
            return view_func(request, *args, **kargs)
            
    return wrapper_func
            
