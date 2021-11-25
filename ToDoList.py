import datetime
import time
import calendar
from colorama import init, Fore  #文字顏色套件

#google語音
from gtts import gTTS
from playsound import playsound
import os
import time

#在日曆上標示日期
def markTheDay(day, cal, color):
    cal_f = cal[:cal.find(str(day))]
    cal = cal[cal.find(str(day))+len(str(day)):]
    init(autoreset=True)
    print(cal_f + color + str(day) + Fore.RESET, end = '')
    return cal

date = datetime.date.today()	#取得今天日期
date_str = str(date)	#傳換成字串
#取出年月日
year = int(date_str[:date_str.find("-")])
month = int(date_str[date_str.find("-")+1:date_str.find("-",date_str.find("-")+1)])
day = int(date_str[date_str.find("-",date_str.find("-")+1)+1:])  #先轉int將0消掉
#待辦事項
TODO_list = []	#存取待辦事項，格式:[名稱, [年, 月, 日], 相距天數，幾天前提醒]

while True:
	TODO_name = input("請輸入待辦事項名稱(輸入q結束輸入):")
	if(TODO_name == 'q'):
		break
	TODO_date = input("請輸入待辦事項西元年/月/日:")
	#處理輸入的日期(拆分並轉型)
	TODO_date = [int(TODO_date[:TODO_date.find('/')]), 
	             int(TODO_date[TODO_date.find('/')+1:TODO_date.find('/',TODO_date.find('/')+1)]), 
	             int(TODO_date[TODO_date.find('/',TODO_date.find('/')+1)+1:])]
	#計算相差天數(datetime.date 
	time_dis =datetime.date(TODO_date[0], TODO_date[1], TODO_date[2]) - datetime.date.today()
	TODO_hint = int(input("請輸入在幾天前提醒:"))
	TODO_list.append([TODO_name, TODO_date, time_dis.days, TODO_hint])

TODO_list.append(['Today', [year, month, day], 0,-1])
#依照日期排序
TODO_list.sort(key = lambda TODO_list:[TODO_list[1][2]])
TODO_list.sort(key = lambda TODO_list:[TODO_list[1][1]])
TODO_list.sort(key = lambda TODO_list:[TODO_list[1][0]])

cal = calendar.month(year, month)
# 標示日期會標到年分故先輸出月曆到Sunday
cal_f = cal[:cal.find('Su')]
# 存取尚未輸出的部分
cal = cal[cal.find(str('Su'))+len(str('Su')):]
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

# 輸出待辦清單
for i in range(len(TODO_list)):
	print(str(TODO_list[i][1][0]) + '/' +
		  str(TODO_list[i][1][1]) + '/' + 
		  str(TODO_list[i][1][2]) + ' ' +
		  TODO_list[i][0], end = '')
	if(TODO_list[i][2] < 0):
		print(':' + str(abs(TODO_list[i][2])) + '天前')
	elif(TODO_list[i][2] > 0):
		print(':' + str(abs(TODO_list[i][2])) + '天後')
	elif(TODO_list[i][2] == 0):
		print('')
  
# 提醒功能
for i in range(len(TODO_list)):
  if(TODO_list[i][2]==TODO_list[i][3]):
	  file_name = str(int(time.time()))                
	  file_path = file_name + '.mp3'
	  text = "提醒您，在"+str(TODO_list[i][2])+"天後要"+str(TODO_list[i][0])
	  language = 'zh'

	  speech = gTTS(text = text, lang = language, slow = False)

	  speech.save(file_name + '.mp3')

	  playsound(file_name + '.mp3')
