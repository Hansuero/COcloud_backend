# Generated by Django 4.2.4 on 2023-08-28 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
