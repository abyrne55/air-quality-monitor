# Generated by Django 2.1 on 2018-09-19 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0006_auto_20180917_1654'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sensor',
            name='mylist',
        ),
        migrations.AddField(
            model_name='sensor',
            name='data',
            field=models.ManyToManyField(to='monitor.DataPoint'),
        ),
    ]
