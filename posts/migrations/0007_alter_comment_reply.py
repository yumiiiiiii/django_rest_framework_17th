# Generated by Django 4.1.7 on 2023-04-07 08:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_rename_re_comment_comment_reply'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='reply',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment_reply', to='posts.comment'),
        ),
    ]
