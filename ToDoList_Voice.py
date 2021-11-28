# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 20:10:41 2021

@author: User
"""

import datetime
import time
import calendar
from colorama import init, Fore  #文字顏色套件

#google語音
from gtts import gTTS
from playsound import playsound
import os
import time

#speak to text
import speech_recognition

import pyaudio

def speech(text):
    file_name = str(int(time.time()))                
    speech = gTTS(text = text, lang = language, slow = False)
    speech.save(file_name + '.mp3')
    playsound(file_name + '.mp3')

#在日曆上標示日期
def markTheDay(day, cal, color):
    cal_f = cal[:cal.find(str(day))]
    cal = cal[cal.find(str(day))+len(str(day)):]
    init(autoreset=True)
    print(cal_f + color + str(day) + Fore.RESET, end = '')
    return cal

def Voice_To_Text():
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source: 
     ## 介紹一下 with XXX as XX 這個指令
     ## XXX 是一個函數或動作 然後我們把他的output放在 XX 裡
     ## with 是在設定一個範圍 讓本來的 source 不會一直進行
     ## 簡單的應用可以參考
     ## https://blog.gtwang.org/programming/python-with-context-manager-tutorial/
        print("請開始說話:")                               # print 一個提示 提醒你可以講話了
        r.adjust_for_ambient_noise(source)     # 函數調整麥克風的噪音:
        audio = r.listen(source)
     ## with 的功能結束 source 會不見 
     ## 接下來我們只會用到 audio 的結果
    try:
        Text = r.recognize_google(audio, language="zh-TW")     
              ## 將剛說的話轉成 zh-TW 繁體中文的字串
              ## recognize_google 指得是使用google的api 
              ## 也就是用google 網站看到的語音辨識啦~~
              ## 雖然有其他選擇 
    except speech_recognition.UnknownValueError:
        Text = "無法翻譯"
    except speech_recognition.RequestError as e:
        Text = "無法翻譯{0}".format(e)
              # 兩個 except 是當語音辨識不出來的時候 防呆用的 
    print(Text)          
    return Text

#情感
import re
with open('D:/NUK/AI語意/期中專題/ntusd-negative.txt', mode='r', encoding='utf-8') as f:
    negs = f.readlines()
with open('D:/NUK/AI語意/期中專題/ntusd-positive.txt', mode='r', encoding='utf-8') as f:
    poss = f.readlines()

language = 'zh'

#Intro
print("歡迎回家!")
print("今天過得如何呀?")
#s = input()
speech("歡迎回家!")
speech("今天過得如何呀?")
s = Voice_To_Text()
neg = [] #負面詞句List
pos = []
x = 0
isNotNeg = True
for i in negs:
    a=re.findall(r'\w+',i) 
    neg.extend(a)
for i in poss:
    a=re.findall(r'\w+',i) 
    pos.extend(a)
    

for i in range(len(neg)):
    if neg[i] in s.strip():
        print('秀秀~讓我幫你分攤一些工作吧!')
        speech('秀秀 讓我幫你分攤一些工作吧!')
        isNotNeg = False
        break

if(isNotNeg):
    for i in range(len(pos)):
        if pos[i] in s.strip():
            print('恭喜~真是開心的一天!那讓我幫你分攤一些工作吧!讓你天天開心!')
            speech('恭喜 真是開心的一天!那讓我幫你分攤一些工作吧!讓你天天開心!')
            break

#待辦事項
TODO_list = []	#存取待辦事項，格式:[名稱, [年, 月, 日], 相距天數，幾天前提醒,提醒日日期]
#讀取txt
path = 'ToDoList.txt'
f = open(path, 'a+')
list_history = f.readlines()
list_data = []
'''
for i in list_history:
    a=re.findall(r'\w+',i) 
    list_data.extend(a)
'''
for line in list_history:
    year_todo = line[:line.find('/')]
    month_todo = line[line.find('/')+1:line.find('/',line.find('/')+1)]
    day_todo = line[line.find('/',line.find('/')+1)+1:line.find(' ')]
    TODO_name = line[line.find(' ')+1:line.find(':')]
    
    TODO_date=[int(year_todo),int(month_todo),int(day_todo)]
    #計算相差天數
    time_dis =datetime.date(TODO_date[0], TODO_date[1], TODO_date[2]) - datetime.date.today()
    
    TODO_hint_date = line[line.find(' ',line.find(' ')+1)+1:line.find('\n')]
    TODO_hint_date = datetime.date.fromisoformat(TODO_hint_date)
    
    TODO_hint = TODO_hint_date - datetime.date.today()
    
    TODO_list.append([TODO_name, TODO_date, time_dis.days, TODO_hint.days, TODO_hint_date])
    
#擷取日期和事項

date = datetime.date.today()	#取得今天日期
date_str = str(date)	#傳換成字串
#取出年月日
year = int(date_str[:date_str.find("-")])
month = int(date_str[date_str.find("-")+1:date_str.find("-",date_str.find("-")+1)])
day = int(date_str[date_str.find("-",date_str.find("-")+1)+1:])  #先轉int將0消掉


while True:
    
    print("有甚麼待辦事項需要我幫你紀錄的嗎?")
    speech("有甚麼待辦事項需要我幫你紀錄的嗎?")
    #s=input()
    s = Voice_To_Text()
    if '沒' in s:
        break
    if '年' in s:
        year_todo = s[s.find('年')-4:s.find('年')]
    else:
        year_todo = datetime.date.today().year
        
    if '月' in s:
        if(s.find('月') > 1):
            month_todo = s[s.find('月')-2:s.find('月')]
            if not (month_todo[0] in ['1','2','3','4','5','6','7','8','9']) :
                month_todo = month_todo[-1]
        else:
            month_todo = s[s.find('月')-1:s.find('月')]
    else:
        month_todo = datetime.date.today().month
    if '日' in s:
        if s.find('日')>1:
            day_todo = s[s.find('日')-2:s.find('日')]
            if not (day_todo[0] in ['1','2','3','4','5','6','7','8','9']) :
                day_todo = day_todo[-1]
        else:
            day_todo = s[s.find('日')-1:s.find('日')]
    elif '號' in s:
        if s.find('號'):
            day_todo = s[s.find('號')-2:s.find('號')]
            if not (day_todo[0] in ['1','2','3','4','5','6','7','8','9']) :
                day_todo = day_todo[-1]
        else:
            day_todo = s[s.find('號')-1:s.find('號')]
    else:
        
        print("不好意思我聽不懂，麻煩你再說一次")
        speech("不好意思我聽不懂，麻煩你再說一次")
        continue
    if '要' in s:
        TODO_name = s[s.find('要')+1:]
    else:
        
        print("不好意思我聽不懂，麻煩你再說一次")
        speech("不好意思我聽不懂，麻煩你再說一次")
    TODO_date=[int(year_todo),int(month_todo),int(day_todo)]
    #計算相差天數
    time_dis = datetime.date(TODO_date[0], TODO_date[1], TODO_date[2]) - datetime.date.today()
    #TODO_hint = int(input("請問要在幾天前提醒您呢?"))
    print('請問要在幾天前提醒您呢?')
    speech('請問要在幾天前提醒您呢?')
    unknow = True;
    while(unknow):
        s = Voice_To_Text()
        if '天' in s:
            if s[:s.find('天')] == "兩":
                TODO_hint = 2
            else:
                TODO_hint = int(s[:s.find('天')])
            unknow = False
        else:
            print("不好意思我聽不懂，麻煩你再說一次")
            speech("不好意思我聽不懂，麻煩你再說一次")
    # 算出提醒日的日期
    TODO_hint_date = datetime.date(TODO_date[0], TODO_date[1], TODO_date[2]) - datetime.timedelta(days=TODO_hint)
    TODO_list.append([TODO_name, TODO_date, time_dis.days, TODO_hint, TODO_hint_date])

TODO_list.append(['Today', [year, month, day], 0,-1,-1])
#依照日期排序
TODO_list.sort(key = lambda TODO_list:[TODO_list[1][2]])
TODO_list.sort(key = lambda TODO_list:[TODO_list[1][1]])
TODO_list.sort(key = lambda TODO_list:[TODO_list[1][0]])

cal = calendar.month(year, month)
# 標示日期會標到年分故先輸出月曆到Sunday 
cal_f = cal[:cal.find('Su')]
# 存取尚未輸出的部分
cal = cal[cal.find(str('Su')):]
print(cal_f, end = '')

# 將當月的待辦事項日期用紅色標示，當天則用黃色
for i in range(len(TODO_list)):
    if TODO_list[i][1][0] == year:
        if TODO_list[i][1][1] == month:
            if TODO_list[i][0] == 'Today':
                cal = markTheDay(TODO_list[i][1][2], cal, Fore.GREEN)
            else:
                cal = markTheDay(TODO_list[i][1][2], cal, Fore.RED)
        elif TODO_list[i][1][1] > month:
            break
    elif TODO_list[i][1][0] > year:
        break
print(cal)
f.close()
f = open(path, 'w')
# 輸出待辦清單
for i in range(len(TODO_list)):
    if TODO_list[i][2] != 0:
        print(str(TODO_list[i][1][0]) + '/' + 
              str(TODO_list[i][1][1]) + '/' + 
              str(TODO_list[i][1][2]) + ' ' +
              TODO_list[i][0], end = '', file=f)
    print(str(TODO_list[i][1][0]) + '/' +
		  str(TODO_list[i][1][1]) + '/' + 
		  str(TODO_list[i][1][2]) + ' ' +
		  TODO_list[i][0], end = '')
        
    if(TODO_list[i][2] < 0):
        print(':' + str(abs(TODO_list[i][2])) + '天前', end = '', file=f)
        print(':' + str(abs(TODO_list[i][2])) + '天前')
        print(' '+str(TODO_hint_date), file=f)
    elif(TODO_list[i][2] > 0):
        print(':' + str(abs(TODO_list[i][2])) + '天後', end = '', file=f)
        print(':' + str(abs(TODO_list[i][2])) + '天後')
        print(' '+str(TODO_hint_date), file=f)
    elif(TODO_list[i][2] == 0):
        print('')
    
print('')

#輸出到txt
f.close()
# 提醒功能
for i in range(len(TODO_list)):
  if(TODO_list[i][4]==datetime.date.today()):
	  text = "提醒您，"+str(TODO_list[i][2])+"天後要"+str(TODO_list[i][0])
	  print(text)
	  speech(text)

print('')
        
print("待辦事項已經幫您紀錄完畢囉~")
#print("如果忘記可以再回來確認喔")
print("下次見~")        
speech("待辦事項已經幫您紀錄完畢囉")
#speech("如果忘記可以再回來確認喔")
speech("下次見")  

