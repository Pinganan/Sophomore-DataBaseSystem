# Generated by Django 3.0.6 on 2020-05-31 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ea',
            name='phone',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
