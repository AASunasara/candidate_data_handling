# Generated by Django 3.1.5 on 2021-01-09 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_handling_app', '0002_auto_20210109_0839'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('excel_file_url', models.URLField(max_length=300)),
            ],
        ),
    ]