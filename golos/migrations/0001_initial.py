# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-11-07 10:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='LikeDislike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote', models.SmallIntegerField(choices=[(-1, 'Не нравится'), (1, 'Нравится')], verbose_name='Голос')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='Nominees',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='имя номинанта')),
                ('image', models.ImageField(upload_to='nominees/photos', verbose_name='изображение')),
            ],
            options={
                'verbose_name': 'Номинант',
                'verbose_name_plural': 'Номинанты',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Show',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='название шоу')),
                ('image', models.ImageField(upload_to='show/photos', verbose_name='изображение')),
            ],
            options={
                'verbose_name': 'Шоу',
                'verbose_name_plural': 'Все Шоу',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='UserGolos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=500, verbose_name='отпечаток пальца')),
            ],
        ),
        migrations.AddField(
            model_name='nominees',
            name='show',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='golos.Show', verbose_name='название шоу'),
        ),
        migrations.AddField(
            model_name='likedislike',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='golos.UserGolos', verbose_name='Пользователь'),
        ),
    ]
