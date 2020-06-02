from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import EA
import MySQLdb

# Create your views here.

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
    return render(request, 'login.html', {})