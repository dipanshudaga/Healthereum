# Generated by Django 3.0.2 on 2020-01-17 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='skills',
        ),
        migrations.AddField(
            model_name='doctor',
            name='skills',
            field=models.ManyToManyField(to='user.Specialization'),
        ),
    ]
