# -*- coding: utf-8 -*-
from celery.schedules import crontab
from celery.task import task, periodic_task
from django.db import transaction
from django.utils import timezone
from ..models import Project, Repository, Change, Builder, Build
from .buildbot_json import Buildbot
import json, datetime

@periodic_task(run_every=crontab(minute='3,13,23,33,43,53'))
def query_buildbot():
    for builder in Builder.objects.all():
        build_last_complete = builder.builds.filter(completed=True).order_by('number').last()
        build_first_incomplete = builder.builds.filter(completed=False).order_by('number').first()
        if build_last_complete and build_first_incomplete:
            build_number_start = min(build_last_complete.number, build_first_incomplete.number)
        elif build_last_complete:
            build_number_start = build_last_complete.number
        elif build_first_incomplete:
            build_number_start = build_first_incomplete.number
        else:
            build_number_start = 0
        fetch_builds_from_buildbot.delay(builder.link, builder.name, build_number_start)

@task(ignore_result=True)
def fetch_builds_from_buildbot(link, builder_name, build_number_start):
    buildbot = Buildbot(link)
    buildbot_builder = buildbot.builders[builder_name]
    if buildbot_builder:
        buildbot_builds = buildbot_builder.builds
        buildbot_builds.cache()
        buildbot_latest_build = buildbot_builds[-1]
        for build_number in xrange(build_number_start, buildbot_latest_build.number+1):
            fetch_build_from_buildbot.delay(link, builder_name, build_number)

@task(ignore_result=True)
def fetch_build_from_buildbot(link, builder_name, build_number):
    buildbot = Buildbot(link)
    buildbot_builder = buildbot.builders[builder_name]
    if buildbot_builder:
        buildbot_builds = buildbot_builder.builds
        buildbot_builds.cache()
        buildbot_build = buildbot_builds[build_number]
        parse_build(buildbot_build, builder_name, build_number)

def parse_build(buildbot_build, builder_name, build_number):
    builder, created = Builder.objects.get_or_create(name=builder_name)

    build_data = {
        'completed': buildbot_build.completed,
        'result': buildbot_build.result,
        'simplified_result': buildbot_build.simplified_result,
        'start_time': parse_time(buildbot_build.start_time),
        'end_time': parse_time(buildbot_build.end_time),
        'duration': buildbot_build.duration,
        'properties': json.dumps(buildbot_build.properties),
        'data': json.dumps(buildbot_build.data),
    }

    with transaction.atomic():
        build, created = Build.objects.get_or_create(number=build_number,
                                                     builder=builder,
                                                     defaults=build_data)
        if not created:
            for key, value in build_data.iteritems():
                setattr(build, key, value)
            build.save(update_fields=build_data.keys())

    buildbot_properties = dict((prop[0], prop[1]) for prop in buildbot_build.properties)
    project_name = buildbot_properties.get('project', None) or buildbot_properties.get('branch', None)
    repository_name = buildbot_properties.get('repository', None)

    if project_name:
        project, created = Project.objects.get_or_create(name=project_name)
    else:
        project = None
    if repository_name:
        repository, created = Repository.objects.get_or_create(name=repository_name)
    else:
        repository = None

    buildbot_sourcestamps = buildbot_build.data.get('sourceStamps', [])
    for buildbot_sourcestamp in buildbot_sourcestamps:
        buildbot_changes = buildbot_sourcestamp.get('changes', [])
        for buildbot_change in buildbot_changes:
            parse_change(buildbot_change, project, repository, build)

def parse_change(buildbot_change, project, repository, build):
    project_name = buildbot_change.get('project', None) or buildbot_change.get('branch', None)
    repository_name = buildbot_change.get('repository', None)

    if project_name and project_name != project.name:
        change_project, created = Project.objects.get_or_create(name=project_name)
    else:
        change_project = project
    if repository_name and repository_name != repository.name:
        change_repository, created = Repository.objects.get_or_create(name=repository_name)
    else:
        change_repository = repository

    change_data = {
        'comments': buildbot_change.get('comments'),
        'when': parse_time(buildbot_change.get('when')),
        'who': buildbot_change.get('who'),
    }

    with transaction.atomic():
        change, created = Change.objects.get_or_create(project=change_project,
                                                       repository=change_repository,
                                                       revision=buildbot_change.get('revision'),
                                                       defaults=change_data)
        if not created:
            for key, value in change_data.iteritems():
                setattr(change, key, value)
            change.save(update_fields=change_data.keys())

    build.changes.add(change)

def parse_time(time):
    if time:
        return datetime.datetime.fromtimestamp(time, timezone.utc)
    return None
