# Generated by Django 4.1 on 2022-09-09 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='article_id',
            field=models.IntegerField(default=0),
        ),
    ]