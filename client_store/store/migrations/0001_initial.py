# Generated by Django 3.1.7 on 2021-03-17 17:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, verbose_name='first name')),
                ('last_name', models.CharField(max_length=100, verbose_name='last name')),
                ('bio', models.TextField(blank=True, verbose_name='bio')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='date of birth')),
                ('date_of_death', models.DateField(blank=True, null=True, verbose_name='date of death')),
            ],
            options={
                'ordering': ['last_name', 'first_name'],
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('publication_year', models.IntegerField(verbose_name='year')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('price', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='price')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.author')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_products', models.PositiveIntegerField(default=0)),
                ('final_price', models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='?????????? ????????')),
                ('in_order', models.BooleanField(default=False)),
                ('book', models.ManyToManyField(blank=True, to='store.Book')),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='name')),
            ],
        ),
        migrations.CreateModel(
            name='PublishingHouse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('info', models.TextField(blank=True, verbose_name='info')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='?????????? ????????????????')),
                ('address', models.CharField(blank=True, max_length=255, null=True, verbose_name='??????????')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='????????????????????????')),
            ],
        ),
        migrations.CreateModel(
            name='CartProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.PositiveIntegerField(default=1)),
                ('final_price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='?????????? ????????')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.book', verbose_name='??????????')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_products', to='store.cart', verbose_name='??????????????')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.customer', verbose_name='????????????????????')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.customer', verbose_name='????????????????'),
        ),
        migrations.AddField(
            model_name='book',
            name='genre',
            field=models.ManyToManyField(blank=True, to='store.Genre', verbose_name='genre'),
        ),
        migrations.AddField(
            model_name='book',
            name='publishing_house',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.publishinghouse'),
        ),
    ]
