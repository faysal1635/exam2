# Generated by Django 3.2.2 on 2021-06-07 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='exam_time',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]