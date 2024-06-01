# Generated by Django 5.0.4 on 2024-05-31 10:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('connect', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=20)),
                ('platform', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('tag', models.CharField(default='none', max_length=20)),
                ('color', models.CharField(default='none', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('platform', models.CharField(max_length=20)),
                ('text', models.TextField()),
                ('icon', models.ImageField(default='none', upload_to='images/')),
                ('image', models.ImageField(default='none', upload_to='images/')),
                ('tag', models.CharField(default='none', max_length=20)),
                ('Account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='page.account')),
            ],
        ),
    ]