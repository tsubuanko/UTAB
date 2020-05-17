from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0002_user_twitter'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('memo', models.TextField()),
            ],
        ),
    ]