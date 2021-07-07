# Generated by Django 3.1.7 on 2021-07-04 16:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0004_students_cgpa'),
        ('electives', '0005_auto_20210703_0903'),
    ]

    operations = [
        migrations.CreateModel(
            name='ElectiveSelected',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.IntegerField()),
                ('elective_id', models.ForeignKey(db_column='elective_id', on_delete=django.db.models.deletion.CASCADE, to='electives.electives')),
                ('student_id', models.ForeignKey(db_column='student_id', on_delete=django.db.models.deletion.CASCADE, to='students.students')),
            ],
        ),
    ]
