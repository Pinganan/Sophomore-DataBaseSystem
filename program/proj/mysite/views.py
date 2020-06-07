from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import EA, CI, Rdeal, Mdetect, Manufacturer
import MySQLdb
import datetime
import os
from django.db import connection
from .forms import SearchForm

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

    path = 'C:\\Users\\user\\Desktop\\proj' + '\\Manufacturer.txt'    # Manufacturer data
    files = open(path, 'r')
    for sample in files:
        lists = []
        lists.append(sample.strip().split(" "))
        try:
            Manufacturer.objects.get(manufacturer=lists[0][0], productName=lists[0][1], partnerName=lists[0][2], mphone=lists[0][3])
        except:
            partner = Manufacturer()
            partner.manufacturer = lists[0][0]
            partner.productName = CI.objects.get(productName=lists[0][1])
            partner.partnerName = lists[0][2]
            partner.mphone = lists[0][3]
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
        global account
        account = user.no
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
    form = SearchForm()
    checkprint = [True, True, True, True, True, True]
    Mnames = EA.objects.all()
    Enames = EA.objects.all()
    MFnames = Manufacturer.objects.all()
    Pnames = CI.objects.all()
    choice = 'select productName, firstName, lastName, no, phone, price, signDate, startDate, finishDate, manufacturer, partnerName, mphone, content '
    choice += 'from mysite_EA, mysite_CI, mysite_Rdeal, mysite_Manufacturer '
    choice += 'where mysite_EA.no = mysite_Rdeal.no_id and mysite_CI.productName = mysite_Rdeal.productName_id and mysite_Manufacturer.productName_id = mysite_CI.productName and mysite_EA.authority = "M" '
    if request.POST:
        checklist = request.POST.getlist('P')
        control(checkprint, checklist)
        sform = SearchForm(request.POST) # form 包含提交的数据

        if sform.is_valid():# 如果提交的数据合法
            pname = sform.cleaned_data['pname']
            if pname != "":
                choice += " and productName=\'" + pname + "\'"
            mname = sform.cleaned_data['mname']
            if mname != "":
                choice += ' and firstName=\"' + mname + '\"'
            price = sform.cleaned_data['price']
            if price == '1':
                choice += ' and price <= 10 and price > 0'
            elif price == '10':
                choice += ' and price <= 100 and price >10'
            elif price == '100':
                choice += 'and price <= 1000 and price >100'
            elif price == '1000':
                choice += ' and price <= 10000 and price >1000'
            mfname = sform.cleaned_data['mfname']
            if mfname != "":
                choice += ' and manufacturer=\"' + mfname + '\"'
        else:
            print(sform.errors)
        
        with connection.cursor() as cursor:
            cursor.execute(choice)
            Results = cursor.fetchall()
    return render(request, 'Brank.html', locals())

def test(request):
    # EA.objects.filter(authority='N').select_related().values()

    return render(request, 'testt.html', locals())

def ManagerPage(request):
    return render(request, 'Mrank.html', locals())

def NormalPage(request):
    form = SearchForm()
    searchResult = ""
    checkprint = [True, True, True, True, True, True, True]
    # Results = CI.objects.all()
    if request.POST:
        if request.POST.get('insertp'):
            searchResult = "新增的結果："
            pname = request.POST.get('insertp')
            date = request.POST.get('insertd')
            print(pname)
            try:
                Mdetect.objects.get(productName=pname, detectDate=date)
            except:
                detect = Mdetect()
                detect.productName = CI.objects.get(productName=pname)
                detect.detectDate = date
                detect.save()
                with connection.cursor() as cursor:
                    choice = 'select productName, firstName, lastName, no, phone, price, signDate, startDate, finishDate, manufacturer, partnerName, mphone, content '
                    choice += 'from mysite_EA, mysite_CI, mysite_Rdeal, mysite_Manufacturer '
                    choice += 'where mysite_EA.no = mysite_Rdeal.no_id and mysite_CI.productName = mysite_Rdeal.productName_id and mysite_Manufacturer.productName_id = mysite_CI.productName and mysite_EA.authority = "M" and mysite_CI.productName = \"' + pname + '\"'
                    cursor.execute(choice)
                    Results = cursor.fetchall()
        else:
            checklist = request.POST.getlist('P')
            print(checklist)
            searchResult = "查詢的結果："
            control(checkprint, checklist)
            if 'p_employee' not in checklist:
                checkprint[6] = False
            sform = SearchForm(request.POST) # form 包含提交的数据
            
            if sform.is_valid():# 如果提交的数据合法
                choice = 'select productName, firstName, lastName, no, phone, price, signDate, startDate, finishDate, manufacturer, partnerName, mphone, content '
                choice += 'from mysite_EA, mysite_CI, mysite_Rdeal, mysite_Manufacturer '
                choice += 'where mysite_EA.no = mysite_Rdeal.no_id and mysite_CI.productName = mysite_Rdeal.productName_id and mysite_Manufacturer.productName_id = mysite_CI.productName and mysite_EA.authority = "N" '
                global account
                choice += ' and mysite_EA.no=\"' + account + '\"'
                print(choice)
                
                pname = sform.cleaned_data['pname']
                if pname != "":
                    choice += " and productName=\'" + pname + "\'"
                price = sform.cleaned_data['price']
                if price == '1':
                    choice += ' and price <= 10 and price > 0'
                elif price == '10':
                    choice += ' and price <= 100 and price >10'
                elif price == '100':
                    choice += 'and price <= 1000 and price >100'
                elif price == '1000':
                    choice += ' and price <= 10000 and price >1000'
                mfname = sform.cleaned_data['mfname']
                if mfname != "":
                    choice += ' and manufacturer=\"' + mfname + '\"'
                date1 = request.POST.get('date1')
                date2 = request.POST.get('date2')
                if date1 !="":
                    choice += ' and mysite_CI.signDate < 2008-2-11'
            else:
                print(sform.errors)
        with connection.cursor() as cursor:
            cursor.execute(choice)
            Results = cursor.fetchall()
    return render(request, 'Nrank.html', locals())

def DetectPage(request):
    if request.POST:
        d_pname = request.POST.get('d_pname')
        result = Mdetect.objects.filter(productName = d_pname)
    return render(request, 'detect.html', locals())

def EmployeePage(request):
    if request.POST:
        d_pname = request.POST.get('d_pname')
        with connection.cursor() as cursor:
            choice = 'select firstName, lastName, no, phone '
            choice += 'from mysite_EA, mysite_Rdeal '
            choice += 'where mysite_EA.no = mysite_Rdeal.no_id and mysite_Rdeal.productName_id = \"' + d_pname + '\"'
            cursor.execute(choice)
            result = cursor.fetchall()
    return render(request, 'employee.html', locals())