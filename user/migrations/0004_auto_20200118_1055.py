# Generated by Django 3.0.2 on 2020-01-18 10:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hospital', '0018_auto_20200118_1055'),
        ('user', '0003_auto_20200118_0834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital.City'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='hospital',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital.Hospital'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='skills',
            field=models.ManyToManyField(to='user.Specialization'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='patient',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
