from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import EA
from .models import CI
import MySQLdb
import datetime

# Create your views here.

def ini_data():
    user = EA()
    user.no = 'andy406031211@gmail.com'
    user.ps = '123456'
    user.firstName = "Ping"
    user.lastName = 'Anan'
    user.phone = '886982804351'
    user.authority = 'R'
    user.flag_leader = 1
    user.save()
    pro = CI()
    pro.productName = "kkkkk"
    pro.price = 1000
    pro.signDate = '1999-9-4'
    pro.finishDate = '1999-12-11'
    pro.content = 'fhsgiuyrhtoierw'
    pro.save()
ini_data()

def RootPage(request) :
    accountChange = ""  
    if request.POST:
        user = EA()
        user.no = request.POST.get('no')
        user.ps = request.POST.get('ps')
        if request.POST.get('phone') :
            user.phone = request.POST.get('phone')
        user.firstName = request.POST.get('fname')
        user.lastName = request.POST.get('lname')
        user.flag_leader = request.POST.get('leader')
        user.authority = request.POST.get('authority')
        add_delete = request.POST.get('add_delete')
        if add_delete == 'delete':
            try:
                EA.objects.get(no=user.no, ps=user.ps).delete()
                accountChange = "delete success"
            except:
                accountChange = "delete faliure"
        elif add_delete == 'update':
            try:
                EA.objects.get(no=user.no)
                user.save()
                accountChange = "update success"
            except:
                accountChange = "update failure"
        else:
            try:
                EA.objects.get(no=user.no)
                accountChange = "insert failure"
            except:
                user.save()
                accountChange = "insert success"
    return  render(request, 'am.html', {'accountChange':accountChange})

def login(request):
    loginMessage=""
    if request.POST:
        user = EA()
        user.no = request.POST.get('uname')
        user.ps = request.POST.get('ps')
        try:
            login = EA.objects.get(no=user.no, ps=user.ps)
            if login.authority == 'R':
                return HttpResponseRedirect("http://127.0.0.1:8000/Srank/")
        except:
            loginMessage = 'login failure'
    return render(request, 'login.html', {'loginMessage':loginMessage})

def graph(request):
    lists = []
    mins = CI.objects.all().values('finishDate')
    lists.append(mins)
    return render(request, 'others.html', {'mins':lists})
