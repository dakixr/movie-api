# Generated by Django 5.0.6 on 2024-06-06 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_api', '0002_alter_director_birthyear_alter_director_nationality'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actor',
            name='BirthYear',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='actor',
            name='Nationality',
            field=models.CharField(max_length=100, null=True),
        ),
    ]