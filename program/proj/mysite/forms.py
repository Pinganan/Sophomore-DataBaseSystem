from django import forms
from django.forms import fields
from django.forms import widgets
from mysite import models

pname_q=[(c.productName, c.productName) for c in models.CI.objects.all()]
mname_q=[(e.firstName, e.firstName) for e in models.EA.objects.filter(authority='M')]
ename_q=[(e.firstName, e.firstName) for e in models.EA.objects.all()]
price_q=[(0,'None'),(1,'1~10'),(10,'10~100'),(100,'100~1000'),(1000,'1000~10000')]
mfname_q=[(m.manufacturer, m.manufacturer) for m in models.Manufacturer.objects.all()]
eno_q=[(e.no, e.no) for e in models.EA.objects.all()]
enoreplace_q=[(e.no, e.no) for e in models.EA.objects.all()]
noselect=[('', 'None')]
class SearchForm(forms.Form):
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
    eno = fields.ChoiceField(
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
        self.fields["eno"].choices = eno_q

class IForm(forms.Form):
    pname = fields.ChoiceField(
        choices = [],
        widget = widgets.Select,
        required=True,
    )
    eno = fields.ChoiceField(
        choices = [],
        widget = widgets.Select,
        required=True,
    )
    def __init__(self,*args,**kwargs):
        super(IForm, self).__init__(*args,**kwargs)
        self.fields["pname"].choices = pname_q
        self.fields["eno"].choices = eno_q
class RForm(forms.Form):
    pname = fields.ChoiceField(
        choices = [],
        widget = widgets.Select,
        required=True,
    )
    eno = fields.ChoiceField(
        choices = [],
        widget = widgets.Select,
        required=True,
    )
    enoreplace = fields.ChoiceField(
        choices = [],
        widget = widgets.Select,
        required=True,
    )
    def __init__(self,*args,**kwargs):
        super(RForm, self).__init__(*args,**kwargs)
        self.fields["pname"].choices = pname_q
        self.fields["eno"].choices = eno_q
        self.fields["enoreplace"].choices = enoreplace_q


class DetectForm(forms.Form):
    pname = fields.ChoiceField(
        choices = [],
        widget = widgets.Select,
        required=True,
    )
    def __init__(self,*args,**kwargs):
        super(DetectForm, self).__init__(*args,**kwargs)
        self.fields["pname"].choices = pname_q