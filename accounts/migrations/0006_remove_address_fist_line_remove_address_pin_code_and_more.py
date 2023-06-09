# Generated by Django 4.0.1 on 2022-06-25 18:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_cartitems_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='fist_line',
        ),
        migrations.RemoveField(
            model_name='address',
            name='pin_code',
        ),
        migrations.AddField(
            model_name='address',
            name='first_line',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='pin',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='second_line',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='state',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.profile'),
        ),
        migrations.AlterField(
            model_name='cartitems',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
