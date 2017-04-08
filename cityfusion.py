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



xlsfilePath = os.getcwd() + '\lnk.xls'
print xlsfilePath

book = xlrd.open_workbook(xlsfilePath)
sheet0 = book.sheet_by_index(0)
mqhost = str(sheet0.cell_value(0, 1))

print mqhost
print 'waiting mqhost ...'
connection = pika.BlockingConnection( pika.ConnectionParameters(host = mqhost,heartbeat_interval=0) )
channel = connection.channel()

channel.exchange_declare(exchange='messages', type='fanout')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='messages', queue=queue_name)
print 'waiting command ...'

#==================================================
def mouse_click(x=None,y=None):
    if not x is None and not y is None:
        windll.user32.SetCursorPos(x, y)
        time.sleep(0.15)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.15)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
#==================================================

def callback(ch, method, properties, body):
    try:
        for i in range(sheet0.nrows):
            if body == str(sheet0.cell_value(i+1,0)):
                if sheet0.cell_value(i+1,2) == 0:
                    print sheet0.cell_value(i+1,1)
                    win32api.ShellExecute(0,'open',sheet0.cell_value(i+1,1),'','',1)
                    break

                elif sheet0.cell_value(i+1,2) == 1:
                    Pxy = str(sheet0.cell_value(i+1,1)).strip('[').strip(']').split(',')
                    print "mouse_click:" + str(sheet0.cell_value(i+1,1))
                    mouse_click(int(Pxy[0]),int(Pxy[1]))
                    break
            else:
                continue
    except:
            print "Error:Command does not exist "
channel.basic_consume(callback, queue=queue_name, no_ack=True)
channel.start_consuming()
