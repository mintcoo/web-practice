# Generated by Django 4.1 on 2022-09-18 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0024_profile_icon_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=30),
        ),
    ]