# -*- coding: UTF-8 -*-
import re
import pymysql
import codecs
from mylog import MyLog as mylog


log = mylog()
conn = pymysql.connect(host='localhost',user='root',password='159951',database='disease_archives')
cursor = conn.cursor()
sql = '''CREATE TABLE IF NOT EXISTS DATAA(
		data_id INT UNSIGNED AUTO_INCREMENT,
		sex VARCHAR(40),
		age VARCHAR(40),
		visiting_time VARCHAR(40),
		symptom VARCHAR(40),
		disease VARCHAR(40),
		PRIMARY KEY ( `data_id` )
	)CHARSET=UTF8MB4;'''
cursor.execute(sql)
log.info('建表成功')

with open('patient_record_vector.txt', encoding="utf-8") as f:
	for line in f:
		try:
			p = re.compile('p_\w+:|p_\w+。|p_\w+,|p_\w+-\w+-\w+:\w+:\w+,|p_\w+-\w+-\w+:\w+,')
			tems = p.findall(line)
			sex = tems[0][2]
			age = tems[1].lstrip('p_').rstrip(',')
			visitingTime = tems[2].lstrip('p_').rstrip(',')
			p = re.compile('s_\w+,')
			tems = p.findall(line)
			symptom = ''
			for tem in tems:
				symptom = symptom + tem.lstrip('s_').rstrip(',') + ',';
			symptom = symptom.rstrip(',')
			p = re.compile('d_\w+,?')
			tems = p.findall(line)
			disease = ''
			for tem in tems:
				disease = disease + tem.lstrip('d_').rstrip(',') + ',';
			disease = disease.rstrip(',')
		
			sql = "INSERT INTO DATAA(sex, \
					age, visiting_time, symptom, \
					disease) \
					VALUES ('%s', '%s', '%s', '%s', '%s')" % \
					(sex, age, visitingTime, symptom, disease)
			cursor.execute(sql)
			conn.commit()
		except:
			continue;
conn.close()	
