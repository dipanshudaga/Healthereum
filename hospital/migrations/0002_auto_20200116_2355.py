# Generated by Django 3.0.2 on 2020-01-16 23:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Medicines',
            new_name='Medicine',
        ),
    ]
