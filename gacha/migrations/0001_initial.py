# Generated by Django 3.2 on 2022-09-06 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='название')),
                ('rarity', models.IntegerField(default=0, verbose_name='редкость')),
            ],
            options={
                'verbose_name': 'Карточка',
                'verbose_name_plural': 'Карточки',
            },
        ),
    ]
