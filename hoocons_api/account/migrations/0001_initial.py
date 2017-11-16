# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-16 00:26
from __future__ import unicode_literals

import caching.base
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        ('location', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('user', models.OneToOneField(max_length=30, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('display_name', models.CharField(db_index=True, max_length=50)),
                ('nickname', models.CharField(blank=True, max_length=50, unique=True)),
                ('dob', models.DateField(blank=True, db_index=True, null=True)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], default='Other', max_length=6)),
                ('avatar_url', models.TextField(default='http://res.cloudinary.com/dumfykuvl/image/upload/v1493749974/images_lm0sjf.jpg')),
                ('wallpaper_url', models.TextField(default='http://res.cloudinary.com/dumfykuvl/image/upload/v1493749974/images_lm0sjf.jpg')),
                ('join_date', models.DateField(blank=True, db_index=True, default=django.utils.timezone.now, null=True)),
                ('last_action', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('is_sharing_location', models.BooleanField(default=False)),
                ('level', models.PositiveSmallIntegerField(default=0)),
                ('email', models.EmailField(blank=True, max_length=70, null=True, unique=True)),
                ('followers', models.ManyToManyField(blank=True, related_name='_account_followers_+', to='account.Account')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='location', to='location.Location')),
            ],
            options={
                'verbose_name': 'Account',
                'verbose_name_plural': 'Accounts',
                'db_table': 'account',
            },
            bases=(caching.base.CachingMixin, models.Model),
        ),
        migrations.CreateModel(
            name='FriendshipRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_made_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('message', models.TextField(blank=True, null=True, verbose_name='Message')),
                ('found_user_from', models.CharField(blank=True, default='Search', max_length=50, null=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to='account.Account')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to='account.Account')),
            ],
            options={
                'verbose_name': 'Friendship Request',
                'verbose_name_plural': 'Friendship Requests',
                'db_table': 'friendship_request',
            },
            bases=(caching.base.CachingMixin, models.Model),
        ),
        migrations.CreateModel(
            name='RelationShip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rel_made_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('status', models.CharField(choices=[('Friend', 'FRIEND'), ('Followed', 'FOLLOWED'), ('Friend_Followed', 'FRIEND_FOLLOWED'), ('Friend_Ignored', 'FRIEND_FOLLOWED'), ('Blocked', 'BLOCKED'), ('Ignored', 'IGNORED')], default='Friend', max_length=20)),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_user', to='account.Account')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_user', to='account.Account')),
            ],
            options={
                'verbose_name': 'RelationShip',
                'verbose_name_plural': 'RelationShips',
                'db_table': 'relationship',
            },
            bases=(caching.base.CachingMixin, models.Model),
        ),
        migrations.AlterUniqueTogether(
            name='relationship',
            unique_together=set([('from_user', 'to_user')]),
        ),
        migrations.AlterUniqueTogether(
            name='friendshiprequest',
            unique_together=set([('receiver', 'sender')]),
        ),
    ]