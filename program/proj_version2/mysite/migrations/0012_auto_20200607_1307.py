# Generated by Django 3.0.7 on 2020-06-07 05:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0011_auto_20200606_1632'),
    ]

    operations = [
        migrations.RenameField(
            model_name='manufacturer',
            old_name='phone',
            new_name='mphone',
        ),
    ]
