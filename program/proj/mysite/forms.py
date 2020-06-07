from django import forms
from django.forms import fields
from django.forms import widgets
from mysite import models

pname_q=[(c.productName, c.productName) for c in models.CI.objects.all()]
mname_q=[(e.firstName, e.firstName) for e in models.EA.objects.filter(authority='M')]
ename_q=[(e.firstName, e.firstName) for e in models.EA.objects.all()]
price_q=[(0,'None'),(1,'1~10'),(10,'10~100'),(100,'100~1000'),(1000,'1000~10000')]
mfname_q=[(m.manufacturer, m.manufacturer) for m in models.Manufacturer.objects.all()]
noselect=[('', 'None')]
class SearchForm(forms.Form):
    # a = models.CI.objects.values_list("productName","productName")
    pname = fields.ChoiceField(
        choices = [],
        widget = widgets.Select,
        required=False,
    )
    mname = fields.ChoiceField(
        choices = [],
        widget = widgets.Select,
        required=False,
    )
    ename = fields.ChoiceField(
        choices = [],
        widget = widgets.Select,
        required=False,
    )
    price = fields.ChoiceField(
        choices = [],
        widget = widgets.Select,
        required=False,
    )
    mfname = fields.ChoiceField(
        choices = [],
        widget = widgets.Select,
        required=False,
    )
    def __init__(self,*args,**kwargs):
        super(SearchForm, self).__init__(*args,**kwargs)
        self.fields["pname"].choices = noselect + pname_q
        self.fields["mname"].choices = noselect + mname_q
        self.fields["ename"].choices = noselect + ename_q
        self.fields["price"].choices = price_q
        self.fields["mfname"].choices = noselect + mfname_q