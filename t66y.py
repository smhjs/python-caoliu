import requests
import re
import os
import threading
import random
import urllib
from bs4 import BeautifulSoup

proxies = { "http": "http://127.0.0.1:1080", "https": "http://127.0.0.1:1080" } 
#下载草榴图片
class down():
	
	def __init__(self): 
		#定义草榴域名	
		self.starturl="http://t66y.com/thread0806.php?fid=16"
		self.baseurl="http://t66y.com/"
		
		# 判断文件存放路径
		if "草榴" not in os.listdir(os.getcwd()):
			#创建草榴文件夹
			os.makedirs("草榴")

	#根据帖子地址下载图片
	def downloadimg(self,List_Url,dir10):
		try:
			#判断文件夹是否为空
			dir11=os.getcwd()+'/草榴/'+dir10
			if dir10 not in os.listdir(os.getcwd()+'/草榴'):
				os.makedirs(os.getcwd()+'/草榴/'+dir10)
			#获取发帖内容
			c=requests.get(self.baseurl+List_Url,proxies=proxies)
			c.encoding = 'gbk'
			soup=BeautifulSoup(c.text,"html.parser")
			#循环下载图片
			for x in soup.find_all('input',attrs={'type': 'image'}):
				print(x.get('src'))
				#获取图片名称
				filename=os.path.basename(x.get('src'))
				imgadd=dir11+"/"+filename
				#根据图片地址下载图片
				r=requests.get(x.get('src'),proxies=proxies)
				if r.status_code==200:
					with open(imgadd, 'wb') as file:
						file.write(r.content)
					print('下载成功：'+filename)
		except Exception as e:
			raise e

	#获取发帖列表

	def start(self,max_thread_num=100):
		try:
			#请求服务器内容 使用代理
			c=requests.get(self.starturl,proxies=proxies)
			c.encoding = 'gbk'
			thread_list=[]
			#解析服务器返回内容
			soup=BeautifulSoup(c.text,"html.parser")
			for x in soup.find_all('a',attrs={'href':re.compile('^htm_data')}):
				if x.parent.name=='h3':
					#获取帖子-链接http://t66y.com/thread0806.php?fid=16&search=&page=2
					if x.find('font') is None:
						listurl=x.get('href')
						thread_list.append(threading.Thread(target=self.downloadimg,args=(listurl,x.text)))
					else:
						listurl = x.get('href')
						thread_list.append(threading.Thread(target=self.downloadimg, args=(listurl, x.find('font').text)))
			for t in range(len(thread_list)):
				thread_list[t].start()
				print("NO."+str(t)+"线程启动")
				while True:
					if len(threading.enumerate())<max_thread_num:
						break

		except Exception as e:
			print(e)

	#def downimg(imageurl,imagedir):

if __name__ == '__main__':
	c=down()
	c.start()
	#c.getimgurl()