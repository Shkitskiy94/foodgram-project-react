# Generated by Django 4.1.6 on 2023-02-27 17:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0004_alter_recipe_cooking_time_alter_tag_colour_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingredientquantity',
            old_name='quantity',
            new_name='amount',
        ),
    ]