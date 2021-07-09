# Generated by Django 3.2.4 on 2021-07-08 22:02

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviews',
            name='review_id',
            field=models.UUIDField(default=uuid.UUID('400874f5-b943-4186-a7fa-c08cd17bb324'), editable=False, primary_key=True, serialize=False),
        ),
    ]
