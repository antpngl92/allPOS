# Generated by Django 3.1.4 on 2021-04-25 11:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0005_remove_orderemail_ingredients'),
        ('stock', '0013_auto_20210425_1149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventoryingredient',
            name='email_sent',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name='ingredients',
                to='emails.orderemail'
            ),
        ),
    ]
