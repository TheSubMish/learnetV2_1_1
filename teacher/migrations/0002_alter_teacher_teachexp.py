# Generated by Django 4.2.5 on 2023-09-22 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='teachexp',
            field=models.IntegerField(null=True),
        ),
    ]