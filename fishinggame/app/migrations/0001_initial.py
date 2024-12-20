# Generated by Django 5.1.1 on 2024-09-07 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=255, unique=True)),
                ('user_name', models.CharField(max_length=255)),
                ('coins', models.IntegerField(default=0)),
                ('diamonds', models.IntegerField(default=0)),
                ('level', models.IntegerField(default=1)),
                ('current_experience', models.IntegerField(default=0)),
                ('experience_for_next_level', models.IntegerField(default=100)),
                ('rod_type', models.CharField(default='basic', max_length=255)),
                ('fish_inventory', models.JSONField(default=list)),
            ],
        ),
    ]
