# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from models import *
from Task.models import *
import datas
# Create your views here.
def loginpage(request):
    return render(request, 'loginpage.html')


def login(request):
    print '*****admin login*****'
    id = request.POST['id']
    pwd = request.POST['pwd']
    dept = request.POST['dept']
    print 'id: %s'%(id)
    print 'password: %s'%(pwd)
    print 'department: %s'%(dept)
    try:
        u = User.objects.get(id=id, pwd=pwd, dept=dept)
        print 'login success'
    except:
        print 'login failed'
        return HttpResponseRedirect("/eva/index")
    return render(request, 'home.html', {
        'user': u
    })


def applyforms(request):
    ID = request.POST['id']
    user = User.objects.get(id=ID)
    print('%s enter applyforms' % (ID))
    applyform = ApplyForm.objects.all().order_by('first', 'second', 'id')
    return render(request, 'applyforms.html', {
        'user': user,
        'applyform': applyform
    })


def changepassword(request, ID):
    return render(request, 'changepwd.html', {
        'id': ID
    })


def change(request):
    id = request.POST['id']
    pwd = request.POST['pwd']
    npwd = request.POST['npwd']
    u = User.objects.get(id=id)
    print('***** %s enter change password *****'%(id))
    print('password: %s'%(pwd))
    print('new pswd: %s'%(npwd))
    if u.pwd == pwd:
        User.objects.filter(id=id).update(pwd=npwd)
        return HttpResponseRedirect('/eva/index')
    else:
        return HttpResponseRedirect('/eva/pwdcg/' + id)


def task1(request):
    ID = request.POST['id']
    user = User.objects.get(id=ID)
    print('%s enter task1'%(ID))
    q = Question.objects.get(id='1')
    ans = Answer.objects.filter(ques=q).order_by('user')
    return render(request, 'tasklist1.html', {
        'user': user,
        'ans': ans
    })


def task2(request):
    ID = request.POST['id']
    print('%s enter task2'%(ID))
    user = User.objects.get(id=ID)
    if user.dept == '主席团':
        ans = Answer.objects.filter(ques__id__in=['2', '3', '4', '5']).order_by('ques__id')
    elif user.dept == '综事部':
        ans = Answer.objects.filter(ques__id__in=['2'])
    elif user.dept == '竞赛部':
        ans = Answer.objects.filter(ques__id__in=['3'])
    elif user.dept == '双创部':
        ans = Answer.objects.filter(ques__id__in=['4'])
    elif user.dept == '技交部':
        ans = Answer.objects.filter(ques__id__in=['5'])
    datalist = []
    for a in ans:
        marklist = []
        avg = '0'
        if user.job == '副部长' or user.job == '干事':
            userlist = {}
            userlist[user.id] = user
            userlist0 = User.objects.filter(dept=user.dept)
            for u in userlist0:
                mark = ''
                marks = Mark.objects.filter(user=u, ans=a)
                if marks.count() == 0:
                    mark = '0'
                else:
                    mark = marks.first().mark
                    avg = str(float(avg) + float(mark))
                if u.id == ID:
                    marklist.append(marks.first())
            marknum = Mark.objects.filter(ans=a)
            if marknum.count() == 0:
                avg = '0'
            else:
                avg = str(float(avg) / float(marknum.count()))

        elif user.job == '部长':
            userlist = User.objects.filter(dept=user.dept)
            for u in userlist:
                mark = ''
                marks = Mark.objects.filter(user=u, ans=a)
                if marks.count() == 0:
                    mark = '0'
                else:
                    mark = marks.first().mark
                    avg = str(float(avg) + float(mark))
                marklist.append(marks.first())
            marknum = Mark.objects.filter(ans=a)
            if marknum.count() == 0:
                avg = '0'
            else:
                avg = str(float(avg) / float(marknum.count()))
        elif user.dept == '主席团':
            userlist = User.objects.all()
            for u in userlist:
                mark = ''
                marks = Mark.objects.filter(user=u, ans=a)
                if marks.count() == 0:
                    mark = '0'
                else:
                    mark = marks.first().mark
                    avg = str(float(avg) + float(mark))
                marklist.append(marks.first())
            marknum = Mark.objects.filter(ans=a)
            if marknum.count() == 0:
                avg = '0'
            else:
                avg = str(float(avg) / float(marknum.count()))

        info = {
            "aid": a.id,
            "id": a.user.id,
            "name": a.user.name,
            "dept": a.ques.id,
            "ans": a.ans,
            "marks": marklist,
            "avg": avg,
        }
        datalist.append(info)
    return render(request, 'tasklist2.html', {
        'user': user,
        'userlist': userlist,
        'list': datalist,
    })


def task3(request):
    ID = request.POST['id']
    print('%s enter task3'%(ID))
    user = User.objects.get(id=ID)
    datalist = []
    if user.dept != '主席团':
        ans = Answer.objects.filter(ques__id__in=['6', '7', '8', '9',
                                                  '10', '11', '12', '13',
                                                  '14', '15', '16', '17',]).order_by('ques__id')
    else:
        ans = Answer.objects.filter(ques__id__in=['6', '7', '8', '9',
                                                '10', '11', '12', '13',
                                                '14', '15', '16', '17',]).order_by('user')
    datalist = []
    for a in ans:
        a.ques_id = str(int(a.ques_id) - 5)
        marklist = []
        avg = '0'
        if user.job == '副部长' or user.job == '干事':
            userlist = {}
            userlist[user.id] = user
            userlist0 = User.objects.filter(dept=user.dept)
            for u in userlist0:
                mark = ''
                marks = Mark.objects.filter(user=u, ans=a)
                if marks.count() == 0:
                    mark = '0'
                else:
                    mark = marks.first().mark
                    avg = str(float(avg) + float(mark))
                if u.id == ID:
                    marklist.append(marks.first())
            marknum = Mark.objects.filter(ans=a, user__dept=user.dept)
            if marknum.count() == 0:
                avg = '0'
            else:
                avg = str(float(avg) / float(marknum.count()))

        elif user.job == '部长':
            userlist = User.objects.filter(dept=user.dept)
            for u in userlist:
                mark = ''
                marks = Mark.objects.filter(user=u, ans=a)
                if marks.count() == 0:
                    mark = '0'
                else:
                    mark = marks.first().mark
                    avg = str(float(avg) + float(mark))
                marklist.append(marks.first())
            marknum = Mark.objects.filter(ans=a, user__dept=user.dept)
            if marknum.count() == 0:
                avg = '0'
            else:
                avg = str(float(avg) / float(marknum.count()))
        elif user.dept == '主席团':
            userlist = User.objects.all()
            userlist0 = User.objects.filter(dept='主席团')
            userlist1 = User.objects.filter(dept='综事部')
            userlist2 = User.objects.filter(dept='竞赛部')
            userlist3 = User.objects.filter(dept='双创部')
            userlist4 = User.objects.filter(dept='技交部')
            avg = '0'
            for u in userlist0:
                mark = ''
                marks = Mark.objects.filter(user=u, ans=a)
                if marks.count() == 0:
                    mark = '0'
                else:
                    mark = marks.first().mark
                    avg = str(float(avg) + float(mark))
                    # marklist.append(marks.first())
            marknum = Mark.objects.filter(ans=a, user__dept='主席团')
            if marknum.count() == 0:
                avg = '0'
            else:
                avg = str(float(avg) / float(marknum.count()))
            m = Mark(mark=avg, user=user, ans=a)
            marklist.append(m)
            avg = '0'
            for u in userlist1:
                mark = ''
                marks = Mark.objects.filter(user=u, ans=a)
                if marks.count() == 0:
                    mark = '0'
                else:
                    mark = marks.first().mark
                    avg = str(float(avg) + float(mark))
                #marklist.append(marks.first())
            marknum = Mark.objects.filter(ans=a, user__dept='综事部')
            if marknum.count() == 0:
                avg = '0'
            else:
                avg = str(float(avg) / float(marknum.count()))
            m = Mark(mark=avg, user=user, ans=a)
            marklist.append(m)
            avg = '0'
            for u in userlist2:
                mark = ''
                marks = Mark.objects.filter(user=u, ans=a)
                if marks.count() == 0:
                    mark = '0'
                else:
                    mark = marks.first().mark
                    avg = str(float(avg) + float(mark))
                #marklist.append(marks.first())
            marknum = Mark.objects.filter(ans=a, user__dept='竞赛部')
            if marknum.count() == 0:
                avg = '0'
            else:
                avg = str(float(avg) / float(marknum.count()))
            m = Mark(mark=avg, user=user, ans=a)
            marklist.append(m)
            avg = '0'
            for u in userlist3:
                mark = ''
                marks = Mark.objects.filter(user=u, ans=a)
                if marks.count() == 0:
                    mark = '0'
                else:
                    mark = marks.first().mark
                    avg = str(float(avg) + float(mark))
                    # marklist.append(marks.first())
            marknum = Mark.objects.filter(ans=a, user__dept='双创部')
            if marknum.count() == 0:
                avg = '0'
            else:
                avg = str(float(avg) / float(marknum.count()))
            m = Mark(mark=avg, user=user, ans=a)
            marklist.append(m)
            avg = '0'
            for u in userlist4:
                mark = ''
                marks = Mark.objects.filter(user=u, ans=a)
                if marks.count() == 0:
                    mark = '0'
                else:
                    mark = marks.first().mark
                    avg = str(float(avg) + float(mark))
                    # marklist.append(marks.first())
            marknum = Mark.objects.filter(ans=a, user__dept='技交部')
            if marknum.count() == 0:
                avg = '0'
            else:
                avg = str(float(avg) / float(marknum.count()))
            m = Mark(mark=avg, user=user, ans=a)
            marklist.append(m)
            avg = '0'
            avg = str((float(marklist[0].mark) + float(marklist[1].mark) + float(marklist[2].mark) + float(marklist[3].mark) + float(marklist[4].mark)) / 5)
        info = {
            "aid": a.id,
            "id": a.user.id,
            "name": a.user.name,
            "dept": a.ques.id,
            "ans": a.ans,
            "marks": marklist,
            "avg": avg,
        }
        datalist.append(info)

    return render(request, 'tasklist3.html', {
        'user': user,
        'userlist': userlist,
        'list': datalist,
    })


def interviewlist(request):
    dept = {
        '2': '综事部',
        '3': '竞赛部',
        '4': '双创部',
        '5': '技交部',
    }
    ID = request.POST['id']
    print('%s enter interviewlist' % (ID))
    user = User.objects.get(id=ID)
    applyform = ApplyForm.objects.all().order_by('first', 'second', 'id')
    answer = Answer.objects.all().order_by('ques_id')
    list1 = []
    list2 = []
    num1 = 0
    num2 = 0
    for a in applyform:
        com = True
        id = a.id
        name = a.name
        first = a.first
        second = a.second
        answer1 = answer.filter(ques__id='1', user=a)
        ans1 = ''
        if answer1.count() == 0:
            com = False
            ans1 = 'None'
        answer2 = answer.filter(ques__id__in=['2', '3', '4', '5'], user=a)
        ans2 = ''
        if answer2.count() == 0:
            com = False
            ans2 = 'None'
        else:
            """
            for aa in answer2:
                ans2 = ans2 + dept[aa.ques_id.__str__()]
                if answer2.count() > 1:
                    ans2 = ans2 + '、'
            """
            for index in range(len(answer2)):
                ans2 = ans2 + dept[answer2[index].ques_id.__str__()]
                if index != len(answer2) - 1:
                    ans2 = ans2 + '、'
        answer3 = answer.filter(ques__id__in=['6', '7', '8', '9',
                                              '10', '11', '12', '13',
                                              '14', '15', '16', '17', ], user=a)
        ans3 = ''
        if answer3.count() < 3:
            com = False
        if answer3.count() == 0:
            ans3 = 'None'
        else:
            for index in range(len(answer3)):
                ans3 = ans3 + str(int(answer3[index].ques_id.__str__()) - 5)
                if index != len(answer3) - 1:
                    ans3 = ans3 + '、'
        num = 0
        if com:
            num = num1 + 1
            num1 = num1 + 1
        else:
            num = num2 + 1
            num2 = num2 + 1
        info = {
            "no": num,
            "id": id,
            "name": name,
            "first": first,
            "second": second,
            "ans1": ans1,
            "ans2": ans2,
            "ans3": ans3,
        }
        if com:
            list1.append(info)
        else:
            list2.append(info)
    return render(request, 'interviewlist.html', {
        "list1": list1,
        "list2": list2,
        "user": user,
    })


def save2(request):
    uid = request.POST['uid']
    aid = request.POST['aid']
    mark = request.POST['mark']
    print uid
    print aid
    print mark
    user = User.objects.get(id=uid)
    ans = Answer.objects.get(id=aid)
    try:
        m = Mark.objects.filter(user=user, ans=ans)
        if m.count() == 0:
            print '%s create mark %s for %s'%(uid, mark, ans.ques_id)
            Mark.objects.create(user=user, ans=ans, mark=mark)
        else:
            print '%s update mark %s for %s' % (uid, mark, ans.ques_id)
            m.update(mark=mark)
    except:
        pass
    ret = {'msg': '1'}
    return HttpResponse(json.dumps(ret))


def save3(request):
    uid = request.POST['uid']
    aid = request.POST['aid']
    mark = request.POST['mark']
    print uid
    print aid
    print mark
    aid = aid
    user = User.objects.get(id=uid)
    ans = Answer.objects.get(id=aid)
    try:
        m = Mark.objects.filter(user=user, ans=ans)
        if m.count() == 0:
            print '%s create mark %s for %s'%(uid, mark, ans.ques_id)
            Mark.objects.create(user=user, ans=ans, mark=mark)
        else:
            print '%s update mark %s for %s' % (uid, mark, ans.ques_id)
            m.update(mark=mark)
    except:
        pass
    ret = {'msg': '1'}
    return HttpResponse(json.dumps(ret))