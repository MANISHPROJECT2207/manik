# Generated by Django 5.0.7 on 2024-08-14 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0010_unit'),
    ]

    operations = [
        migrations.AddField(
            model_name='unit',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]