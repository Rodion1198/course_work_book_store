# Generated by Django 3.1.7 on 2021-04-14 11:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_order_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='price',
        ),
    ]
