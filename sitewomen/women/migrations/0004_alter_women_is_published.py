# Generated by Django 4.2 on 2024-07-16 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('women', '0003_alter_women_content_alter_women_slug_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='women',
            name='is_published',
            field=models.BooleanField(choices=[(0, 'Черновик'), (1, 'Опубликовано')], default=0),
        ),
    ]
