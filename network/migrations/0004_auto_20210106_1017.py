# Generated by Django 3.1.4 on 2021-01-06 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_auto_20210106_1013'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='comments',
        ),
        migrations.AddField(
            model_name='post',
            name='comments_count',
            field=models.IntegerField(default=0),
        ),
    ]
