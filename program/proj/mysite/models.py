from django.db import models
from django.http import HttpResponse
# Create your models here.

class EA(models.Model):
    no          = models.EmailField(primary_key=True)
    ps          = models.CharField(max_length=20)
    firstName   = models.CharField(max_length=10)
    lastName    = models.CharField(max_length=10)
    phone       = models.BigIntegerField(null=True, default=0)
    authority   = models.CharField(max_length=1)
    flag_leader = models.BooleanField(default=0)

class CI(models.Model):
    productName = models.CharField(primary_key=True, max_length=15)
    price       = models.IntegerField()
    signDate    = models.DateField()
    startDate   = models.DateField(null=True)
    finishDate  = models.DateField(null=True)
    content     = models.TextField()

class Rdeal(models.Model):
    no          = models.ForeignKey(EA, on_delete=models.PROTECT)
    productName = models.ForeignKey(CI, on_delete=models.PROTECT)

class Mdetect(models.Model):
    productName = models.ForeignKey(CI, on_delete=models.PROTECT, related_name='pname')
    detectDate  = models.ForeignKey(CI, on_delete=models.PROTECT, related_name='ddate')

class Manufacturer(models.Model):
    manufacturer= models.CharField(max_length=20, default="squirrel")
    productName = models.ForeignKey(CI, on_delete=models.PROTECT, related_name='man_name')
    partnerName = models.CharField(max_length=20)
    phone       = models.IntegerField()