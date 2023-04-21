# Generated by Django 4.2 on 2023-04-20 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=16, unique=True)),
                ('register_date', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'app user',
                'verbose_name_plural': 'app users',
                'db_table': 'app_user',
            },
        ),
        migrations.CreateModel(
            name='LoginRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(db_index=True, max_length=16)),
                ('expire_time', models.DateTimeField()),
                ('verification_code', models.CharField(max_length=8)),
                ('request_date', models.DateField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'login request',
                'verbose_name_plural': 'login requests',
                'db_table': 'login_request',
            },
        ),
    ]