# Generated by Django 2.2.8 on 2020-07-07 19:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20200707_1922'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='quantity',
        ),
    ]