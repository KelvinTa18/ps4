# Generated by Django 5.0.6 on 2024-05-19 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Predict',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': (('predict_one', 'can predict one student'), ('predict_all', 'can predict all student')),
            },
        ),
    ]
