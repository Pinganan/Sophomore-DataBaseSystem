"""proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from mysite import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Srank/', views.RootPage),
    path('Brank/', views.BossPage),
    path('Nrank/', views.NormalPage),
    path('Nrank/detect/', views.DetectPage),
    path('Nrank/employee/', views.EmployeePage),
    path('others/', views.graph),
    path('Mrank/', views.ManagerPage),
    path('testt/', views.test),
    path('', views.login),
    path('Mrank/detect/', views.DetectPage),
    path('Mrank/employee/', views.EmployeePage),
    path('M_insert/', views.M_insertPage),
]
