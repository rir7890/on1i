# Generated by Django 5.0.4 on 2024-04-28 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='app_user_mst',
            fields=[
                ('user_name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('f_name', models.CharField(max_length=100)),
                ('l_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('mobile', models.CharField(max_length=20, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('join_date', models.DateField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=False)),
            ],
        ),
    ]
