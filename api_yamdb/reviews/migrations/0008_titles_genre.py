# Generated by Django 3.2 on 2023-11-15 21:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0007_remove_titles_genre'),
    ]

    operations = [
        migrations.AddField(
            model_name='titles',
            name='genre',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='genre', to='reviews.genres'),
            preserve_default=False,
        ),
    ]
