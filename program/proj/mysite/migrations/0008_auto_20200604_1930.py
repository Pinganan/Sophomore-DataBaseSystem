# Generated by Django 3.0.7 on 2020-06-04 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0007_auto_20200601_2236'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ci',
            name='detectDate',
        ),
        migrations.AddField(
            model_name='manufacturer',
            name='manufacturer',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
