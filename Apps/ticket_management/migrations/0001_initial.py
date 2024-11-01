# Generated by Django 5.1.2 on 2024-10-29 19:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('org_management', '0002_organization_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketColumn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('position', models.PositiveIntegerField(help_text='Defines the order of columns')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ticket_columns', to='org_management.organization')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('column', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='ticket_management.ticketcolumn')),
            ],
        ),
    ]
