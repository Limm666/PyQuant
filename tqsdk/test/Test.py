# -*- coding:utf-8 -*- 
# author: limm_666

import re

s1 = '通过几天Python的学习，感觉Python很简单，非常容易上手！'
print(re.findall('Python', s1))
print("-------------------------------------")

s2 = '此次新朗逸主要搭载了1.5L和1.5T两种动力总成的发动机。别克英朗则搭载了1.0T和1.3T的动力总成。'
print(re.findall('1..', s2))
print(re.findall('1\...', s2))
print("-------------------------------------")

# 剔除字符串中的所有空白
s3 = ' 距离2019北京马拉松开跑只有两周时间了，\n今年的北京马拉松预报名人数超过16万人，\t 媒体公布的中签率只有16%左右，再创历年来的新低。\n'
print(s3)
re.sub('\s','',s3)
print("-------------------------------------")

# 取出手机号信息
s4 = '用户联系方式：13612345566，用户编号为11011254321'
print(re.findall('1[1356789]\d*', s4))
# 提取出动力总成
s5 = '通过对比新朗逸1.5L和1.5T两种动力在1.5年行驶期后的数据。发现1.5T的口碑相对较好！'
print(re.findall('1.5[a-zA-Z]',s5))
print("-------------------------------------")

# 提取出用户的年龄
s6 = 'id:1, name:Tom, age:3, gender:1; id:2, name:Lily, age:5, gender:0'
print(re.findall('\d',s6))
print(re.findall('age:\d',s6))
print(re.findall('age:(\d)',s6))
# 注意这个括号
