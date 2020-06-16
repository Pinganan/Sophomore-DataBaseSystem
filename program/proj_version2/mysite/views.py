from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import EA, CI, Rdeal, Mdetect, Manufacturer
import MySQLdb
import datetime
import os
from django.db import connection
from .forms import SearchForm
from .forms import RForm
from .forms import IForm
from .forms import DetectForm

# Create your views here.
# print(os.getcwd())

def get_inidata():
    path = 'C:\\Users\\User\\Desktop\\proj_version2' + '\\EA.txt'    #EA data
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

    path = 'C:\\Users\\User\\Desktop\\proj_version2' + '\\CI.txt'     #CI data
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

    path = 'C:\\Users\\User\\Desktop\\proj_version2' + '\\Rdeal.txt'  #Relation data between EA & CI
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

    path = 'C:\\Users\\User\\Desktop\\proj_version2' + '\\Mdetect.txt'    # multivalue data of detect date
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

    path = 'C:\\Users\\User\\Desktop\\proj_version2' + '\\Manufacturer.txt'    # Manufacturer data
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
                try:
                    user.save()
                    accountChange = "insert success"
                except:
                    accountChange = "insert failure"
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
    money = []
    python2json = {}
    mins = CI.objects.all().values('finishDate').order_by('finishDate')
    moneys = CI.objects.all().values('price').order_by('finishDate')
    for r in mins:
        strs = r.get('finishDate')
        lists.append(strs.year)
    for m in moneys:
        money.append(m.get("price"))

    return render(request, 'others.html', locals())

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
    form = SearchForm()
    searchResult = ""
    checkprint = [True, True, True, True, True, True, True]
    # Results = CI.objects.all()
    if request.POST:
        checklist = request.POST.getlist('P')
        control(checkprint, checklist)
        searchResult = "查詢的結果："
        if 'p_employee' not in checklist:
            checkprint[6] = False
        sform = SearchForm(request.POST)
        if sform.is_valid():# 如果提交的数据合法
            choice = 'select productName, firstName, lastName, no, phone, price, signDate, startDate, finishDate, manufacturer, partnerName, mphone, content '
            choice += 'from mysite_EA, mysite_CI, mysite_Rdeal, mysite_Manufacturer '
            choice += 'where mysite_EA.no = mysite_Rdeal.no_id and mysite_CI.productName = mysite_Rdeal.productName_id and mysite_Manufacturer.productName_id = mysite_CI.productName and mysite_EA.authority = "M" '        
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
            if date1 != "":
                choice += ' and mysite_CI.signDate > \"' + date1 + '\"'
                choice += ' and mysite_CI.finishDate < \"' + date2 + '\"'
            global account
            choice += ' and mysite_ci.productName in ( select productName from mysite_ea, mysite_rdeal, mysite_ci where mysite_rdeal.no_id=\"' +  account  + '\" and mysite_rdeal.productName_id=mysite_ci.productName)'
        else:
            print(sform.errors)
        with connection.cursor() as cursor:
            cursor.execute(choice)
            Results = cursor.fetchall()
    return render(request, 'Mrank.html', locals())

def NormalPage(request):
    form = SearchForm()
    global account
    # formD = DetectForm()
    searchResult = ""
    Nrank_insertDate=""
    choice = ""
    checkprint = [True, True, True, True, True, True, True]
    # Results = CI.objects.all()
    if request.POST:
        if request.POST.get('insertp'):
            searchResult = "新增的結果："
            pname = request.POST.get('insertp')
            date = request.POST.get('insertd')
            try:
                CI.objects.get(productName=pname)
                try:
                    Rdeal.objects.get(no=account, productName=pname)
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
                    Nrank_insertDate = " insert success "
                except:
                    Nrank_insertDate = " insert failure "
                    return render(request, 'Nrank.html', locals())
            except:
                Nrank_insertDate = " insert failure "
                return render(request, 'Nrank.html', locals())
        else:
            checklist = request.POST.getlist('P')
            searchResult = "查詢的結果："
            control(checkprint, checklist)
            if 'p_employee' not in checklist:
                checkprint[6] = False

            sform = SearchForm(request.POST) # form 包含提交的数据
            if sform.is_valid():# 如果提交的数据合法
                choice = 'select productName, firstName, lastName, no, phone, price, signDate, startDate, finishDate, manufacturer, partnerName, mphone, content '
                choice += 'from mysite_EA, mysite_CI, mysite_Rdeal, mysite_Manufacturer '
                choice += 'where mysite_EA.no = mysite_Rdeal.no_id and mysite_CI.productName = mysite_Rdeal.productName_id and mysite_Manufacturer.productName_id = mysite_CI.productName and mysite_EA.authority = "M" '
                
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
                choice += ' and mysite_ci.productName in ( select productName from mysite_ea, mysite_rdeal, mysite_ci where mysite_rdeal.no_id=\"' +  account  + '\" and mysite_rdeal.productName_id=mysite_ci.productName)'
            else:
                print(sform.errors)
        with connection.cursor() as cursor:
            cursor.execute(choice)
            Results = cursor.fetchall()
    return render(request, 'Nrank.html', locals())

def DetectPage(request):
    if request.POST:
        d_pname = request.POST.get('d_pname')
        result = Mdetect.objects.filter(productName=d_pname).values('detectDate').order_by('detectDate')
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

def M_insertPage(request):
    global account
    no = account
    judge = request.POST.get('judge')
    form = IForm()
    Rform = RForm()
    sform = IForm(request.POST)
    rform = RForm(request.POST)
    insertfMessage = ""
    inserteMessage = ""
    replaceMessage = ""
    updateMessage = ""
    if request.POST:
        if request.POST.get('mfname','') != '' and judge == '1':
            pro = CI()
            pname = request.POST.get('pname')
            try:
                CI.objects.get(productName=pname)
                insertfMessage = "insert failure"
            except:
                if pname !="":
                    pro.productName = pname
                price = request.POST.get('price')
                pro.price = price
                signd = request.POST.get('signd')
                if signd != "":
                    pro.signDate = signd
                startd = request.POST.get('startd')
                if startd != "":
                    pro.startDate = startd
                finishd = request.POST.get('finishd')
                if finishd != "":
                    pro.finishDate = finishd
                pro.content = '123456789'
                pro.save()

                man = Manufacturer()
                man.productName = CI.objects.get(productName=pname)
                mfname = request.POST.get('mfname')
                if mfname != "":
                    man.manufacturer = mfname
                mpname = request.POST.get('mpname')
                if mpname != "":
                    man.partnerName = mpname
                mfphone = request.POST.get('mfphone')
                if mfphone != "":
                    man.phone = mfphone
                man.save()

                deal = Rdeal()
                deal.no = EA.objects.get(no=no)
                deal.productName = CI.objects.get(productName=pname)
                deal.save()
                insertfMessage = "insert success"

                print('pname: '+pname)
                print('price: '+price)
                print('signd: '+signd)
                print('startd: '+startd)
                print('finishd: '+finishd)
                print('mfname: '+mfname)
                print('mpname: '+mpname)
                print('mfphone: '+mfphone)
        elif sform.is_valid() and judge == '2':
            eno = sform.cleaned_data['eno']
            pname = sform.cleaned_data['pname']
            print('eno: '+eno)
            print('pname: '+pname)

            deal = Rdeal()
            deal.no = EA.objects.get(no=eno)
            deal.productName = CI.objects.get(productName=pname)
            try:
                Rdeal.objects.get(no=eno, productName=pname)
                inserteMessage = "insert failure"
            except:
                try:
                    Rdeal.objects.get(no=account, productName=pname)
                    deal.save()
                    inserteMessage = "insert success"
                except:
                    inserteMessage = "insert failure"
        elif rform.is_valid() and judge == '4':
            pname = rform.cleaned_data['pname']
            eno = rform.cleaned_data['eno']
            enonew = rform.cleaned_data['enonew']
            try:
                deal = Rdeal.objects.get(no=eno, productName=pname)
                deal.no = EA.objects.get(no=enonew)
                deal.save()
                replaceMessage = "replace success"
            except:
                replaceMessage = "replace failure"
            print('pname: '+pname)
            print('eno: '+eno)
            print('enonew: ' + enonew)
        else:
            man = Manufacturer()
            pname = request.POST.get('u_pname')
            price = request.POST.get('u_price','')
            startd = request.POST.get('u_startd')
            finishd = request.POST.get('u_finishd')
            mpname = request.POST.get('u_mpname')
            mfphone = request.POST.get('u_mfphone')
            try:
                pro = CI.objects.get(productName=pname)
                pro.price = price
                pro.startDate = startd
                pro.finishDate = finishd
                try:
                    man = CI.objects.get(productName=pname)
                    man.partnerName = mpname
                    man.phone = mfphone
                    man.save()
                    pro.save()
                    updateMessage = "update success"
                except:
                    updateMessage = "update failure"
            except:
                updateMessage = "update failure"

    return render(request, 'M_insert.html', locals())