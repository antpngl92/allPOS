# Generated by Django 3.1.4 on 2021-03-23 14:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0002_auto_20210126_0952'),
        ('stock', '0004_auto_20210116_0137'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventoryingredient',
            name='supplier',
        ),
        migrations.AddField(
            model_name='inventoryingredient',
            name='supplier',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to='supplier.supplier'
            ),
        ),
    ]
