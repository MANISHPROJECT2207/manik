# Generated by Django 5.0.7 on 2024-08-14 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0011_unit_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='no_units',
            field=models.IntegerField(default=1),
        ),
    ]
