# Generated by Django 5.1.2 on 2024-10-16 00:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0014_alter_pedido_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='data',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 15, 21, 17, 34, 993150)),
        ),
    ]
