# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invitations', '0003_auto_20151126_1523'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='confirmed',
            field=models.BooleanField(default=False, verbose_name='confirmed'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='invitation',
            name='email',
            field=models.EmailField(unique=True, max_length=75, verbose_name='e-mail address'),
            preserve_default=True,
        ),
    ]
