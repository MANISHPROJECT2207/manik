# Generated by Django 5.0.7 on 2024-08-14 07:01

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0013_unit_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='unit',
            name='completed_by',
            field=models.ManyToManyField(blank=True, related_name='completed_units', to=settings.AUTH_USER_MODEL),
        ),
    ]
