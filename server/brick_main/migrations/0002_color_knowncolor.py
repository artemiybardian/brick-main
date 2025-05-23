# Generated by Django 5.2 on 2025-04-13 11:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brick_main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Цвет',
                'verbose_name_plural': 'Цвета',
                'db_table': 'color',
            },
        ),
        migrations.CreateModel(
            name='KnownColor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='known_in_objects', to='brick_main.color', verbose_name='Цвет')),
                ('obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='known_colors', to='brick_main.obj', verbose_name='Деталь')),
            ],
            options={
                'verbose_name': 'Известный цвет',
                'verbose_name_plural': 'Известные цвета',
                'db_table': 'known_color',
                'indexes': [models.Index(fields=['obj'], name='known_color_obj_id_0bb009_idx'), models.Index(fields=['color'], name='known_color_color_i_197e43_idx')],
                'unique_together': {('obj', 'color')},
            },
        ),
    ]
