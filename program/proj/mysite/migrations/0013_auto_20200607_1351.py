# Generated by Django 3.0.7 on 2020-06-07 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0012_auto_20200607_1307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manufacturer',
            name='mphone',
            field=models.BigIntegerField(null=True),
        ),
    ]
