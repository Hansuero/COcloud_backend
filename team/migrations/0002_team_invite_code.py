# Generated by Django 4.2.4 on 2023-08-26 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='invite_code',
            field=models.CharField(default=0, max_length=16, verbose_name='邀请码'),
            preserve_default=False,
        ),
    ]
