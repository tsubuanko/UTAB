# Generated by Django 2.1.15 on 2020-05-18 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0009_thread_faculty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thread',
            name='faculty',
            field=models.CharField(choices=[('前期教養学部', '前期教養学部'), ('後期教養学部', '後期教養学部'), ('法学部', '法学部'), ('経済学部', '経済学部'), ('文学部', '文学部'), ('教育学部', '教育学部'), ('理学部', '理学部'), ('工学部', '工学部'), ('農学部', '農学部'), ('薬学部', '薬学部'), ('医学部', '医学部')], max_length=20, null=True),
        ),
    ]
