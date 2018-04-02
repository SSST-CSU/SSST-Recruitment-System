# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import *
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'pwd', 'name', 'dept', 'job')


class MarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'ans', 'mark')


class AdmitAdmin(admin.ModelAdmin):
    list_display = ('person', 'result', 'attach')


admin.site.register(User, UserAdmin)
admin.site.register(Mark, MarkAdmin)
admin.site.register(Admit, AdmitAdmin)