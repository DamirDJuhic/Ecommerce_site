# Generated by Django 3.0 on 2022-01-04 18:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20211227_2010'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='date_order',
            new_name='date_orderd',
        ),
    ]
