# Generated by Django 5.1 on 2024-08-30 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_subject_codes'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='full_name',
            field=models.CharField(blank=True, max_length=55, null=True),
        ),
        migrations.AlterField(
            model_name='subject',
            name='name',
            field=models.CharField(max_length=8),
        ),
    ]
