# Generated by Django 3.2.6 on 2021-09-24 13:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_message_thread'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='timeofmessage',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]