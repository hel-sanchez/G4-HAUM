# Generated by Django 4.2.4 on 2023-10-31 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0004_alter_pricerange_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pricerange',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]