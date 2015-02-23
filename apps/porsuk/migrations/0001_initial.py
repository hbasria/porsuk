# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='A_files',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filename', models.CharField(max_length=80, verbose_name='File Name')),
                ('target', models.CharField(max_length=80, null=True, verbose_name='Target')),
                ('perm', models.IntegerField(null=True, verbose_name='Permisions')),
                ('owner', models.CharField(max_length=55, null=True, verbose_name='Owner')),
                ('group', models.CharField(max_length=55, null=True, verbose_name='Group')),
            ],
            options={
                'verbose_name': 'Additional File',
                'verbose_name_plural': 'Additional Files',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Archive',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uri', models.CharField(max_length=200, verbose_name='Uri')),
                ('type', models.CharField(max_length=35, null=True, verbose_name='Type', blank=True)),
                ('sha1sum', models.CharField(max_length=200, verbose_name='sha1sum')),
                ('target', models.CharField(max_length=200, null=True, verbose_name='Target', blank=True)),
            ],
            options={
                'verbose_name': 'Archive',
                'verbose_name_plural': 'Archives',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('component', models.CharField(max_length=200, verbose_name='Component')),
                ('localname', models.CharField(max_length=200, verbose_name='Local Name')),
                ('summary', models.CharField(max_length=600, null=True, verbose_name='Summary', blank=True)),
                ('description', models.CharField(max_length=1500, null=True, verbose_name='Description', blank=True)),
            ],
            options={
                'verbose_name': 'Component',
                'verbose_name_plural': 'Components',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Dependency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80, verbose_name='Dependency')),
                ('versionFrom', models.CharField(max_length=35, null=True, verbose_name='Version From', blank=True)),
                ('versionTo', models.CharField(max_length=35, null=True, verbose_name='Version To', blank=True)),
                ('version', models.CharField(max_length=35, null=True, verbose_name='Version', blank=True)),
                ('releaseFrom', models.CharField(max_length=35, null=True, verbose_name='Release From', blank=True)),
                ('releaseTo', models.CharField(max_length=35, null=True, verbose_name='Release To', blank=True)),
                ('release', models.CharField(max_length=35, null=True, verbose_name='Release', blank=True)),
            ],
            options={
                'verbose_name': 'Dependency',
                'verbose_name_plural': 'Dependencies',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Files',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('path', models.CharField(max_length=150, verbose_name='Path')),
                ('fileType', models.CharField(max_length=50, verbose_name='fileType')),
            ],
            options={
                'verbose_name': 'Dosya',
                'verbose_name_plural': 'Files',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IntraFiles',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filename', models.CharField(max_length=150, verbose_name='File Name')),
                ('path', models.CharField(max_length=300, verbose_name='Path')),
                ('type', models.CharField(max_length=80, verbose_name='Type')),
                ('size', models.IntegerField(verbose_name='Size')),
                ('mode', models.IntegerField(verbose_name='Mode')),
                ('hash', models.CharField(max_length=80, verbose_name='Hash')),
            ],
            options={
                'verbose_name': 'IntraFile',
                'verbose_name_plural': 'IntraFiles',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IsA',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='IsA')),
            ],
            options={
                'verbose_name': 'Is A',
                'verbose_name_plural': "Is A's",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('license', models.CharField(unique=True, max_length=50, verbose_name='License')),
                ('url', models.URLField(null=True, verbose_name='URL', blank=True)),
            ],
            options={
                'verbose_name': 'License',
                'verbose_name_plural': 'Licenses',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80, verbose_name='Name')),
                ('slug', models.SlugField(unique=True, max_length=200, verbose_name='Package Slug')),
                ('installedSize', models.IntegerField(null=True, verbose_name='Installed Size', blank=True)),
                ('packageSize', models.IntegerField(null=True, verbose_name='Package Size', blank=True)),
                ('packageHash', models.CharField(max_length=100, null=True, verbose_name='Hash', blank=True)),
                ('packageURI', models.CharField(max_length=250, null=True, verbose_name='URI', blank=True)),
                ('replaces', models.CharField(max_length=100, null=True, verbose_name='Replaces', blank=True)),
                ('a_files', models.ManyToManyField(to='porsuk.A_files', null=True, verbose_name='Additional Files')),
                ('files', models.ManyToManyField(to='porsuk.Files', verbose_name='Files')),
                ('intrafiles', models.ManyToManyField(to='porsuk.IntraFiles', null=True, verbose_name='IntraFiles')),
                ('runtime_dep', models.ManyToManyField(related_name='runtime_dep', null=True, verbose_name='Runtime Dependencies', to='porsuk.Dependency')),
            ],
            options={
                'verbose_name': 'Package',
                'verbose_name_plural': 'Packages',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Packager',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80, verbose_name='Name')),
                ('email', models.EmailField(max_length=75, verbose_name='E-posta')),
            ],
            options={
                'verbose_name': 'Packager',
                'verbose_name_plural': 'Packagers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Patch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='Patch')),
                ('level', models.IntegerField(null=True, verbose_name='Level')),
            ],
            options={
                'verbose_name': 'Patch',
                'verbose_name_plural': 'Patches',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Repo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=30, verbose_name='Name')),
                ('url', models.URLField(verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Repository',
                'verbose_name_plural': 'Repositories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=150, verbose_name='Source Slug')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('homepage', models.URLField(null=True, verbose_name='Homepage', blank=True)),
                ('part_of', models.CharField(max_length=100, null=True, verbose_name='Partof', blank=True)),
                ('summary', models.CharField(max_length=600, null=True, verbose_name='Summary', blank=True)),
                ('description', models.CharField(max_length=1500, null=True, verbose_name='Description', blank=True)),
                ('icon', models.CharField(max_length=100, null=True, verbose_name='Icon', blank=True)),
                ('version', models.CharField(max_length=40, null=True, verbose_name='Version', blank=True)),
                ('release', models.CharField(max_length=40, null=True, verbose_name='Release', blank=True)),
                ('created_at', models.DateTimeField(null=True, verbose_name='First Release Date', blank=True)),
                ('updated_at', models.DateTimeField(null=True, verbose_name='Last Update', blank=True)),
                ('build_script_size', models.IntegerField(null=True, verbose_name='Build Script Size', blank=True)),
                ('spec_script_size', models.IntegerField(null=True, verbose_name='Spec Script Size', blank=True)),
                ('update_count', models.IntegerField(null=True, verbose_name='Update Count', blank=True)),
                ('patch_count', models.IntegerField(null=True, verbose_name='Patch Count', blank=True)),
                ('archives', models.ManyToManyField(to='porsuk.Archive', verbose_name='Archives')),
                ('build_dep', models.ManyToManyField(related_name='build_dep', null=True, verbose_name='build dependencies', to='porsuk.Dependency', blank=True)),
                ('component', models.ForeignKey(verbose_name='Component', to='porsuk.Component')),
                ('isa', models.ManyToManyField(to='porsuk.IsA', null=True, verbose_name='Is A', blank=True)),
                ('license', models.ManyToManyField(to='porsuk.License', verbose_name='License')),
                ('packager', models.ForeignKey(verbose_name='Packager', to='porsuk.Packager')),
                ('packages', models.ManyToManyField(related_name='packages', null=True, verbose_name='Packages', to='porsuk.Package', blank=True)),
                ('repo', models.ForeignKey(verbose_name='Repository', to='porsuk.Repo')),
            ],
            options={
                'verbose_name': 'Source',
                'verbose_name_plural': 'Sources',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Update',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('release', models.IntegerField(verbose_name='Release')),
                ('type', models.CharField(max_length=50, null=True, verbose_name='Type')),
                ('date', models.DateField(verbose_name='Date')),
                ('version', models.CharField(max_length=50, verbose_name='Version')),
                ('comment', models.CharField(max_length=3000, verbose_name='Comment')),
                ('packager', models.ForeignKey(verbose_name='Packager', to='porsuk.Packager')),
            ],
            options={
                'get_latest_by': 'date',
                'verbose_name': 'Update',
                'verbose_name_plural': 'Updates',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='source',
            name='updates',
            field=models.ManyToManyField(to='porsuk.Update', null=True, verbose_name='Update', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='patch',
            name='source',
            field=models.ForeignKey(related_name='patches', to='porsuk.Source'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='package',
            name='source',
            field=models.ForeignKey(verbose_name=b'Source', to='porsuk.Source'),
            preserve_default=True,
        ),
    ]
