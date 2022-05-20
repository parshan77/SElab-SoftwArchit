# Generated by Django 4.0.4 on 2022-05-25 22:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ride',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bike_id', models.PositiveIntegerField(unique=True)),
                ('biker_username', models.CharField(max_length=128)),
                ('ongoing', models.BooleanField(default=False)),
                ('startX', models.IntegerField(blank=True, null=True)),
                ('startY', models.IntegerField(blank=True, null=True)),
                ('endX', models.IntegerField(blank=True, null=True)),
                ('endY', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=128, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('isAdmin', models.BooleanField(default=False)),
                ('busy', models.BooleanField(default=False)),
                ('token', models.CharField(default='', max_length=256)),
                ('token_exp_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('score', models.IntegerField(default=0)),
                ('locationX', models.IntegerField(blank=True, null=True)),
                ('locationY', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
