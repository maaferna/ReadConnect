# Generated by Django 4.2.6 on 2023-10-27 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books_store', '0007_userprofile_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='full_name',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
