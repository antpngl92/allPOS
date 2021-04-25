from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0008_automatedordering'),
    ]

    operations = [
        migrations.AddField(
            model_name='automatedordering',
            name='email_confirmation',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='automatedordering',
            name='email_text',
            field=models.CharField(default="", max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='automatedordering',
            name='record_orders',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
