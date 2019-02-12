#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import requests
from peewee import *
import json

db = SqliteDatabase('issues.db')
APP_DIR = os.path.abspath(os.path.dirname(__file__))

USERNAME = '-------'
PASSWORD = '--------'

REPO_OWNER = '---------'
REPO_NAME = '----------'


class Problem(Model):
    repo = CharField()
    sub_repo = CharField()
    name = CharField()
    version = CharField()
    maintainers = CharField()
    comment = CharField()
    problem = CharField()
    remote_id = IntegerField(null=True)
    status = CharField(default='new')

    class Meta:
        database = db


def get_or_create(model, defaults=None, **kwargs):
    defaults = defaults or {}
    query = model.select()

    for field, value in kwargs.items():
        if '__' in field:
            query = query.filter(**{field: value})
        else:
            query = query.where(getattr(model, field) == value)

    try:
        if kwargs:
            return query.get(), False

    except model.DoesNotExist:
        pass

    try:
        params = dict((k, v) for k, v in kwargs.items()
                      if '__' not in k)
        params.update(defaults)

        with model._meta.database.atomic():
            return model.create(**params), True

    except IntegrityError as exc:
        try:
            return query.get(), False
        except model.DoesNotExist:
            raise exc


def sync_issues():
    '''
    {u'comment': u'Change the dynamic library load path (rpath) of binaries',
        u'rawversion': u'0.16',
        u'family': u'pisi',
        u'basename': None,
        u'licenses': [u'GPLv2'],
        u'maintainer': u'admins@pisilinux.org',
        u'id': 2089187564,
        u'category':u'app:console',
        u'versionclass': 1,
        u'version': u'0.16',
        u'homepage': u'http://freshmeat.net/projects/chrpath/',
        u'extrafields': {u'pspecdir': u'system/devel/chrpath'},
        u'flavors': [],
        u'origversion': u'0.16',
        u'downloads': [u'http://source.pisilinux.org/1.0/chrpath-0.16.tar.gz'],
        u'repo': u'pisi_main',
        u'maintainers': [u'admins@pisilinux.org'],
        u'shadow': False,
        u'effname': u'chrpath',
        u'name': u'chrpath',
        u'flags': 0,
        u'subrepo': u'core',
        u'problem': u'Homepage link "http://freshmeat.net/projects/chrpath/" is dead (HTTP error 404) for more than a month.'}
    :return:
    '''
    problems = requests.get('https://repology.org/api/v1/repository/pisi_main/problems')

    if problems.status_code == 200:
        problems = problems.json()

        for problem in problems:
            obj, created = get_or_create(Problem, remote_id=problem.get('id'), defaults={
                'repo': problem.get('repo'),
                'sub_repo': problem.get('subrepo'),
                'name': problem.get('name'),
                'version': problem.get('version'),
                'maintainers': ','.join(problem.get('maintainers')),
                'problem': problem.get('problem'),
                'comment': problem.get('comment'),
            })

            if created:
                make_github_issue(obj.comment, obj.problem, ['repology'])

            print(created, obj.comment)


def make_github_issue(title, body=None, labels=None):
    '''Create an issue on github.com using the given parameters.'''
    # Our url to create issues via POST
    url = 'https://api.github.com/repos/%s/%s/issues' % (REPO_OWNER, REPO_NAME)
    # Create an authenticated session to create the issue
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)
    # Create our issue
    issue = {'title': title,
             'body': body,
             'labels': labels}
    # Add the issue to our repository
    r = session.post(url, json.dumps(issue))
    if r.status_code == 201:
        print ('Successfully created Issue ')
    else:
        print ('Could not create Issue {0:s}'.format(title))
        print ('Response:', r.content)


if __name__ == '__main__':
    db_path = os.path.join(APP_DIR, 'issues.db')

    if not os.path.exists(db_path):
        db.create_tables([Problem, ])

    sync_issues()
