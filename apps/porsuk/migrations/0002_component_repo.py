# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('porsuk', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='component',
            name='repo',
            field=models.ForeignKey(default=1, verbose_name='Repository', to='porsuk.Repo'),
            preserve_default=False,
        ),
    ]
