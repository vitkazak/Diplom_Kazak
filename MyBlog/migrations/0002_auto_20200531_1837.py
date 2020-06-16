# Generated by Django 3.0.3 on 2020-05-31 15:37

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('MyBlog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='readers',
        ),
        migrations.AddField(
            model_name='article',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='members', to=settings.AUTH_USER_MODEL),
        ),
    ]
