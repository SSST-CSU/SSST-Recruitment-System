# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import httplib
import json

import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
import MySQLdb
from django.views.decorators.csrf import csrf_exempt

from models import *
# Create your views here.

@csrf_exempt
def page_not_found(request):
	return HttpResponseRedirect("http://115.159.217.104:8080/404.jsp")


@csrf_exempt
def page_error(request):
	return HttpResponseRedirect("http://115.159.217.104:8080/500.jsp")


def applyForm(request, ID):
    time = datetime.datetime.now()
    print('time: %s' % (time.__str__()))
    stat = ''
    if time > datetime.datetime(year=2017, month=10, day=9):
        stat = 'readonly=\"readonly\"'
        print stat
    print "*****" + ID + ' Enter ApplyForm *****'
    userInfo = {}
    try:
        u = ApplyForm.objects.get(id=ID)
        userInfo = {
            'id': u.id,
            'name': u.name,
            'sex': u.sex,
            'political': u.political,
            'place': u.place,
            'classes': u.classes,
            'qq': u.qq,
            'tel': u.tel,
            'swap': u.swap,
            'first': u.first,
            'second': u.second,
            'award': u.award,
            'tink': u.tink,
            'advice': u.advice,
            'attach': u.attach,
            'stat': stat,
        }
        print "Apply Form Exist, get userInfo"
    except:
        print 'Apply Form Not Exist'
        db = MySQLdb.connect('localhost', 'root', '', 'sta')
        cur = db.cursor()
        print cur
        sql = "SELECT * FROM person WHERE account=" + ID
        try:
            cur.execute(sql)
            r = cur.fetchall()
            print 'Data in MySQL:'
            if r == ():
                return HttpResponseRedirect("http://115.159.217.104:8080/404.jsp")
            for row in r:
                name = row[1]
                classes = row[2]
                tel = row[7]
                qq = row[9]
                print 'name:' + name
                userInfo = {
                    'id': ID,
                    'name': name,
                    'sex': '',
                    'political': '',
                    'place': '',
                    'classes': classes,
                    'qq': qq,
                    'tel': tel,
                    'swap': '',
                    'first': '',
                    'second': '',
                    'award': '',
                    'tink': '',
                    'advice': '',
                    'attach': '',
                    'stat': stat,
                }
        except:
            print "Error(applyForm): unable to fecth data in MySQL"
            db.close()
            return HttpResponseRedirect("http://115.159.217.104:8080/404.jsp")
        db.close()
    return render(request, 'applyForm.html', userInfo)


def index(request, id):
    #id = request.POST['id']
    print "*****" + id + " Enter tasklist*****"
    time = datetime.datetime.now()
    print('time: %s'%(time.__str__()))
    end11 = ''
    end12 = ''
    end21 = ''
    interview = ''
    if time > datetime.datetime(year=2017, month=10, day=9):
        end11 = '/*'
        end12 = '*/'
    if time > datetime.datetime(year=2017, month=10, day=11, hour=12, minute=30):
        end21 = '*/'
    """
    db= MySQLdb.connect('localhost', 'root', '', 'sta')
    cur = db.cursor()
    sql = "SELECT * FROM person WHERE account=" + id
    userInfo = {}
    try:
        cur.execute(sql)
        r = cur.fetchall()
        if r == ():
            return HttpResponseRedirect("http://115.159.217.104:8080/404.jsp")
        print 'Data in MySQL:'
        print r
        for row in r:
            name = row[1]
            classes = row[2]
            department = row[3]
            mail = row[4]
            acount = row[5]
            password = row[6]
            tel = row[7]
            isMember = row[8]
            qq = row[9]
            wechat = row[10]
            introduce = row[11]
            job = row[12]
            protrait = row[13]
            userInfo = {
                            'name': name,
                            'classes': classes,
                            'department': department,
                            'mail': mail,
                            'account': acount,
                            'password': password,
                            'tel': tel,
                            'isMember': isMember,
                            'qq': qq,
                            'wechat': wechat,
                            'introduce': introduce,
                            'job': job,
                            'protrait': protrait,
                            'end11': end11,
                            'end12': end12,
                            'end21': end21,
                            'interview': interview,
                        }
    except:
        print "Error(index): unable to fecth data"
        db.close()
        return
    db.close()
    """
    userInfo = {}
    try:
        user = ApplyForm.objects.get(id=id)
        ans1 = Answer.objects.filter(ques__id='1', user=user)
        ans2 = Answer.objects.filter(ques__id__in=['2', '3', '4', '5'], user=user)
        ans3 = Answer.objects.filter(ques__id__in=['6', '7', '8', '9',
                                                   '10', '11', '12', '13',
                                                   '14', '15', '16', '17', ], user=user)
        if ans1.count() == 0:
            interview = '请完成考核任务一'
        elif ans2.count() == 0:
            interview = '请完成考核任务二'
        elif ans3.count() < 3:
            interview = '请完成考核任务三'
        else:
            interview = '你已具有面试资格'
        userInfo = {
            'name': user.name,
            'classes': user.classes,
            'account': user.id,
            'tel': user.tel,
            'qq': user.qq,
            'end11': end11,
            'end12': end12,
            'end21': end21,
            'interview': interview,
        }
    except:
        print "Error(index): unable to fecth data"
        return HttpResponseRedirect("http://115.159.217.104:8080/404.jsp")
    return render(request, 'index.html', userInfo)

def loginpage(request):
    return render(request, 'login.html')


def login(request):
    id = request.POST['id']
    name = request.POST['name']
    success = False
    try:
        u = ApplyForm.objects.get(id=id)
        if u.name == name:
            success = True
    except:
        pass
    if success:
        return index(request, id)


def applyform(request):
    ID = request.POST['id']
    Name = request.POST['name']
    Sex = request.POST['sex']
    Political = request.POST['political']
    Place = request.POST['place']
    Classes = request.POST['classes']
    QQ = request.POST['qq']
    Tel = request.POST['tel']
    Swap = request.POST['swap']
    First = request.POST['first']
    Second = request.POST['second']
    Award = request.POST['award']
    Tink = request.POST['tink']
    Advice = request.POST['advice']
    Attach = request.POST['attach']
    print '*****' + ID + ' Apply*****'
    try:
        u = ApplyForm.objects.get(id=ID)
        ApplyForm.objects.filter(id=ID).update(name=Name,
                                               sex=Sex,
                                               political=Political,
                                               place=Place,
                                               classes=Classes,
                                               qq=QQ,
                                               tel=Tel,
                                               swap=Swap,
                                               tink=Tink,
                                               advice=Advice,
                                               attach=Attach,
                                               award=Award,
                                               first=First,
                                               second=Second)
        print 'apply update'
        print 'id:' + ID
        print 'sex:' + Sex
        print 'pol:' + Political
        print 'pla:' + Place
    except:
        ApplyForm.objects.create(
                id = ID,
                name = Name,
                sex = Sex,
                political = Political,
                place = Place,
                classes = Classes,
                qq = QQ,
                tel = Tel,
                swap = Swap,
                first = First,
                second = Second,
                award = Award,
                tink = Tink,
                advice = Advice,
                attach = Attach)
        print 'apply create'
    return render(request, 'result.html',
                  {
                      'name': Name,
                      'id': ID,
                  })


def task1(request, ID):
    print '*****' + ID + ' Enter task1*****'
    time = datetime.datetime.now()
    print('time: %s' % (time.__str__()))
    stat = ''
    if time > datetime.datetime(year=2017, month=10, day=9):
        stat = 'readonly=\"readonly\"'
        print stat
    ques = Question.objects.get(id='1')
    print 'Question ID : ' + ques.id
    print 'Question : ' + ques.q
    try:
        u = ApplyForm.objects.get(id=ID)
    except:
        print 'No Apply, go to apply form from task1'
        return HttpResponseRedirect("/applyForm/" + ID)
    name = u.name
    id = u.id
    ans = ''
    try:
        a = Answer.objects.get(user=u, ques=ques)
        print a
        ans = a.ans
        print 'ans exist: ' + ans
    except:
        pass
    return render(request, 'task1.html',
                  {
                      'id': id,
                      'name': name,
                      'ans': ans,
                      'stat': stat,
                  })


def task2(request, ID):
    print '*****' + ID + 'Enter task2*****'
    time = datetime.datetime.now()
    print('time: %s' % (time.__str__()))
    stat = ''
    if time > datetime.datetime(year=2017, month=10, day=9):
        stat = 'readonly=\"readonly\"'
        print stat
    try:
        u = ApplyForm.objects.get(id=ID)
    except:
        print 'No Apply, go to apply form from task2'
        return HttpResponseRedirect("/applyForm/" + ID)
    name = u.name
    id = u.id
    return render(request, 'task2.html',
                  {
                      'id': id,
                      'name': name,
                      'stat': stat,
                  })


def task3(request, ID):
    print '*****' + ID + 'Enter task3*****'
    time = datetime.datetime.now()
    print('time: %s' % (time.__str__()))
    stat = ''
    if time > datetime.datetime(year=2017, month=10, day=11, hour=12, minute=30):
        stat = 'readonly=\"readonly\"'
        print stat
    try:
        u = ApplyForm.objects.get(id=ID)
    except:
        print 'No Apply, go to apply form from task3'
        return HttpResponseRedirect("/applyForm/" + ID)
    name = u.name
    id = u.id
    return render(request, 'task3.html',
                  {
                      'id': id,
                      'name': name,
                      'stat': stat,
                  })



def task(request, times, ID):
    time = datetime.datetime.now()
    print 'time: '
    print time

    if times == '1':
        return task1(request, ID)
    if times == '2':
        return task2(request, ID)
    if times == '3':
        return task3(request, ID)


def addAnswer1(request):
    id = request.POST['id']
    u = ApplyForm.objects.get(id=id)
    name = request.POST['name']
    q = Question.objects.get(id='1')
    ans = request.POST['ans']
    print '*****get answer 1*****'
    print 'id:%s'%(id)
    print 'name:%s'%(name)
    print 'ans:'
    print ans
    a = Answer.objects.filter(user=u, ques=q)
    print a.count()
    if a.count() != 0:
        print 'update answer\t%s'%(ans)
        a.update(ans=ans)
        print 'update success'
    else:
        print 'create answer:\t%s\t%s\t%s'%(u, q, ans)
        Answer.objects.create(user=u, ques=q, ans=ans)
        print 'create success'
    return HttpResponseRedirect("/tasklist/" + id)


def addAnswer2(request):
    id = request.POST['id']
    u = ApplyForm.objects.get(id=id)
    name = request.POST['name']
    dept = request.POST['dept']
    if dept == '综事部':
        q = Question.objects.get(id='2')
    elif dept == '竞赛部':
        q = Question.objects.get(id='3')
    elif dept == '双创部':
        q = Question.objects.get(id='4')
    else:
        q = Question.objects.get(id='5')
    ans = request.POST['ans']
    print '*****get answer 2*****'
    print 'id:%s' % (id)
    print 'name:%s' % (name)
    print 'ans:'
    print ans
    a = Answer.objects.filter(user=u, ques=q)
    print a.count()
    if a.count() != 0:
        print 'update answer\t%s'%(ans)
        a.update(ans=ans)
        print 'update success'
    else:
        print 'create answer\t%s\t%s\t%s'%(u, q, ans)
        Answer.objects.create(user=u, ques=q, ans=ans)
        print 'create success'
    return HttpResponseRedirect("/tasklist/" + id)


def addAnswer3(request):
    id = request.POST['id']
    u = ApplyForm.objects.get(id=id)
    name = request.POST['name']
    quesid = request.POST['dept']
    q = Question.objects.get(id=quesid)
    ans = request.POST['ans']
    print '*****get answer %s*****' % (quesid)
    print 'id:%s'%(id)
    print 'name:%s'%(name)
    print 'ans:'
    print ans
    a = Answer.objects.filter(user=u, ques=q)
    print a.count()
    if a.count() != 0:
        print 'update answer\t%s'%(ans)
        a.update(ans=ans)
        print 'update success'
    else:
        print 'create answer\t%s\t%s\t%s'%(u, q, ans)
        Answer.objects.create(user=u, ques=q, ans=ans)
        print 'create success'
    return index(request, id)


def ajax2(request):
    if request.method == 'POST':
        dept = request.POST['dept']
        id = request.POST['id']
        print '***** AJAX2 ' + id + ' post ' + dept + '*****'
        u = ApplyForm.objects.get(id=id)
        print 'Get the user:' + u.name
        quesid = ''
        if dept == '综事部':
            quesid = '2'
        elif dept == '竞赛部':
            quesid = '3'
        elif dept == '双创部':
            quesid = '4'
        else:
            quesid = '5'
        q = Question.objects.get(id=quesid)
        ques = q.q
        print 'Find the question:' + ques
        ans = ''
        try:
            a = Answer.objects.filter(user=u, ques=q)
            ans = a.first().ans
            print 'answer exist:' + ans
        except:
            pass
        ret = {'ques': ques, 'answer': ans}
        return HttpResponse(json.dumps(ret))


def ajax3(request):
    if request.method == 'POST':
        quesid = request.POST['dept']
        id = request.POST['id']
        print '***** AJAX3 ' + id + ' post ' + quesid + '*****'
        u = ApplyForm.objects.get(id=id)
        print 'Get the user:' + u.name
        q = Question.objects.get(id=quesid)
        ques = q.q
        print 'Find the question:' + ques
        ans = ''
        try:
            a = Answer.objects.filter(user=u, ques=q)
            ans = a.first().ans
            print 'answer exist:' + ans
        except:
            pass
        ret = {'ques': ques, 'answer': ans}
        return HttpResponse(json.dumps(ret))