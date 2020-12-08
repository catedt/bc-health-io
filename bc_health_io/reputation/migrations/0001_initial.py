# Generated by Django 2.2.11 on 2020-05-20 02:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Reputation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doctorId', models.CharField(max_length=42)),
                ('email', models.CharField(max_length=255)),
                ('repute', models.IntegerField()),
                ('createDate', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Reputation Created')),
                ('updateDate', models.DateTimeField(default=None, verbose_name='Reputation Updated')),
            ],
            options={
                'ordering': ['updateDate'],
            },
        ),
    ]
