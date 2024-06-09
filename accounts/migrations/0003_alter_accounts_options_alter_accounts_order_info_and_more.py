# Generated by Django 5.0.4 on 2024-05-21 10:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_initial'),
        ('order', '0002_initial'),
        ('purchase', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='accounts',
            options={'ordering': ['-date'], 'verbose_name': 'Account Entry', 'verbose_name_plural': 'Account Entries'},
        ),
        migrations.AlterField(
            model_name='accounts',
            name='order_info',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='order', to='order.order'),
        ),
        migrations.AlterField(
            model_name='accounts',
            name='purchase_info',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='purchase', to='purchase.purchase'),
        ),
    ]
