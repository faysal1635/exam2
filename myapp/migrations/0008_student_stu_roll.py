# Generated by Django 3.2.2 on 2021-06-09 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_alter_exam_exam_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='stu_roll',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]
