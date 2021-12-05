# Generated by Django 3.2.9 on 2021-12-05 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Article', '0007_article_source'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('CID', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Collection_Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CID', models.IntegerField()),
                ('AID', models.IntegerField()),
            ],
        ),
    ]