# Generated by Django 3.2.4 on 2021-06-23 19:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodConnect', '0009_auto_20210623_0937'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restauranttrail',
            name='review_id',
        ),
    ]
