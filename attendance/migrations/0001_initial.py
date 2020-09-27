# Generated by Django 3.1 on 2020-09-26 16:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAttendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendance_status', models.CharField(max_length=255)),
                ('selfassstatus', models.CharField(max_length=251)),
                ('working_location', models.CharField(max_length=255)),
                ('wfo_time', models.CharField(max_length=255)),
                ('condition', models.CharField(max_length=255)),
                ('sick_reason', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('authors', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
