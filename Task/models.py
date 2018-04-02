# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
# Create your models here.


class ApplyForm(models.Model):
    id = models.CharField(max_length=10, primary_key=True, null=False)
    name = models.CharField(max_length=5, null=False)
    sex = models.CharField(max_length=1, null=False)
    political = models.CharField(max_length=10, null=False)
    # 籍贯
    place = models.CharField(max_length=30)
    classes = models.CharField(max_length=4, null=False)
    qq = models.CharField(max_length=15, null=False)
    tel = models.CharField(max_length=20, null=False)
    swap = models.CharField(max_length=1, null=False)
    first = models.CharField(max_length=8, null=False)
    second = models.CharField(max_length=8, null=True, blank=True)
    # 本人获奖情况及特长、技能等
    award = models.TextField(max_length=500, null=True, blank=True)
    # 对学生机构干部工作的想法
    tink = models.TextField(max_length=500, null=True, blank=True)
    # 对学院发展及对学生工作的建议
    advice = models.TextField(max_length=500, null=True, blank=True)
    # 备注
    attach = models.TextField(max_length=500, null=True, blank=True)

    def __unicode__(self):
        return self.id


class Question(models.Model):
    id = models.CharField(primary_key=True, max_length=5)
    q = models.TextField(max_length=500, null=False)

    def __unicode__(self):
        return self.id


class Answer(models.Model):
    user = models.ForeignKey(ApplyForm, on_delete=models.CASCADE, related_name='ApplyForm_Answer', null=False)
    ques = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='Question_Answer', null=False)
    ans = models.TextField(max_length=1024)

    def __unicode__(self):
        return unicode(self.id)