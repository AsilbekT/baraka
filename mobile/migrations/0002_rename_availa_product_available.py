# Generated by Django 4.1.1 on 2022-09-19 13:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mobile', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='availa',
            new_name='available',
        ),
    ]
