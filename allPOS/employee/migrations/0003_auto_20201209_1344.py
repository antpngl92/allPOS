# Generated by Django 3.1.4 on 2020-12-09 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0002_auto_20201209_1343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='is_employeed',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
