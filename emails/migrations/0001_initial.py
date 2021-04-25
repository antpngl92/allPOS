# Generated by Django 3.1.4 on 2021-04-24 21:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stock', '0009_auto_20210424_2107'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderEmail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('ingredients', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='stock.inventoryingredient')),
            ],
        ),
    ]
