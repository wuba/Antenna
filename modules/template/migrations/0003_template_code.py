# Generated by Django 3.2.9 on 2022-10-11 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('template', '0002_auto_20220826_1026'),
    ]

    operations = [
        migrations.AddField(
            model_name='template',
            name='code',
            field=models.TextField(default='this is a test code', help_text='文件代码'),
        ),
    ]