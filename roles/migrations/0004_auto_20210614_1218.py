# Generated by Django 3.1.7 on 2021-06-14 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0003_auto_20210613_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roles',
            name='role_id',
            field=models.CharField(max_length=5, primary_key=True, serialize=False),
        ),
    ]
