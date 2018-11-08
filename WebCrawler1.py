# web_parser.py
import requests
from bs4 import BeautifulSoup
import os

import telegram

bot = telegram.Bot(token='679726235:AAE5ETXt6t4-qa1HvyFg6_fydffdJEuPahw')
chat_id = 458661470

# 파일의 위치
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

req = requests.get('http://www.mss.go.kr/site/gyeonggi/ex/bbs/List.do?cbIdx=247')
req.encoding = 'utf-8'

html = req.text
soup = BeautifulSoup(html, 'html.parser')
titles_temp = soup.select('td.alignLeft > a')

titles = []
check_line_count = 5
i = 0
while i < check_line_count:
	str1 = titles_temp[i].text.replace('\t','')
	str2 = str1.replace('\r\n','')
	titles.append(str2)
	i = i+1

with open(os.path.join(BASE_DIR, 'latest.txt'), 'r+') as f_read:
	i = 0
	diff = False
	while i < check_line_count:
		str1 = f_read.readline()
		str2 = str1.replace('\t','')
		before = str2.replace('\r\n','')
		if before != titles[i]:
			diff = True
			break
		i = i+1
		
	if(diff):
		text='새로운 글 있음\n'
		for title in titles:
			text = text + title;
		text = text + "http://www.mss.go.kr/site/gyeonggi/ex/bbs/List.do?cbIdx=247"
		bot.sendMessage(chat_id=chat_id, text=text)
		
	else:
		bot.sendMessage(chat_id=chat_id, text='변경없음')
	f_read.close()

with open(os.path.join(BASE_DIR, 'latest.txt'), 'w+') as f_write:
	for title in titles:
		f_write.write(title)
	f_write.close()