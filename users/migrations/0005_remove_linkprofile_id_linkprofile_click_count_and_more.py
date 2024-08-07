# Generated by Django 5.0.4 on 2024-07-14 18:34

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_linkprofile_personal_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='linkprofile',
            name='id',
        ),
        migrations.AddField(
            model_name='linkprofile',
            name='click_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='linkprofile',
            name='profile_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='linkprofile',
            name='channel_url',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(default='images/default_image.png', upload_to='images/'),
        ),
    ]
