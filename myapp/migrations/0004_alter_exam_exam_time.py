# Generated by Django 3.2.2 on 2021-06-07 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_alter_exam_exam_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='exam_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
