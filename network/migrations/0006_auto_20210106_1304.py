# Generated by Django 3.1.4 on 2021-01-06 12:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_commentlike_postlike'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentlike',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_likes', to='network.comment'),
        ),
    ]
