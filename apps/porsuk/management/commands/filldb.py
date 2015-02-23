# -*- coding: utf-8 -*-
import os
from time import time
import datetime
from django.core.exceptions import ValidationError

from django.core.management.base import BaseCommand
from django.template.defaultfilters import slugify
from apps.porsuk.models import Repo, Component, Packager, Source, Package, Dependency, Patch, Files, A_files
from pisi.specfile import SpecFile
from pisi.component import Component as PisiComponent


__author__ = 'hba'

def validate_date(date_text, repo_os):
    try:
        if repo_os == 'pisilinux':
            return datetime.datetime.strptime(date_text, '%Y-%m-%d')
        else:
            return datetime.datetime.strptime(date_text, '%d-%m-%Y')
    except ValueError:
        return None

class Command(BaseCommand):
    def handle(self, *args, **options):

        repositories = (
            ('pisilinux', '1.0', 'http://packages.pisilinux.org/repositories/1.0/stable/x86_64/pisi-index.xml.xz'),
            ('evolveos', '1.0', 'https://github.com/evolve-os/repository/raw/master/eopkg-index.xml.xz'),
        )

        home = os.environ.get('HOME')
        gitdir = 'workspaces/pisi'
        package_blacklist = []

        startTime=time()
        package_counter = 1

        for repo_os, repo_name, repo_url in repositories:
            repo_path = os.path.join(home, gitdir, repo_os, repo_name)
            repo, created = Repo.objects.get_or_create(name='-'.join([repo_os, repo_name]), url=repo_url)

            for root, dirs, files in os.walk(repo_path):
                for file in files:
                    if file == 'pspec.xml':
                        print "spec file: %s" % os.path.join(root, file)
                        spec = SpecFile(os.path.join(root, file))

                        if spec.source.name in package_blacklist:
                           print "%s BlackList'te. Atlanıyor..." % spec.source.name
                           package_counter += 1
                           continue



                        packStartTime = time()


                        component, created = (None, None)

                        ### Component ###
                        try:
                            comp_file = PisiComponent(os.path.join(root, '../component.xml'))
                            component, created = Component.objects.get_or_create(component=comp_file.name, repo=repo)
                        except:
                            print "Could not find component.xml, trying to retrieve component from directories"
                            dir_comp = root[:root.rfind('/')].replace(os.path.join(home, gitdir, repo_name) + '/','').replace("/",".")
                            component, created = Component.objects.get_or_create(component=dir_comp, repo=repo)

                        packager, created = Packager.objects.get_or_create(name=spec.source.packager.name, email=spec.source.packager.email)

                        print "\033[01;33m%s\033[0m - %s - %s - (Paket \033[01;33m%d\033[0m)" % (spec.source.name, component.component, repo_name, package_counter)

                        ######### Source #########

                        source_slug = '%s-%s' % (slugify(spec.source.name), repo_os)
                        source, created = Source.objects.get_or_create(name=spec.source.name, slug=source_slug, repo=repo,
                                                                    defaults={
                                                                        'component':component,
                                                                        'packager':packager
                                                                    })
                        #try:
                        source.summary = spec.source.summary
                        source.description = spec.source.description


                        source.homepage = spec.source.homepage
                        source.version = spec.getSourceVersion()
                        source.archive_name = spec.source.archive[0].name
                        source.archive_sha1sum = spec.source.archive[0].sha1sum
                        source.archive_type = spec.source.archive[0].type
                        source.archive_url = spec.source.archive[0].uri

                        ### İstatistikler ###
                        source.created_at = validate_date(spec.history[-1].date, repo_os)
                        source.updated_at = validate_date(spec.history[0].date, repo_os)
                        source.build_script_size = getFileSize(os.path.join(root, 'actions.py'))
                        source.spec_script_size = getFileSize(os.path.join(root, file))
                        source.update_count = spec.history.__len__()
                        source.patch_count = spec.source.patches.__len__()
                        source.save()

                        ### Build Dependencies ###
                        for bu in spec.source.buildDependencies:
                            bd, bd_created = Dependency.objects.get_or_create(name=bu.package,
                                                                              versionFrom=bu.versionFrom,
                                                                              versionTo=bu.versionTo,
                                                                              version=bu.version,
                                                                              releaseFrom=bu.releaseFrom,
                                                                              releaseTo=bu.releaseTo,
                                                                              release=bu.release)
                            source.build_dep.add(bd)

                        ### Patches ###
                        for pec in spec.source.patches:
                            patch, created = Patch.objects.get_or_create(source=source, name=pec.filename, level=pec.level)

                        ######### Package #########
                        for package in spec.packages:
                            package_slug = '%s-%s' % (slugify(package.name), repo_os)
                            p, p_created = Package.objects.get_or_create(slug=package_slug,
                                                                         defaults={
                                                                             'name': package.name,
                                                                             'source': source,
                                                                         })
                            source.packages.add(p)

                            ### RuntimeDeps ##
                            for run_dep in package.packageDependencies:
                                runtime_dep, rundep_created = Dependency.objects.get_or_create(name=run_dep.package,
                                                                                               versionFrom=run_dep.versionFrom,
                                                                                               versionTo=run_dep.versionTo,
                                                                                               version=run_dep.version,
                                                                                               releaseFrom=run_dep.releaseFrom,
                                                                                               releaseTo=run_dep.releaseTo,
                                                                                               release=run_dep.release,)

                                p.runtime_dep.add(runtime_dep)


                            ### Files ###
                            for package_file in package.files:
                                file, created = Files.objects.get_or_create(path=package_file.path, fileType=package_file.fileType)
                                p.files.add(file)

                        ### Additional Files ###
                        for additional_file in package.additionalFiles:
                            a_file, created = A_files.objects.get_or_create(filename=additional_file.filename,
                                         target=additional_file.target,
                                         perm=additional_file.permission,
                                         owner=additional_file.owner,
                                         group=additional_file.group)

                            p.a_files.add(a_file)






                        ### Source kaydet ###
                        source.save()

                        print "\033[01;33m%.3f s\033[0m" %(time() - packStartTime),
                        print "- %d s" % (time() - startTime)
                        package_counter += 1




def getFileSize(src):
    """Verilen dosyanın satır sayısını döndürür"""
    src_file = open(src)
    len = src_file.readlines().__len__()
    src_file.close()
    return len