# Generated by Django 2.1 on 2018-09-19 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0008_auto_20180919_0045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensor',
            name='data',
            field=models.ManyToManyField(blank=True, to='monitor.DataPoint'),
        ),
    ]
