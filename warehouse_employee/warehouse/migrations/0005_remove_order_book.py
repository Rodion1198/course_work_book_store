# Generated by Django 3.1.7 on 2021-03-27 08:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0004_bookinstance_order_item'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='book',
        ),
    ]
