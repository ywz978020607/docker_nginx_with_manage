# Generated by Django 2.2.7 on 2021-03-17 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0027_status_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='alertmail',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='status',
            name='period',
            field=models.CharField(default='', max_length=30),
        ),
    ]
