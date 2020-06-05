from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import EA
from .models import CI
from .models import Manufacturer
import MySQLdb
import datetime
import os

# Create your views here.

def get_EA():
    # os.getcwd()
    path = 'C:\\Users\\user\\Desktop\\proj' + '\\EA.txt'
    print(path)
    
    files = open(path, 'r')
    for sample in files:
        lists = []
        user = EA()
        count = 0
        lists.append(sample.strip().split(" "))
        for item in lists:
            if count == 6:
                user.no = item[0]
                user.ps = item[1]
                user.firstName = item[2]
                user.lastName = item[3]
                user.phone = item[4]
                user.authority = item[5]
                user.flag_leader = item[6]
                user.save()
            else :
                count += 1
    files.close()
get_EA()

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

def BossPage(request):
    bossFirstname = "Ping"
    bossLastname = "-Anan！"
    searchResult = "查詢的結果："
    Mnames = EA.objects.all()
    Enames = EA.objects.all()
    MFnames = Manufacturer.objects.all()
    Pnames = CI.objects.all()
    Results = EA.objects.all()
    return render(request, 'Brank.html', locals())
