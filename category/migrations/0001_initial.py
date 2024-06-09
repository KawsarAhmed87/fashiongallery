# Generated by Django 5.0.4 on 2024-05-20 04:24

import category.validation
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=100, null=True, unique=True)),
                ('featured', models.BooleanField(default=False)),
                ('image', models.ImageField(blank=True, null=True, upload_to='category/', validators=[category.validation.validate_image])),
                ('created_date', models.DateField(auto_now_add=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
