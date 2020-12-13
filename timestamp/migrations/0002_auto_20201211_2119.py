# Generated by Django 3.1.4 on 2020-12-11 21:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('timestamp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='timestapm',
            name='datestamp',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='timestapm',
            name='timestamp',
            field=models.TimeField(auto_now_add=True),
        ),
    ]