# Generated by Django 3.1.7 on 2021-03-27 08:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0003_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookinstance',
            name='order_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='in_order_item', to='warehouse.orderitem'),
        ),
    ]
