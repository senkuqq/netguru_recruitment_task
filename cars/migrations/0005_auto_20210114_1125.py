# Generated by Django 3.1.5 on 2021-01-14 10:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0004_car_make'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='car',
            unique_together={('name', 'make')},
        ),
    ]
