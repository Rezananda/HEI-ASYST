# Generated by Django 3.1 on 2020-08-21 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='initial',
            field=models.CharField(max_length=3),
        ),
    ]
