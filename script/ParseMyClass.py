# -*- encoding: utf-8 -*-
import urllib.request
import re
import sys

"""
ОПИСАНИЕ
скрипт парсит страницы LENTA.ru сы ссылками вида "https://lenta.ru/articles/..." и "https://lenta.ru/news/..."
для того чтобы определить еще какие либо страницы, можно составить регулярное выражение, 
и вставить проверку параметра self.article на пустоту, если он будет пустой, тогда можно 
регуляркой вытащить другой тег, не только article и обрабатывать его содержимое

После получения и очистки контент сохраняется в файл с именем страницы (если сылка вида 
https://lenta.ru/articles/2016/05/20/loan - то контент сохраняется в файл loan.txt рядом
со скриптом) 

Внизу указаны проверочные страницы
"""

class ParseMyClass:
	def __init__(self,url):
		self.url=url
		self.file = self.url.split('/')[-1]
		site = urllib.request.urlopen(self.url)
		html = str(site.read().decode('utf-8'))
		self.article = re.findall(r'<article[^>]*>(.*?)</article>', str(html), re.DOTALL)
		if len(self.article)==0:
			self.article = re.findall(r'<div.*itemtype="http://schema.org/NewsArticle[^>]+?>(.*)</div>', str(html) , re.DOTALL)
		self.razbor()
		self.save()
		
	def razbor(self):
		article = self.article

		#меняем ссылки
		article = re.sub(r'<[aA]\s{1}href=[\'\"](.*?)[\'\"][^>]*>(.*?)</[aA]>', r'[URL="\1"] \2 [/URL]', str(article))

#		#Тут надо будет подумать, как получше это сделать		
#		#выбираем фотки
#		article = re.sub(r'<img(.*?)alt=[\'\"](.*?)[\'\"](.*?)src=[\'\"](.*?)[\'\"](.*?)>', r'[IMG="\4"]\2[/IMG]', str(article))
		
		#удаляем различные теги для чистоты
		article = re.sub(r'<(section|script|aside|time).*?</\1>(?s)', '', str(article))
		article = re.sub(r'<div class="bordered-title">(.*)</div>', '', str(article))
		
		#удаляем лишние пробелы
		article = re.sub(r'\s+',' ', str(article))
		
		#удаляем табуляцию
		article = re.sub(r'\t', r'\s', str(article))
		
		#выделяем заголовки
		article = re.sub(r'<[hH][^>]*>(.*?)</[hH][^>]*>', r'\1\r\n', str(article))
		
		# выделяем абзацы
		article = re.sub(r'<[pP][^>]*>(.*?)</[pP][^>]*>', r'\1\r\n', str(article))
		
		# удаляем все оставльные теги
		article = re.sub(r'<.*?>','', str(article))
		
		# Выравниваем по 80 символов
		article.strip()
		list = article.split('\r\n')
		i=0
		j=79
		while i<len(list):
			if len(list[i])>j:
				shag=1
				k=j*shag
				nachalo_stroki=0
				while 0<k<=len(list[i]):
					print(str(k)+"   sdf   "+str(len(list[i])))
					if ord(list[i][k])!=32:
						while  list[i][k] is not None and list[i][k]!=' ' and list[i][k]!='\n' and k>nachalo_stroki:
							k=k-1
					if k==nachalo_stroki:
						list[i]=list[i][:j+nachalo_stroki]+'\n'+list[i][j+nachalo_stroki:]
					else:
						list[i]=list[i][:k]+'\n'+list[i][k+1:]
					k=(j*shag)-k
					shag=shag+1
					k=(j*shag)-k
					nachalo_stroki=k-j
			i=i+1
		article = str('\r\n'.join(list))
		self.article = article
		
	def save(self):
		fname=self.file+'.txt'
		f = open(fname, 'w')
		f.write(str(self.article))
		f.close()

if len (sys.argv) > 1:
	parse = ParseMyClass(sys.argv[1])
else:
	url = input('Введите URL статьи в виде "https://lenta.ru/articles/..."')
	if url is not None and len(url.strip())>0:
		parse = ParseMyClass(url)
		
#parse = ParseMyClass('https://lenta.ru/articles/2016/05/20/loan')		
#parse = ParseMyClass('https://lenta.ru/articles/2016/05/20/nogotkov')	
#parse = ParseMyClass('https://lenta.ru/articles/2016/05/20/platinum')	
#parse = ParseMyClass('https://lenta.ru/articles/2016/05/21/dnepr')	
#parse = ParseMyClass('https://lenta.ru/articles/2016/05/21/scaryipoteka/')	
#parse = ParseMyClass('https://lenta.ru/articles/2016/05/18/minigun')
#parse = ParseMyClass('https://lenta.ru/news/2016/05/21/fireinthesky')
#parse = ParseMyClass('https://lenta.ru/news/2016/05/21/ducks')
