# Generated by Django 4.2.7 on 2023-11-22 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('universitas', '0003_remove_detail_cited_id_detail_cited_id_dosen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detail_cited',
            name='id_dosen',
            field=models.CharField(max_length=255, primary_key=True, serialize=False),
        ),
    ]
