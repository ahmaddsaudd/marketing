# Generated by Django 3.2.12 on 2024-03-16 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketing', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='response',
            name='background_task',
        ),
        migrations.AddField(
            model_name='response',
            name='background_task_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='response',
            name='designation',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='response',
            name='domain_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='response',
            name='email',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='response',
            name='industry',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='response',
            name='keyword',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='response',
            name='name',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='response',
            name='response_object',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='results',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='results',
            name='keyword',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='results',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='tags',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='tags',
            name='name',
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='tags',
            name='status',
            field=models.CharField(max_length=50, null=True),
        ),
    ]