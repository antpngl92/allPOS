# Generated by Django 3.1.4 on 2021-04-25 11:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0004_auto_20210425_1112'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderemail',
            name='ingredients',
        ),
    ]