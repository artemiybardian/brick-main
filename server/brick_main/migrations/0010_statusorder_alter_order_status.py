# Generated by Django 5.2 on 2025-04-18 20:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brick_main', '0009_order_orderitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='Statusorder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Статус Заказ',
                'verbose_name_plural': 'Статус Заказ',
                'db_table': 'status_order',
            },
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='brick_main.statusorder', verbose_name='Статус'),
        ),
    ]
