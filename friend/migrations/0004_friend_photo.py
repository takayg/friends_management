# Generated by Django 3.1.7 on 2021-03-13 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('friend', '0003_auto_20210314_0133'),
    ]

    operations = [
        migrations.AddField(
            model_name='friend',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Photo'),
        ),
    ]