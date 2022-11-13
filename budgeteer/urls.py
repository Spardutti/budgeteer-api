"""budgeteer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from app import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView) 

urlpatterns = [
    path("admin/", admin.site.urls),
    # Users
    path('users/', views.UserList.as_view()),
    path('user/<int:pk>/', views.UserDetail.as_view()),
    # Categories
    path('categories/', views.WeeklyCategoryList.as_view()),
    path('category/<int:pk>', views.WeeklyCategoryDetail.as_view()),
    # Expenses
    path('expenses/', views.WeeklyExpenseList.as_view()),
    # Monthly Income
    path('income/', views.MonthlyIncomeList.as_view()),
    path('income/<int:pk>', views.MonthlyIncomeDetail.as_view()),
    # Token
    path("token/", TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # LOGIN
    path('auth/', include('rest_framework.urls'))
]

urlpatterns = format_suffix_patterns(urlpatterns)
