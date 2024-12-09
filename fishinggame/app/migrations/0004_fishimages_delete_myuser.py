# Generated by Django 5.1.1 on 2024-10-27 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_myuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='FishImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=50)),
                ('images', models.JSONField()),
            ],
        ),
        migrations.DeleteModel(
            name='MyUser',
        ),
    ]