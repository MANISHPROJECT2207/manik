# Generated by Django 5.1 on 2024-08-30 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_subject_full_name_alter_subject_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='name',
            field=models.CharField(max_length=12),
        ),
    ]
