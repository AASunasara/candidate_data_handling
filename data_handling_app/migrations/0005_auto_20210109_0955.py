# Generated by Django 3.1.5 on 2021-01-09 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_handling_app', '0004_auto_20210109_0954'),
    ]

    operations = [
        migrations.CreateModel(
            name='auth_user',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('excel_file_url', models.URLField(max_length=300)),
            ],
        ),
        migrations.DeleteModel(
            name='Users',
        ),
    ]