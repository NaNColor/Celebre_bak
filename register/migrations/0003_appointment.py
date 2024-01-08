# Generated by Django 3.2.18 on 2023-04-23 15:33

from django.db import migrations, models
import django.db.models.deletion
import register.models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0002_workschedule'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default=register.models.get_default_my_date, max_length=255, verbose_name='Обозначение')),
                ('client_name', models.CharField(max_length=255, verbose_name='Имя')),
                ('client_patronymic', models.CharField(default='', max_length=255, verbose_name='Отчество')),
                ('client_phone', models.CharField(max_length=13, verbose_name='Номер телефона')),
                ('appointment_reg_date', models.DateTimeField(auto_now_add=True)),
                ('appointment_date', models.DateField(blank=True, null=True, verbose_name='Дата записи')),
                ('appointment_beg_date', models.TimeField(verbose_name='Начало')),
                ('appointment_end_date', models.TimeField(verbose_name='Конец')),
                ('proof', models.BooleanField(default=False, verbose_name='Подтверждено')),
                ('address', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='register.address', verbose_name='Адрес')),
                ('option', models.ForeignKey(default=None, on_delete=django.db.models.deletion.SET_DEFAULT, to='register.option', verbose_name='Услуга')),
                ('stylist', models.ForeignKey(default=None, on_delete=django.db.models.deletion.SET_DEFAULT, to='register.stylist', verbose_name='Стилист')),
            ],
        ),
    ]
