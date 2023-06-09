# Generated by Django 4.2 on 2023-05-06 04:19

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_user_facebook_user_github_user_linkedin_user_twitter_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=django_resized.forms.ResizedImageField(crop=None, default='avatar.png', force_format=None, keep_meta=True, quality=-1, scale=None, size=[300, 300], upload_to=''),
        ),
    ]
