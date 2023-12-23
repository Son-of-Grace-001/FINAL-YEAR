# Generated by Django 5.0 on 2023-12-23 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hostel', '0005_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exeat',
            name='is_approved',
        ),
        migrations.AddField(
            model_name='exeat',
            name='status',
            field=models.CharField(choices=[('PENDING', 'Exect request is pending'), ('APPROVED', 'Approved by admin'), ('REJECTED', 'Rejected by Admin')], default='PENDING', max_length=10),
        ),
    ]
