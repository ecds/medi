# Generated by Django 3.1 on 2021-07-19 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='woman',
            name='document_image',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='woman',
            name='date_range',
            field=models.CharField(blank=True, help_text="Enter a period of time, e.g. 'early 14th century'", max_length=255, null=True),
        ),
    ]