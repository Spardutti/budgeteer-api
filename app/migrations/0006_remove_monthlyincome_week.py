# Generated by Django 4.1.3 on 2022-12-13 16:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_weeklycategory_amount_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='monthlyincome',
            name='week',
        ),
    ]
