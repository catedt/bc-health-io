# Generated by Django 2.2.11 on 2020-04-11 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HbBlockData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ownerBlockId', models.CharField(max_length=50)),
                ('comments', models.TextField()),
                ('url', models.URLField(max_length=1024)),
                ('publicKey', models.CharField(max_length=256)),
                ('createDate', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]