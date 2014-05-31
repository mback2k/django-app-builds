# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
import json

class Project(models.Model):
    name = models.CharField(_('Name'), max_length=50, unique=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name

class Repository(models.Model):
    name = models.CharField(_('Name'), max_length=250, unique=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name

class Change(models.Model):
    project = models.ForeignKey(Project, related_name='changes')
    repository = models.ForeignKey(Repository, related_name='changes', blank=True, null=True)
    revision = models.CharField(_('Revision'), max_length=40)
    comments = models.TextField(_('Comments'))
    when = models.DateTimeField(_('When'))
    who = models.CharField(_('Who'), max_length=100)

    class Meta:
        ordering = ('-when',)
        unique_together = ('project', 'repository', 'revision')

    def __unicode__(self):
        return self.revision

class Builder(models.Model):
    name = models.CharField(_('Name'), max_length=50, unique=True)
    link = models.URLField(_('Link'), help_text=_('JSON API'))

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name

class Build(models.Model):
    SUCCESS, WARNINGS, FAILURE, SKIPPED, EXCEPTION, RETRY = range(6)
    RESULTS = (
        (SUCCESS,   _('Success')),
        (WARNINGS,  _('Warnings')),
        (FAILURE,   _('Failure')),
        (SKIPPED,   _('Skipped')),
        (EXCEPTION, _('Exception')),
        (RETRY,     _('Retry')),
    )

    builder = models.ForeignKey(Builder, related_name='builds')
    number = models.IntegerField(_('Number'))
    changes = models.ManyToManyField(Change, related_name='builds')
    completed = models.BooleanField(_('Completed'), default=False)
    result = models.SmallIntegerField(_('Result'), choices=RESULTS, blank=True, null=True)
    simplified_result = models.NullBooleanField(_('Simplified result'), blank=True, null=True)
    start_time = models.DateTimeField(_('Start time'), blank=True, null=True)
    end_time = models.DateTimeField(_('End time'), blank=True, null=True)
    duration = models.IntegerField(_('Duration'), blank=True, null=True)
    properties = models.TextField(_('Properties'))
    data = models.TextField(_('Data'))

    class Meta:
        ordering = ('-start_time',)
        unique_together = ('builder', 'number')

    def __unicode__(self):
        return u'%s:%d' % (self.builder, self.number)

    def get_property(self, name, default=None):
        if not self._properties:
            self._properties = json.loads(self.properties)
        for key, value, source in self._properties:
            if key == name:
                return value
        return default
