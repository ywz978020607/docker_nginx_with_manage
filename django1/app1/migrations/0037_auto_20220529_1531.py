# Generated by Django 2.2 on 2022-05-29 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0036_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Options',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=30)),
                ('enable_sign_up', models.BooleanField(default=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Status',
        ),
    ]
