from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import EA

# Create your views here.

def RootPage(request) :
    return  render(request, 'am.html')

def add_Account(request):
    user = EA()
    user.authority = 'N'
    number = request.POST.get('no')
    user.no = number
    user.firstName = request.POST.get('fname')
    user.lastName = request.POST.get('lname')
    if request.POST.get('phone') != '':
        user.phone = request.POST.get('phone')
    user.ps = request.POST.get('ps')
    print(user.no)
    user.save()
    return HttpResponseRedirect('http://127.0.0.1:8000/Srank/')