# Generated by Django 3.1.4 on 2021-04-25 13:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0024_inventoryingredient_email_sent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventoryingredient',
            name='email_sent',
        ),
    ]