# Generated by Django 3.2.9 on 2021-12-07 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Article', '0009_collection_article_orderid'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='number',
            field=models.IntegerField(default=0),
        ),
    ]