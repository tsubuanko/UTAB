# Generated by Django 2.1.15 on 2020-05-17 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0007_user_favorite_thread'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='favorite_thread',
            field=models.ManyToManyField(blank=True, to='cms.Thread'),
        ),
    ]