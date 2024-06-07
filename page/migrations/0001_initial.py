# Generated by Django 5.0.6 on 2024-06-07 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccountDB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform', models.CharField(max_length=30)),
                ('token', models.TextField()),
                ('name', models.CharField(max_length=100)),
                ('tag', models.CharField(max_length=30)),
                ('connected', models.BooleanField(default=False)),
                ('icon', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='ContentDB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform', models.CharField(max_length=30)),
                ('userID', models.CharField(default='default_userID', max_length=100)),
                ('text', models.TextField()),
                ('image_url', models.BigIntegerField(default=0)),
                ('userIcon', models.URLField(default='http://default.url/icon.png')),
                ('vote', models.BigIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='FileDB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.IntegerField()),
                ('url', models.URLField(default='http://default.url/icon.png')),
            ],
        ),
    ]
