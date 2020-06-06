from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import EA, CI, Rdeal, Mdetect, Manufacturer
import MySQLdb
import datetime
import os

# Create your views here.
# print(os.getcwd())

def get_inidata():
    path = 'C:\\Users\\user\\Desktop\\proj' + '\\EA.txt'    #EA data
    files = open(path, 'r')
    for sample in files:
        lists = []
        user = EA()
        count = 0
        lists.append(sample.strip().split(" "))
        for item in lists:
            user.no = item[0]
            user.ps = item[1]
            user.firstName = item[2]
            user.lastName = item[3]
            user.phone = item[4]
            user.authority = item[5]
            user.flag_leader = item[6]
            user.save()
    files.close()

    path = 'C:\\Users\\user\\Desktop\\proj' + '\\CI.txt'     #CI data
    files = open(path, "r")
    for sample in files:
        lists = []
        lists.append(sample.strip().split(" "))
        product = CI()
        for item in lists:
            product.productName = item[0]
            product.price = item[1]
            product.signDate = item[2]
            product.startDate = item[3]
            product.finishDate = item[4]
            product.content = "123456789"
            product.save()
    files.close()

    path = 'C:\\Users\\user\\Desktop\\proj' + '\\Rdeal.txt'  #Relation data between EA & CI
    files = open(path, 'r')
    for sample in files:
        lists = []
        lists.append(sample.strip().split(" "))
        try:
            Rdeal.objects.get(no=lists[0][0], productName=lists[0][1])
        except:
            deal = Rdeal()
            deal.no = EA.objects.get(no=lists[0][0])
            deal.productName = CI.objects.get(productName=lists[0][1])
            deal.save()
    files.close()

    path = 'C:\\Users\\user\\Desktop\\proj' + '\\Mdetect.txt'    # multivalue data of detect date
    files = open(path, 'r')
    for sample in files:
        lists = []
        lists.append(sample.strip().split(" "))
        try:
            Mdetect.objects.get(productName=lists[0][0], detectDate=lists[0][1])
        except:
            detect = Mdetect()
            detect.productName = CI.objects.get(productName=lists[0][0])
            detect.detectDate = productName=lists[0][1]
            detect.save()
    files.close()

    path = 'C:\\Users\\user\\Desktop\\proj' + '\\Manufacturer.txt'    # multivalue data of detect date
    files = open(path, 'r')
    for sample in files:
        lists = []
        lists.append(sample.strip().split(" "))
        try:
            Manufacturer.objects.get(manufacturer=lists[0][0], productName=lists[0][1], partnerName=lists[0][2], phone=lists[0][3])
        except:
            partner = Manufacturer()
            partner.manufacturer = lists[0][0]
            partner.productName = CI.objects.get(productName=lists[0][1])
            partner.partnerName = lists[0][2]
            partner.phone = lists[0][3]
            partner.save()
    files.close()
get_inidata()


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
            elif login.authority == 'B':
                return HttpResponseRedirect("http://127.0.0.1:8000/Brank/")
            elif login.authority == 'M':
                return HttpResponseRedirect("http://127.0.0.1:8000/Mrank/")
            elif login.authority == 'N':
                return HttpResponseRedirect("http://127.0.0.1:8000/Nrank/")
        except:
            loginMessage = 'login failure'
    return render(request, 'login.html', {'loginMessage':loginMessage})

def graph(request):
    lists = []
    mins = CI.objects.all().values('finishDate')
    lists.append(mins)
    return render(request, 'others.html', {'mins':lists})

def control(check, checklist):
    if 'p_pname' not in checklist:
        check[0] = False
    if 'p_mname' not in checklist:
        check[1] = False
    if 'p_price' not in checklist:
        check[2] = False
    if 'p_date' not in checklist:
        check[3] = False
    if 'p_manufacturer' not in checklist:
        check[4] = False
    if 'p_content' not in checklist:
        check[5] = False

def BossPage(request):
    bossFirstname = "Ping"
    bossLastname = "-Anan！"
    searchResult = "查詢的結果："
    checkprint = [True, True, True, True, True, True]
    if request.POST:
        checklist = request.POST.getlist('P')
        control(checkprint, checklist)
        Mnames = EA.objects.all()
        Enames = EA.objects.all()
        MFnames = Manufacturer.objects.all()
        Pnames = CI.objects.all()
        Results = EA.objects.all()
    return render(request, 'Brank.html', locals())


from django.db import connection

def test(request):
    # EA.objects.filter(authority='N').select_related().values()

    with connection.cursor() as cursor:
        cursor.execute('select distinct firstName, lastName, partnerName from mysite_ea as e, mysite_rdeal as r, mysite_manufacturer as m where m.productName_id=r.productName_id and r.no_id=e.no and authority="M"')
        result = cursor.fetchall()
    return render(request, 'testt.html', locals())