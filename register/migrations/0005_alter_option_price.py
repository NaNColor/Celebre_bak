# Generated by Django 3.2.18 on 2023-04-25 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0004_blocks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='option',
            name='price',
            field=models.IntegerField(verbose_name='Начальная цена'),
        ),
    ]
