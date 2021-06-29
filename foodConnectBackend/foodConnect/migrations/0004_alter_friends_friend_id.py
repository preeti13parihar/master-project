# Generated by Django 3.2.4 on 2021-06-23 08:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodConnect', '0003_alter_friends_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friends',
            name='friend_id',
            field=models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, related_name='friend_of', to='foodConnect.customer'),
        ),
    ]