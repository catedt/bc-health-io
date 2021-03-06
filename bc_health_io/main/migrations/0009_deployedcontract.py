# Generated by Django 2.2.11 on 2020-05-22 16:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20200520_0241'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeployedContract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contractAddress', models.CharField(max_length=42)),
                ('contractName', models.CharField(max_length=1024)),
                ('abi', models.TextField()),
                ('deployDate', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date deployed')),
            ],
        ),
    ]
