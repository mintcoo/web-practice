# Generated by Django 4.1 on 2022-09-13 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_point'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='point',
            field=models.IntegerField(default=500),
        ),
    ]
