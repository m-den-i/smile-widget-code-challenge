# Generated by Django 2.0.7 on 2018-09-24 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_start', models.DateField()),
                ('date_end', models.DateField(blank=True, null=True)),
                ('name', models.CharField(blank=True, help_text='Name of price offer', max_length=256)),
                ('cost', models.PositiveIntegerField(help_text='Price for the specified period')),
                ('priority', models.PositiveIntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
