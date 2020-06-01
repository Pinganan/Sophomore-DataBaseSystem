# Generated by Django 3.0.6 on 2020-05-31 13:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CI',
            fields=[
                ('productName', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('price', models.IntegerField()),
                ('signDate', models.DateField()),
                ('startDate', models.DateField(null=True)),
                ('detectDate', models.DateField(null=True)),
                ('finishDate', models.DateField(null=True)),
                ('content', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='EA',
            fields=[
                ('no', models.IntegerField(primary_key=True, serialize=False)),
                ('ps', models.CharField(max_length=20)),
                ('firstName', models.CharField(max_length=10)),
                ('lastName', models.CharField(max_length=10)),
                ('phone', models.IntegerField(null=True)),
                ('authority', models.CharField(max_length=1)),
                ('flag_leader', models.BooleanField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Rdeal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mysite.EA')),
                ('productName', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mysite.CI')),
            ],
        ),
        migrations.CreateModel(
            name='Mdetect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detectDate', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='ddate', to='mysite.CI')),
                ('productName', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='pname', to='mysite.CI')),
            ],
        ),
    ]
