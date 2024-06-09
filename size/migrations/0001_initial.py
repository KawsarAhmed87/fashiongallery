# Generated by Django 5.0.4 on 2024-05-20 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=30, null=True, unique=True)),
                ('created_date', models.DateField(auto_now_add=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
