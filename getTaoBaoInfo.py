# -*- coding: UTF-8 -*-
import urllib.request
import urllib.parse
import time
from bs4 import BeautifulSoup
import pymysql
from mylog import MyLog as mylog
import codecs


class Item(object):
	title = None   #商品名
	prePrice = None		#降价以前的价格
	nowPrice = None		#现在的价格
	soldNum = None		#抢购数量
	url = None		#商品地址
	kind = None		#商品种类
	
class GetTaoBaoInfo(object):	#爬虫类
	def __init__(self,url):
		self.url = url
		self.log = mylog()
		self.urlsGoodsType = self.getUrlsGoodsType()	#爬出所有商品的url
		self.items = self.spider(self.urlsGoodsType)	#逐个爬取商品
		self.pipelines(self.items)
		self.saveItemsToDB()	#存到mysql中
		
	def getUrlsGoodsType(self):
		urlsGoodsType = {}
		htmlContent = self.getResponseContent(self.url)
		soup = BeautifulSoup(htmlContent,'lxml')
		tagul = soup.find('ul',attrs={'class':'category'})
		tagsli = tagul.find_all('li')
		for tag in tagsli:
			urlsGoodsType[tag.a.get_text()] = tag['data-href'].strip()
		self.log.info('获得urls成功')
		return urlsGoodsType
		
	
	def spider(self,urlsGoodsType):
		items = []
		for k, v in urlsGoodsType.items():
			htmlContent = self.getResponseContent(v)
			soup = BeautifulSoup(htmlContent,'lxml')
			tagsa = soup.find_all('a',attrs={'class':'qg-item qg-ing'})
			for tag in tagsa:
				item = Item()
				item.kind = k
				item.url = tag['href'].strip()
				item.title = tag.find('p',attrs={'class':'des'}).get_text().strip()
				item.prePrice = tag.find('span',attrs={'class':'original-price'}).get_text().strip('¥') 
				item.nowPrice = tag.find('span',attrs={'class':'promo-price'}).get_text().strip('¥')
				item.soldNum = tag.find('span',attrs={'class':'num'}).get_text().strip('已抢件')
				items.append(item)
				self.log.info('成功获取%s的信息' %item.title)
		return items
		

	def getResponseContent(self,url):
		time.sleep(1)
		urlList = url.split('=')
		url = '='.join(urlList)
		try:
			response = urllib.request.urlopen(url)
		except:
			self.log.error('连接%s失败' %url)
		else:
			temStr = response.read()
			response.close()
			return temStr
		
	def saveItemsToDB(self):   #将数据存到数据库goodsinformation中，密码为159951，用户名root
		conn = pymysql.connect(host='localhost',user='root',password='159951',database='goodsinformation')
		cursor = conn.cursor()
		sql = """CREATE TABLE IF NOT EXISTS TAOBAO( 
				goods_id INT UNSIGNED AUTO_INCREMENT, 
				goods_kind VARCHAR(40), 
				goods_title VARCHAR(100), 
				goods_prePrice VARCHAR(40), 
				goods_nowPrice VARCHAR(40), 
				goods_soldNum VARCHAR(100), 
				goods_url VARCHAR(100), 
				PRIMARY KEY ( `goods_id` ) 
			)CHARSET=utf8;"""
		cursor.execute(sql)
		self.log.info('建立数据表成功')
		for item in self.items:
			sql = "INSERT INTO TAOBAO(goods_kind, \
					goods_title, goods_prePrice, goods_nowPrice, \
					goods_soldNum, goods_url) \
					VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % \
					(item.kind, item.title, item.prePrice, item.nowPrice, item.soldNum, item.url)
			try:
				cursor.execute(sql)
				conn.commit()
			except:
				self.log.error('存入数据库出错')
		conn.close()
	
	
	def pipelines(self,items):
		filename = '淘宝打折商品.txt'
		with codecs.open(filename,'w','utf-8') as fp:
			for item in items:
				try:
					fp.write('%s\r\n' %item.title)
				except Exception as e:
					self.log.error('failed in write')
				else:
					self.log.info('success in write')	
				
url = 'https://qiang.taobao.com/'
GTBI = GetTaoBaoInfo(url)			
