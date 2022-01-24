from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns=[
    path('',views.home,name='home'),
    path('admin_panel/',views.admin_panel,name='admin_panel'),
    path('home/',views.homeNotlogin,name='homeNotlogin'),
    path('login/',views.loginPage,name="login"),
    path('logout/',views.logoutUser,name="logout"),
    path('register/',views.register,name="register"),
    path('products/',views.products,name="products"),
    path('customer/<str:pk_test>/',views.customer,name="customer"),
    path('products/<str:pk_test>/',views.productpage,name="productpage"),
    path('orders/',views.OrderPage,name='orders'),
    path('deletePending/<str:pk>/',views.deletePending,name='deletePending'),
    path('updateOrder/<str:pk>/',views.updateOrder,name='updateOrder'),
    path('updateProduct/<str:pk>/',views.updateProduct,name='updateProduct'),
    path('deleteOrder/<str:pk>/',views.deleteOrder,name='deleteOrder'),
    path('deleteProduct/<str:pk>/',views.deleteProduct,name='deleteProduct'),
    path('updateCustomer/',views.updateCustomer,name="updateCustomer"),
    path('addProduct/',views.addProduct,name='addProduct'),
    path('deleteProfile/',views.deleteProfile,name='deleteProfile'),
    path('buyNow/<str:pk>/',views.buyNow,name='buynow'),
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name='home/password_reset.html'),name='reset_password'),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name='home/password_reset_sent.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='home/password_reset_form.html'),name='password_reset_confirm'),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='home/password_reset_done.html'),name='password_reset_complete'),
]