# Generated by Django 3.1.6 on 2021-03-02 19:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lastName', models.CharField(max_length=30)),
                ('firstName', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=100)),
                ('password', models.CharField(max_length=1024)),
                ('secureToken', models.CharField(max_length=1024, null=True)),
                ('OHIP', models.CharField(max_length=12)),
                ('vaccineStatus', models.BooleanField(default=False)),
                ('exposure', models.BooleanField(default=False)),
                ('phoneNumber', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Vaccinated',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vaccinationDate', models.DateField()),
                ('vaccinationType', models.CharField(max_length=30)),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.user')),
            ],
        ),
        migrations.CreateModel(
            name='OneTimeText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oneTimeValue', models.CharField(max_length=7)),
                ('stillValid', models.BooleanField()),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.user')),
            ],
        ),
        migrations.CreateModel(
            name='CovidTest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateTaken', models.DateField()),
                ('testResults', models.BooleanField()),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.user')),
            ],
        ),
    ]
