# Generated by Django 3.0.7 on 2020-06-06 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0009_auto_20200604_1931'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mdetect',
            name='detectDate',
            field=models.DateField(),
        ),
    ]