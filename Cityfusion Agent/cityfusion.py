#!/usr/bin/env python
# -*- coding:utf-8 -*-
import win32api
import pika
import xlrd
import win32con
import win32gui
from ctypes import *
import time
import os
import SendKeys

# read applnk from lnk.xls file


xlsfilePath = os.getcwd() + '\lnk.xls'
print xlsfilePath

book = xlrd.open_workbook(xlsfilePath)
sheet0 = book.sheet_by_index(0)

timedaly = str(sheet0.cell_value(0, 3))
print "time sleep:"+ timedaly + " s"
time.sleep(float(timedaly))
mqhost = str(sheet0.cell_value(0, 1))
print mqhost
print 'waiting mqhost ...'

#connection = pika.BlockingConnection( pika.ConnectionParameters(host = mqhost,heartbeat_interval=0) )
#channel = connection.channel()

username = 'guest'
pwd = 'guest'
user_pwd = pika.PlainCredentials(username, pwd)
s_conn = pika.BlockingConnection(pika.ConnectionParameters(mqhost, credentials=user_pwd))
channel = s_conn.channel()

# print connection
#channel.exchange_declare(exchange='messages', type='fanout')
#result = channel.queue_declare(exclusive=True)
#print result
#queue_name = result.method.queue
#channel.queue_bind(exchange='messages', queue=queue_name)

channel.exchange_declare(exchange='messages_exchange',type='direct')

result = channel.queue_declare(exclusive=False)
queue_name = result.method.queue
#queue_name = 'messages_queue'
severities = 'messages_key'

channel.queue_bind(exchange='messages_exchange',
                       queue=queue_name,
                       routing_key=severities)

print 'mqhost connected, you can input command..'

#==================================================
def mouse_click(x=None,y=None):
    if not x is None and not y is None:
        windll.user32.SetCursorPos(x, y)
        time.sleep(0.15)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.15)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

#def key_input(key_hex=None):
    #print "input:"+int(key_hex)
    #win32api.keybd_event(key_hex,0,0,0)
    #win32api.keybd_event(key_hex,0,win32con.KEYEVENTF_KEYUP,0)
    #time.sleep(0.01)

#==================================================

#win32api.ShellExecute(0,'open','C:\Users\Bingo\Desktop\sss.avi','','',1)
#time.sleep(3)
#appName = u"sss.avi"
#appName = str(sheet0.cell_value(1,1));
#print appName
#hwnd= win32gui.FindWindow(None, appName)
#print hwnd

#win32gui.PostMessage(hwnd,win32con.WM_SYSCOMMAND,win32con.SC_MAXIMIZE,0)
#time.sleep(3)
#win32gui.SetForegroundWindow(hwnd)
#time.sleep(3)
#win32gui.PostMessage(hwnd,win32con.WM_CLOSE,0,0)

def callback(ch, method, properties, body):

    print body
    try:
        for i in range(sheet0.nrows):
            if body == str(sheet0.cell_value(i+1,0)):
                if sheet0.cell_value(i+1,2) == 0:
                    print sheet0.cell_value(i+1,1)
                    win32api.ShellExecute(0,'open',sheet0.cell_value(i+1,1),'','',3)
                    break

                elif sheet0.cell_value(i+1,2) == 1:
                    Pxy = str(sheet0.cell_value(i+1,1)).strip('[').strip(']').split(',')
                    print "mouse_click:" + str(sheet0.cell_value(i+1,1))
                    mouse_click(int(Pxy[0]),int(Pxy[1]))
                    break

                elif sheet0.cell_value(i+1,2) == 2:
                    key_value = str(sheet0.cell_value(i+1,1))
                    print "key_click:" + key_value
                    #win32api.keybd_event(key_hex,0,0,0)
                    SendKeys.SendKeys(key_value)

                    #key_input(int(sheet0.cell_value(i+1,1)),int(sheet0.cell_value(i+1,1)))
                    #key_input(0xF7)
                    break

                elif sheet0.cell_value(i+1,2) == 3:
                    print "Max windows:" + str(sheet0.cell_value(i+1,1))
                    #appName = u"233.txt - 记事本"
                    appName = str(sheet0.cell_value(i+1,1));
                    hwnd= win32gui.FindWindow(None, appName)
                    print hwnd
                    #win32gui.PostMessage(hwnd,win32con.WM_SYSCOMMAND,win32con.SC_MAXIMIZE,0)
                    win32gui.SetForegroundWindow(hwnd)
                    break

                elif sheet0.cell_value(i+1,2) == 4:
                    print "Min windows:" + str(sheet0.cell_value(i+1,1))
                    appName = str(sheet0.cell_value(i+1,1));
                    hwnd= win32gui.FindWindow(None, appName)
                    print hwnd
                    win32gui.PostMessage(hwnd,win32con.WM_SYSCOMMAND, win32con.SC_MINIMIZE, 0)
                    break

                elif sheet0.cell_value(i+1,2) == 5:
                    print "Close windows:" + str(sheet0.cell_value(i+1,1))
                    appName = str(sheet0.cell_value(i+1,1));
                    hwnd= win32gui.FindWindow(None, appName)
                    print hwnd
                    win32gui.PostMessage(hwnd,win32con.WM_CLOSE,0,0)
                    break
            else:
                continue
    except:
            print "Error:Command does not exist "
channel.basic_consume(callback, queue=queue_name, no_ack=True)
channel.start_consuming()
