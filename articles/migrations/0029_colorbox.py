# Generated by Django 4.1 on 2022-09-25 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0028_remove_itembox_color_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Colorbox',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('color', models.TextField(default='black')),
            ],
        ),
    ]
