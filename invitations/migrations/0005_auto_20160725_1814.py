# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invitations', '0004_auto_20151209_1854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='accepted',
            field=models.BooleanField(default=False, verbose_name='clicked'),
            preserve_default=True,
        ),
    ]
