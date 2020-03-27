# Generated by Django 3.0.4 on 2020-03-26 20:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('portname', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Containers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial', models.CharField(max_length=32)),
                ('ctype', models.CharField(max_length=32)),
                ('isActive', models.BooleanField(default=True)),
                ('lastUpdate', models.DateField(auto_now_add=True)),
                ('pod', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portname.PortRegistry')),
            ],
        ),
    ]
