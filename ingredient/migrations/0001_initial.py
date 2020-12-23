# Generated by Django 3.1.4 on 2020-12-19 18:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('quantity', models.DecimalField(decimal_places=3, max_digits=4, null=True)),
                ('inventory_ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.inventoryingredient')),
            ],
        ),
    ]
