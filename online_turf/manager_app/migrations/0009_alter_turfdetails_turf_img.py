# Generated by Django 4.2.5 on 2023-10-27 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager_app', '0008_alter_turfdetails_turf_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turfdetails',
            name='Turf_img',
            field=models.FileField(blank=True, null=True, upload_to='turf_img'),
        ),
    ]