# Generated by Django 4.1.6 on 2023-02-28 07:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_is_active_user_is_admin_user_is_staff'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_admin',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_staff',
        ),
    ]
