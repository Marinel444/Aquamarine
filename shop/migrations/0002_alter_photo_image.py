# Generated by Django 4.2.4 on 2023-08-29 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(upload_to='products/%Y/%m/%d/', verbose_name='Attachment'),
        ),
    ]
