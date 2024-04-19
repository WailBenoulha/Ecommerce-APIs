from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('product/',views.ProductApiView.as_view()),
    path('product/<int:pk>/',views.ProductApiView.as_view()),
    path('category/',views.CategoryApiView.as_view()),
    path('category/<int:pk>',views.CategoryApiView.as_view()),
    path('order/',views.OrderApiView.as_view()),
    path('order/<int:pk>/',views.OrderApiView.as_view()),
    path('user/',views.UserApiView.as_view()),
    path('user/<int:pk>/',views.UserApiView.as_view())
]
