# Generated by Django 3.2.18 on 2023-05-14 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0002_alter_galery_image_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='galery',
            name='image_path',
            field=models.ImageField(upload_to='images/%Y-%m/'),
        ),
    ]
