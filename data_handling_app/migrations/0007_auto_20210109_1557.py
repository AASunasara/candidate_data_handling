# Generated by Django 3.1.5 on 2021-01-09 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_handling_app', '0006_delete_auth_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidates',
            name='contact_no',
            field=models.CharField(max_length=30),
        ),
    ]