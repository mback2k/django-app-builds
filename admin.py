# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Project, Repository, Change, Builder, Build

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class RepositoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class ChangeAdmin(admin.ModelAdmin):
    list_display = ('project', 'repository', 'revision', 'when', 'who')
    list_filter = ('project', 'repository', 'when')
    search_fields = ('revision', 'comments', 'who')
    #date_hierarchy = 'when'

class BuilderAdmin(admin.ModelAdmin):
    list_display = ('name', 'link')
    search_fields = ('name', 'link')

class BuildAdmin(admin.ModelAdmin):
    filter_horizontal = ('changes',)
    list_display = ('builder', 'number', 'result', 'simplified_result',
                    'start_time', 'end_time', 'duration')
    list_filter = ('builder', 'result', 'simplified_result', 'start_time')
    search_fields = ('changes__revision', 'changes__comments', 'changes__who')
    #date_hierarchy = 'start_time'

admin.site.register(Project, ProjectAdmin)
admin.site.register(Repository, RepositoryAdmin)
admin.site.register(Change, ChangeAdmin)
admin.site.register(Builder, BuilderAdmin)
admin.site.register(Build, BuildAdmin)
