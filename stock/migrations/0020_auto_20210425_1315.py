# Generated by Django 3.1.4 on 2021-04-25 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0019_remove_automatedordering_email_ingredients_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='automatedordering',
            name='email_footer_text',
            field=models.TextField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='automatedordering',
            name='email_greeting_text',
            field=models.TextField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='automatedordering',
            name='email_text',
            field=models.TextField(blank=True, max_length=1000),
        ),
    ]
