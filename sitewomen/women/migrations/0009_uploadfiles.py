# Generated by Django 5.0.7 on 2024-10-07 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('women', '0008_alter_category_options_alter_women_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadFiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='uploads')),
            ],
        ),
    ]
