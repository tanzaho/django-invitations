# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import invitations.models


class Migration(migrations.Migration):

    dependencies = [
        ('invitations', '0006_auto_20161014_1153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='unsubscribe_slug',
            field=models.SlugField(default=invitations.models._create_unsubscribe_slug, max_length=32),
            preserve_default=True,
        ),
    ]
