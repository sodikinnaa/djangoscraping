# Generated by Django 4.2.7 on 2023-11-16 12:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Univerisitas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_univ', models.CharField(max_length=255)),
                ('url_univ', models.CharField(max_length=255)),
                ('total_sitasi', models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Detail_cited',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('afiiliation', models.CharField(max_length=255)),
                ('nama_dosen', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('cited_by', models.IntegerField(null=True)),
                ('urldosen', models.URLField(null=True)),
                ('fk_url_univ', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='universitas.univerisitas')),
            ],
        ),
    ]
