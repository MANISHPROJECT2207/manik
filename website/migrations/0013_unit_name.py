# Generated by Django 5.0.7 on 2024-08-14 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0012_subject_no_units'),
    ]

    operations = [
        migrations.AddField(
            model_name='unit',
            name='name',
            field=models.CharField(default=None, max_length=255),
        ),
    ]