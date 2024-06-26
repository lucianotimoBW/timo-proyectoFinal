# Generated by Django 5.0.6 on 2024-06-20 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0003_message_page'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blog',
            old_name='body',
            new_name='content',
        ),
        migrations.AddField(
            model_name='blog',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='blog',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='blog_images/'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='subtitle',
            field=models.CharField(max_length=255),
        ),
    ]