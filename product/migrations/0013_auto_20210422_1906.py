from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            'ingredient',
            '0007_auto_20210421_2145'
        ),
        (
            'product',
            '0012_product_retail_price'
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='ingredient',
            field=models.ManyToManyField(
                related_name='product',
                to='ingredient.Ingredient'
            ),
        ),

        migrations.AlterField(
            model_name='product',
            name='retail_price',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]
