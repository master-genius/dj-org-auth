# Generated by Django 2.1 on 2018-10-09 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0003_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('blog_title', models.CharField(max_length=200)),
                ('blog_content', models.TextField()),
                ('blog_tags', models.CharField(max_length=100)),
                ('adder_id', models.CharField(db_index=True, max_length=32)),
            ],
        ),
    ]
