# Generated by Django 3.1.4 on 2020-12-22 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_auto_20201222_1551'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodallergenlabels',
            name='name',
            field=models.CharField(default=12, max_length=20),
            preserve_default=False,
        ),
    ]
