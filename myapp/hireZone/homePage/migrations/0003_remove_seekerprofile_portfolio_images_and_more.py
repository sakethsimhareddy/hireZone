# Generated by Django 4.2.13 on 2024-06-16 11:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homePage', '0002_seekerprofile_portfolio_images_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seekerprofile',
            name='portfolio_images',
        ),
        migrations.RemoveField(
            model_name='seekerprofile',
            name='profile_photo',
        ),
    ]
