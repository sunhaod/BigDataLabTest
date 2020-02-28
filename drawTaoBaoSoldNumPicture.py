# -*- coding: UTF-8 -*-
import matplotlib.pyplot as plt
import pymysql
import numpy as np
from mylog import MyLog as mylog

log = mylog()
conn = pymysql.connect('localhost','root','159951','goodsinformation')
cursor = conn.cursor()
sql = '''SELECT goods_kind, goods_soldNum from taobao'''
kind = []
num = []

cursor.execute(sql)
results = cursor.fetchall()
temNum = 0
temKind = results[0][0]
for row in results:
	if temKind != row[0]:
		kind.append(temKind)
		num.append(temNum)
		temKind = row[0]
		temNum = int(row[1])
	else:
		temNum = temNum + int(row[1])

plt.rcParams['font.sans-serif'] = ['KaiTi']
plt.rcParams['axes.unicode_minus'] = False
plt.bar(np.arange(len(num)),num,0.35)
plt.ylabel('销售数量')
plt.title('淘宝打折商品销售情况')
plt.xticks(np.arange(len(num)),kind,rotation=60)
ly = min(num)//100 * 100
hy = (max(num)//100 + 1) * 100
plt.yticks(np.arange(ly,hy,(hy-ly)/10))

for x,y in zip(np.arange(len(num)),num):
    plt.text(x+0.05,y+0.05,'%.0f' %y, ha='center',va='bottom')

plt.show()
