# Generated by Django 3.1.7 on 2021-06-14 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Semesters',
            fields=[
                ('semester_id', models.AutoField(primary_key=True, serialize=False)),
                ('semester_name', models.CharField(max_length=20, unique=True)),
            ],
            options={
                'verbose_name_plural': 'semesters',
                'db_table': 'semesters',
            },
        ),
    ]
