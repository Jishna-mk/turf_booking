# Generated by Django 4.2.5 on 2023-10-27 08:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager_app', '0009_alter_turfdetails_turf_img'),
    ]

    operations = [
        migrations.RenameField(
            model_name='turfdetails',
            old_name='Turf_img',
            new_name='Turf_image',
        ),
    ]
