# Generated by Django 5.0 on 2024-01-04 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hostel', '0002_level_customuser_phone_number_customuser_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='exeat',
            name='department',
            field=models.CharField(default='hello', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='exeat',
            name='faculty',
            field=models.CharField(default='hi', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='exeat',
            name='level',
            field=models.CharField(default='hey', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='exeat',
            name='student_number',
            field=models.CharField(default='hee', max_length=20),
            preserve_default=False,
        ),
    ]
