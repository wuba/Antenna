# Generated by Django 3.2.9 on 2022-08-26 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InviteCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(help_text='验证码', max_length=10)),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', null=True)),
            ],
            options={
                'db_table': 'invite_code',
            },
        ),
        migrations.CreateModel(
            name='VerifyCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(help_text='注册用户名', max_length=124)),
                ('verify_code', models.CharField(help_text='验证码', max_length=6)),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', null=True)),
            ],
            options={
                'db_table': 'verify_code',
            },
        ),
    ]
