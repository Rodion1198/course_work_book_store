# Generated by Django 3.1.7 on 2021-03-17 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='book',
        ),
        migrations.AddField(
            model_name='cart',
            name='books',
            field=models.ManyToManyField(blank=True, related_name='related_cart', to='store.CartProduct'),
        ),
        migrations.AddField(
            model_name='cart',
            name='for_anonymous_user',
            field=models.BooleanField(default=False),
        ),
    ]
