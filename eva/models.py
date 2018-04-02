# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from Task.models import Answer, ApplyForm
# Create your models here.
class User(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=5)
    pwd = models.CharField(max_length=20)
    # 部门
    dept = models.CharField(max_length=10)
    # 职务
    job = models.CharField(max_length=10)

    def __unicode__(self):
        return self.id


class Mark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_Mark', null=False)
    ans = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='ans_Mark', null=False)
    mark = models.IntegerField(null=False)

    def __unicode__(self):
        return unicode(self.id)


class Admit(models.Model):
    person = models.ForeignKey(ApplyForm, on_delete=models.CASCADE, related_name='person_Admit', null=False, primary_key=True)
    result = models.CharField(max_length=500, null=True, blank=True)
    attach = models.CharField(max_length=500, null=True, blank=True)