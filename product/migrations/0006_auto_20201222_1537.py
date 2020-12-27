# Generated by Django 3.1.4 on 2020-12-22 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_auto_20201222_1536'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='foodallergenlabels',
            name='for_product',
        ),
        migrations.AddField(
            model_name='product',
            name='food_allergen_labels',
            field=models.ManyToManyField(to='product.FoodAllergenLabels'),
        ),
    ]