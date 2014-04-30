# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Project'
        db.create_table(u'builds_project', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
        ))
        db.send_create_signal(u'builds', ['Project'])

        # Adding model 'Repository'
        db.create_table(u'builds_repository', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=250)),
        ))
        db.send_create_signal(u'builds', ['Repository'])

        # Adding model 'Change'
        db.create_table(u'builds_change', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='changes', to=orm['builds.Project'])),
            ('repository', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='changes', null=True, to=orm['builds.Repository'])),
            ('revision', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('comments', self.gf('django.db.models.fields.TextField')()),
            ('when', self.gf('django.db.models.fields.DateTimeField')()),
            ('who', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'builds', ['Change'])

        # Adding unique constraint on 'Change', fields ['project', 'repository', 'revision']
        db.create_unique(u'builds_change', ['project_id', 'repository_id', 'revision'])

        # Adding model 'Builder'
        db.create_table(u'builds_builder', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal(u'builds', ['Builder'])

        # Adding model 'Build'
        db.create_table(u'builds_build', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('builder', self.gf('django.db.models.fields.related.ForeignKey')(related_name='builds', to=orm['builds.Builder'])),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('completed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('result', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True)),
            ('simplified_result', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('duration', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('properties', self.gf('django.db.models.fields.TextField')()),
            ('data', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'builds', ['Build'])

        # Adding unique constraint on 'Build', fields ['builder', 'number']
        db.create_unique(u'builds_build', ['builder_id', 'number'])

        # Adding M2M table for field changes on 'Build'
        m2m_table_name = db.shorten_name(u'builds_build_changes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('build', models.ForeignKey(orm[u'builds.build'], null=False)),
            ('change', models.ForeignKey(orm[u'builds.change'], null=False))
        ))
        db.create_unique(m2m_table_name, ['build_id', 'change_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Build', fields ['builder', 'number']
        db.delete_unique(u'builds_build', ['builder_id', 'number'])

        # Removing unique constraint on 'Change', fields ['project', 'repository', 'revision']
        db.delete_unique(u'builds_change', ['project_id', 'repository_id', 'revision'])

        # Deleting model 'Project'
        db.delete_table(u'builds_project')

        # Deleting model 'Repository'
        db.delete_table(u'builds_repository')

        # Deleting model 'Change'
        db.delete_table(u'builds_change')

        # Deleting model 'Builder'
        db.delete_table(u'builds_builder')

        # Deleting model 'Build'
        db.delete_table(u'builds_build')

        # Removing M2M table for field changes on 'Build'
        db.delete_table(db.shorten_name(u'builds_build_changes'))


    models = {
        u'builds.build': {
            'Meta': {'ordering': "('-start_time',)", 'unique_together': "(('builder', 'number'),)", 'object_name': 'Build'},
            'builder': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'builds'", 'to': u"orm['builds.Builder']"}),
            'changes': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'builds'", 'symmetrical': 'False', 'to': u"orm['builds.Change']"}),
            'completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'data': ('django.db.models.fields.TextField', [], {}),
            'duration': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'properties': ('django.db.models.fields.TextField', [], {}),
            'result': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'simplified_result': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'builds.builder': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Builder'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'builds.change': {
            'Meta': {'ordering': "('-when',)", 'unique_together': "(('project', 'repository', 'revision'),)", 'object_name': 'Change'},
            'comments': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'changes'", 'to': u"orm['builds.Project']"}),
            'repository': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'changes'", 'null': 'True', 'to': u"orm['builds.Repository']"}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'when': ('django.db.models.fields.DateTimeField', [], {}),
            'who': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'builds.project': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Project'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'builds.repository': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Repository'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        }
    }

    complete_apps = ['builds']