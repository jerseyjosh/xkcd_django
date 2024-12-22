# Generated by Django 5.1.4 on 2024-12-19 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comic',
            old_name='alt',
            new_name='alt_text',
        ),
        migrations.RenameField(
            model_name='comic',
            old_name='img',
            new_name='image_url',
        ),
        migrations.AddField(
            model_name='comic',
            name='embedding_model',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
