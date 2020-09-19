# Generated by Django 3.1 on 2020-09-19 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0002_auto_20200919_1442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userattendance',
            name='attendance',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='userattendance',
            name='condition',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='userattendance',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='userattendance',
            name='otherNotPresent',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='userattendance',
            name='otherSicks',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='userattendance',
            name='reasonNotPresent',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='userattendance',
            name='selfassstatus',
            field=models.CharField(max_length=251, null=True),
        ),
        migrations.AlterField(
            model_name='userattendance',
            name='sickChoices',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='userattendance',
            name='wfo_description',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='userattendance',
            name='work_status',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
