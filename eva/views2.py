# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from models import *
from Task.models import *
# Create your views here.


def marklist(request):
    applyform = ApplyForm.objects.all()
    datalist = []
    for a in applyform:
        data = {}
        data["user"] = a
        # 第一次考核
        try:
            ans1 = Answer.objects.get(user=a, ques__id='1')
            data["res1"] = "合格"
        except:
            data["res1"] = "未提交"

        # 第二次考核
        marktmp2 = []
        num2 = [0] * 4
        x = ['2', '3', '4', '5']
        mark2 = Mark.objects.filter(ans__ques__id__in=x, ans__user=a)
        for index in range(len(x)):
            num2[index] = mark2.filter(ans__ques__id=x[index]).count()
        avg = [0.0] * 4
        for index in range(len(num2)):
            if num2[index] != 0:
                for m in mark2.filter(ans__ques__id=str(index+2)):
                    avg[index] += float(m.mark)
                avg[index] /= float(mark2.filter(ans__ques__id=str(index+2)).count())
                avg[index] = format(avg[index], '.2f')
            info = {
                "id": str(index+1),
                "mark": avg[index],
            }
            marktmp2.append(info)
        # 0分数量，4次未提交
        zero2 = 0
        markavg21 = '0.0'
        markavg22 = '0.0'
        for index in range(len(marktmp2)):
            if float(marktmp2[index]["mark"]) == 0.0:
                zero2 += 1
            else:
                if markavg21 == '0.0':
                    markavg21 = marktmp2[index]["mark"]
                else:
                    markavg22 = marktmp2[index]["mark"]
        if zero2 == 4:
            info = {
                "id": 4,
                "mark": "无效",
            }
            marktmp2.append(info)
        elif zero2 == 3:
            info = {
                "id": 4,
                "mark": markavg21,
            }
            marktmp2.append(info)
        elif zero2 == 2:
            info = {
                "id": 4,
                "mark": format((float(markavg21) + float(markavg22)) / 2, '.2f'),
            }
            marktmp2.append(info)
        data["res2"] = marktmp2


        # 第三次考核
        marktmp3 = []
        num3 = [0] * 12
        y = ['6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17',]
        mark3 = Mark.objects.filter(ans__ques__id__in=y, ans__user=a)
        for index in range(len(y)):
            num3[index] = mark3.filter(ans__ques__id=y[index]).count()
        avg = [0.0] * len(num3)
        for index in range(len(num3)):
            if num3[index] != 0:
                # 计算各部门平均分
                tmp0 = 0.0
                tmp1 = 0.0
                tmp2 = 0.0
                tmp3 = 0.0
                tmp4 = 0.0

                for m in mark3.filter(ans__ques__id=str(index + 6), user__dept='主席团'):
                    tmp0 += float(m.mark)
                if mark3.filter(ans__ques__id=str(index + 6), user__dept='主席团').count() != 0:
                    tmp0 /= float(mark3.filter(ans__ques__id=str(index + 6), user__dept='主席团').count())
                else:
                    tmp0 = 0.0

                for m in mark3.filter(ans__ques__id=str(index + 6), user__dept='综事部'):
                    tmp1 += float(m.mark)
                if mark3.filter(ans__ques__id=str(index + 6), user__dept='综事部').count() != 0:
                    tmp1 /= float(mark3.filter(ans__ques__id=str(index + 6), user__dept='综事部').count())
                else:
                    tmp1 = 0.0

                for m in mark3.filter(ans__ques__id=str(index + 6), user__dept='竞赛部'):
                    tmp2 += float(m.mark)
                if mark3.filter(ans__ques__id=str(index + 6), user__dept='竞赛部').count() != 0:
                    tmp2 /= float(mark3.filter(ans__ques__id=str(index + 6), user__dept='竞赛部').count())
                else:
                    tmp2 = 0.0

                for m in mark3.filter(ans__ques__id=str(index + 6), user__dept='双创部'):
                    tmp3 += float(m.mark)
                if mark3.filter(ans__ques__id=str(index + 6), user__dept='双创部').count() != 0:
                    tmp3 /= float(mark3.filter(ans__ques__id=str(index + 6), user__dept='双创部').count())
                else:
                    tmp3 = 0.0

                for m in mark3.filter(ans__ques__id=str(index + 6), user__dept='技交部'):
                    tmp4 += float(m.mark)
                if mark3.filter(ans__ques__id=str(index + 6), user__dept='技交部').count() != 0:
                    tmp4 /= float(mark3.filter(ans__ques__id=str(index + 6), user__dept='技交部').count())
                else:
                    tmp4 = 0.0

                # 本题得分
                avg[index] = (tmp0 + tmp1 + tmp2 + tmp3 + tmp4) / 5
                avg[index] = format(avg[index], '.2f')
            info = {
                "id": str(index+1),
                "mark": avg[index],
            }
            marktmp3.append(info)
        zero3 = 0
        markavg3 = ['0.0'] * 10
        iiiiii222 = 0
        for index in range(len(marktmp3)):
            if float(marktmp3[index]["mark"]) == 0.0:
                zero3 += 1
            else:
                if markavg3[iiiiii222] == '0.0':
                    markavg3[iiiiii222] = marktmp3[index]["mark"]
                    iiiiii222 += 1
        if zero3 > 9:
            info = {
                "id": 13,
                "mark": "无效",
            }
            marktmp3.append(info)
        else:
            sum = 0.0
            for e in markavg3:
                sum += float(e)
            sum /= (12-zero3)
            info = {
                "id": 13,
                "mark": str(format(sum, '.2f')),
            }
            marktmp3.append(info)
        data["res3"] = marktmp3
        # 面试
        res4 = ''
        try:
            ans4 = Answer.objects.get(user=a, ques__id='18')
            #mark4 = Mark.objects.get(ans__user=a, ans__ques__id='18')
            #data["res4"] = mark4.mark
            mark4 = Answer.objects.get(user=a, ques__id='18')
            data["res4"] = format(float(mark4.ans), '.2f')
        except:
            data["res4"] = "未参加"
        datalist.append(data)

        # 考核二
        if data["res2"][4]["mark"] != "无效":
            x1 = float(data["res2"][4]["mark"])
        else:
            x1 = 0.0

        # 考核三
        if data["res3"][12]["mark"] != "无效":
            x2 = float(data["res3"][12]["mark"])
        else:
            x2 = 0.0

        # 面试
        if data["res4"] != "未参加":
            x3 = float(data["res4"])
        else:
            x3 = 0.0

        data["avg"] = format(x1 * 0.25 + x2 * 0.21 + x3 * 0.54, '.2f')

        # 录取结果
        try:
            r = Admit.objects.get(person=a)
            data["result"] = r.result
            data["attach"] = r.attach
        except:
            data["result"] = "未录取"
            data["attach"] = ""

    datalist.sort(key=lambda x: -float(x["avg"]))
    i = 0
    for data in datalist:
        i += 1
        data["no"] = i

    return render(request, 'marklist.html', {
        "datalist": datalist,
    })


"""
data = {
    "user": "applyform",
    "res1": "",
    "res2": [
        {
            "id": "id",
            "mark": "mark",
        },
    ],
    "res3": [
        {
            "id": "id",
            "mark": "mark",
        },
    ]
    "res4": "",
    "avg": 0,
    "result": "",
}
"""