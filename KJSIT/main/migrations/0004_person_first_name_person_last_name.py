# Generated by Django 5.0.1 on 2024-06-12 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_delete_job'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='first_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='person',
            name='last_name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
