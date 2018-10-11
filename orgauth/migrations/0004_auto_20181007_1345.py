# Generated by Django 2.1.2 on 2018-10-07 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orgauth', '0003_orguserauth'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrgRolePerm',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('role_name', models.CharField(db_index=True, max_length=32)),
                ('perm_list', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='orguserauth',
            name='member_id',
            field=models.CharField(db_index=True, max_length=32, unique=True),
        ),
    ]
