#!/usr/bin/python
# -*- coding: UTF-8 -*-
# File name   : client.py
# Description : client  
# Website     : www.adeept.com
# E-mail      : support@adeept.com
# Author      : William
# Date        : 2018/08/22
from socket import *
import time
import threading as thread
import tkinter as tk


stat=0          #A status value,ensure the mainloop() runs only once
tcpClicSock=''  #A global variable,for future socket connection
BUFSIZ=1024     #Set a buffer size
ip_stu=1        #Shows connection status

#Global variables of input status
BtnIP=''
ipaddr=''
ipcon=0
send_pwm_conf = 1

def replace_num(initial,new_num):   #Call this function to replace data in '.txt' file
    newline=""
    str_num=str(new_num)
    with open("ip.txt","r") as f:
        for line in f.readlines():
            if(line.find(initial) == 0):
                line = initial+"%s" %(str_num)
            newline += line
    with open("ip.txt","w") as f:
        f.writelines(newline)    #Call this function to replace data in '.txt' file

def num_import(initial):            #Call this function to import data from '.txt' file
    with open("ip.txt") as f:
        for line in f.readlines():
            if(line.find(initial) == 0):
                r=line
    begin=len(list(initial))
    snum=r[begin:]
    n=snum
    return n    

def call_forward(event):         #When this function is called,client commands the car to move forward
    tcpClicSock.send(('add').encode())

def call_back(event):            #When this function is called,client commands the car to move backward
    tcpClicSock.send(('sub').encode())

def normal_state():
    Btn_L0.config(fg=color_text,bg=color_btn)
    Btn_L1.config(fg=color_text,bg=color_btn)
    Btn_L2.config(fg=color_text,bg=color_btn)
    Btn_L3.config(fg=color_text,bg=color_btn)
    Btn_L4.config(fg=color_text,bg=color_btn)
    Btn_L5.config(fg=color_text,bg=color_btn)
    Btn_L6.config(fg=color_text,bg=color_btn)
    Btn_L7.config(fg=color_text,bg=color_btn)
    Btn_L8.config(fg=color_text,bg=color_btn)
    Btn_L9.config(fg=color_text,bg=color_btn)
    Btn_L10.config(fg=color_text,bg=color_btn)
    Btn_L11.config(fg=color_text,bg=color_btn)
    Btn_L12.config(fg=color_text,bg=color_btn)
    Btn_L13.config(fg=color_text,bg=color_btn)
    Btn_L14.config(fg=color_text,bg=color_btn)
    Btn_L15.config(fg=color_text,bg=color_btn)



def set_L0():
    print('L0')
    tcpClicSock.send(('L0').encode())
    normal_state()
    Btn_L0.config(fg='#0277BD',bg='#BBDEFB')

def set_L1():
    print('L1')
    tcpClicSock.send(('L1').encode())
    normal_state()
    Btn_L1.config(fg='#0277BD',bg='#BBDEFB')

def set_L2():
    tcpClicSock.send(('L2').encode())
    normal_state()
    Btn_L2.config(fg='#0277BD',bg='#BBDEFB')

def set_L3():
    tcpClicSock.send(('L3').encode())
    normal_state()
    Btn_L3.config(fg='#0277BD',bg='#BBDEFB')

def set_L4():
    tcpClicSock.send(('L4').encode())
    normal_state()
    Btn_L4.config(fg='#0277BD',bg='#BBDEFB')

def set_L5():
    tcpClicSock.send(('L5').encode())
    normal_state()
    Btn_L5.config(fg='#0277BD',bg='#BBDEFB')

def set_L6():
    tcpClicSock.send(('L6').encode())
    normal_state()
    Btn_L6.config(fg='#0277BD',bg='#BBDEFB')

def set_L7():
    tcpClicSock.send(('L7').encode())
    normal_state()
    Btn_L7.config(fg='#0277BD',bg='#BBDEFB')

def set_L8():
    tcpClicSock.send(('L8').encode())
    normal_state()
    Btn_L8.config(fg='#0277BD',bg='#BBDEFB')

def set_L9():
    tcpClicSock.send(('L9').encode())
    normal_state()
    Btn_L9.config(fg='#0277BD',bg='#BBDEFB')

def set_L10():
    tcpClicSock.send(('L10').encode())
    normal_state()
    Btn_L10.config(fg='#0277BD',bg='#BBDEFB')

def set_L11():
    tcpClicSock.send(('L11').encode())
    normal_state()
    Btn_L11.config(fg='#0277BD',bg='#BBDEFB')

def set_L12():
    tcpClicSock.send(('L12').encode())
    normal_state()
    Btn_L12.config(fg='#0277BD',bg='#BBDEFB')

def set_L13():
    tcpClicSock.send(('L13').encode())
    normal_state()
    Btn_L13.config(fg='#0277BD',bg='#BBDEFB')

def set_L14():
    tcpClicSock.send(('L14').encode())
    normal_state()
    Btn_L14.config(fg='#0277BD',bg='#BBDEFB')

def set_L15():
    tcpClicSock.send(('L15').encode())
    normal_state()
    Btn_L15.config(fg='#0277BD',bg='#BBDEFB')



def normal_st():
    Btn_ST1.config(fg=color_text,bg=color_btn)
    Btn_ST2.config(fg=color_text,bg=color_btn)
    Btn_ST3.config(fg=color_text,bg=color_btn)
    Btn_ST4.config(fg=color_text,bg=color_btn)
    Btn_ST5.config(fg=color_text,bg=color_btn)
    Btn_ST6.config(fg=color_text,bg=color_btn)
    Btn_ST7.config(fg=color_text,bg=color_btn)
    Btn_ST8.config(fg=color_text,bg=color_btn)
    Btn_ST9.config(fg=color_text,bg=color_btn)
    Btn_ST10.config(fg=color_text,bg=color_btn)
    Btn_ST11.config(fg=color_text,bg=color_btn)
    Btn_ST12.config(fg=color_text,bg=color_btn)
    Btn_ST13.config(fg=color_text,bg=color_btn)
    Btn_ST14.config(fg=color_text,bg=color_btn)
    Btn_MAX.config(fg=color_text,bg=color_btn)
    Btn_MIN.config(fg=color_text,bg=color_btn)



def set_ST1():
    tcpClicSock.send(('ST1').encode())
    normal_st()
    Btn_ST1.config(fg='#0277BD',bg='#BBDEFB')

def set_ST2():
    tcpClicSock.send(('ST2').encode())
    normal_st()
    Btn_ST2.config(fg='#0277BD',bg='#BBDEFB')

def set_ST3():
    tcpClicSock.send(('ST3').encode())
    normal_st()
    Btn_ST3.config(fg='#0277BD',bg='#BBDEFB')

def set_ST4():
    tcpClicSock.send(('ST4').encode())
    normal_st()
    Btn_ST4.config(fg='#0277BD',bg='#BBDEFB')

def set_ST5():
    tcpClicSock.send(('ST5').encode())
    normal_st()
    Btn_ST5.config(fg='#0277BD',bg='#BBDEFB')

def set_ST6():
    tcpClicSock.send(('ST6').encode())
    normal_st()
    Btn_ST6.config(fg='#0277BD',bg='#BBDEFB')

def set_ST7():
    tcpClicSock.send(('ST7').encode())
    normal_st()
    Btn_ST7.config(fg='#0277BD',bg='#BBDEFB')

def set_ST8():
    tcpClicSock.send(('ST8').encode())
    normal_st()
    Btn_ST8.config(fg='#0277BD',bg='#BBDEFB')

def set_ST9():
    tcpClicSock.send(('ST9').encode())
    normal_st()
    Btn_ST9.config(fg='#0277BD',bg='#BBDEFB')

def set_ST10():
    tcpClicSock.send(('ST10').encode())
    normal_st()
    Btn_ST10.config(fg='#0277BD',bg='#BBDEFB')

def set_ST11():
    tcpClicSock.send(('ST11').encode())
    normal_st()
    Btn_ST10.config(fg='#0277BD',bg='#BBDEFB')

def set_ST12():
    tcpClicSock.send(('ST12').encode())
    normal_st()
    Btn_ST10.config(fg='#0277BD',bg='#BBDEFB')

def set_ST13():
    tcpClicSock.send(('ST13').encode())
    normal_st()
    Btn_ST10.config(fg='#0277BD',bg='#BBDEFB')

def set_ST14():
    tcpClicSock.send(('ST14').encode())
    normal_st()
    Btn_ST10.config(fg='#0277BD',bg='#BBDEFB')

def set_MIN():
    tcpClicSock.send(('MIN').encode())
    normal_st()
    Btn_ST2.config(fg='#0277BD',bg='#BBDEFB')

def set_MAX():
    tcpClicSock.send(('MAX').encode())
    normal_st()
    Btn_ST2.config(fg='#0277BD',bg='#BBDEFB')

def set_config():
    tcpClicSock.send(('config').encode())

def set_reset():
    tcpClicSock.send(('reset').encode())

def set_save():
    tcpClicSock.send(('save').encode())

def set_run():
    setp_send = var_setps.get()
    time_send = var_time.get()
    tcpClicSock.send(('run %s %s'%(setp_send,time_send)).encode())

def set_stop():
    tcpClicSock.send(('stop').encode())

def set_all():
    setp_send = var_setps.get()
    time_send = var_time.get()
    tcpClicSock.send(('all %s %s'%(setp_send,time_send)).encode())

def set_stepall():
    tcpClicSock.send(('frame').encode())

def set_pwm_thread():
    global send_pwm_conf
    while 1:
        if send_pwm_conf == 0:
            time.sleep(0.3)
            tcpClicSock.send((var_pwm.get()).encode())
            send_pwm_conf = 1
        time.sleep(0.2)
            


def set_pwm(event):
    global send_pwm_conf
    if send_pwm_conf == 1:
        #tcpClicSock.send((var_pwm.get()).encode())
        send_pwm_conf = 0

def loop():                       #GUI
    global tcpClicSock,BtnIP,led_status,color_text,color_btn,Btn_L0,Btn_L1,Btn_L2,Btn_L3,Btn_L4,Btn_L5,Btn_L6,Btn_L7,Btn_L8,Btn_L9,Btn_L10,Btn_L11,Btn_L12,Btn_L13,Btn_L14,Btn_L15,Btn_ST1, Btn_ST2,Btn_ST3,Btn_ST4,Btn_ST5,Btn_ST6,Btn_ST7,Btn_ST8,Btn_ST9,Btn_ST10,Btn_ST11,Btn_ST12,Btn_ST13,Btn_ST14,Btn_MIN,Btn_MAX,var_setps,var_time,var_pwm     #The value of tcpClicSock changes in the function loop(),would also changes in global so the other functions could use it.
    while True:
        color_bg='#000000'        #Set background color
        color_text='#E1F5FE'      #Set text color
        color_btn='#0277BD'       #Set button color
        color_line='#01579B'      #Set line color
        color_can='#212121'       #Set canvas color
        color_oval='#2196F3'      #Set oval color
        target_color='#FF6D00'

        root = tk.Tk()            #Define a window named root
        root.title('Adeept')      #Main window title
        root.geometry('800x630')  #Main window size, middle of the English letter x.
        root.config(bg=color_bg)  #Set the background color of root window
    
        var_pwm = tk.StringVar()  #Speed value saved in a StringVar
        var_pwm.set(425)            #Set a default speed,but change it would not change the default speed value in the car,you need to click button'Set' to send the value to the car

        var_setps = tk.StringVar()
        var_setps.set(5)

        var_time = tk.StringVar()
        var_time.set(0.2)

        logo =tk.PhotoImage(file = 'logo.png')         #Define the picture of logo,but only supports '.png' and '.gif'
        l_logo=tk.Label(root,image = logo,bg=color_bg) #Set a label to show the logo picture
        l_logo.place(x=30,y=13)                        #Place the Label in a right position

        def connect(event):       #Call this function to connect with the server
            if ip_stu == 1:
                sc=thread.Thread(target=socket_connect) #Define a thread for connection
                sc.setDaemon(True)                      #'True' means it is a front thread,it would close when the mainloop() closes
                sc.start()                              #Thread starts

        def connect_2():          #Call this function to connect with the server
            if ip_stu == 1:
                sc=thread.Thread(target=socket_connect) #Define a thread for connection
                sc.setDaemon(True)                      #'True' means it is a front thread,it would close when the mainloop() closes
                sc.start()                              #Thread starts

        def socket_connect():     #Call this function to connect with the server
            global ADDR,tcpClicSock,BUFSIZ,ip_stu,ipaddr
            ip_adr=E1.get()       #Get the IP address from Entry

            if ip_adr == '':      #If no input IP address in Entry,import a default IP
                ip_adr=num_import('IP:')
                l_ip_4.config(text='Connecting')
                l_ip_4.config(bg='#FF8F00')
                l_ip_5.config(text='Default:%s'%ip_adr)
                pass
            
            SERVER_IP = ip_adr
            SERVER_PORT = 10223   #Define port serial 
            BUFSIZ = 1024         #Define buffer size
            ADDR = (SERVER_IP, SERVER_PORT)
            tcpClicSock = socket(AF_INET, SOCK_STREAM) #Set connection value for socket

            for i in range (1,6): #Try 5 times if disconnected
                try:
                    if ip_stu == 1:
                        print("Connecting to server @ %s:%d..." %(SERVER_IP, SERVER_PORT))
                        print("Connecting")
                        tcpClicSock.connect(ADDR)        #Connection with the server
                    
                        print("Connected")
                    
                        l_ip_5.config(text='IP:%s'%ip_adr)
                        l_ip_4.config(text='Connected')
                        l_ip_4.config(bg='#558B2F')

                        replace_num('IP:',ip_adr)
                        E1.config(state='disabled')      #Disable the Entry
                        Btn14.config(state='disabled',bg='#212121')   #Disable the Entry
                    
                        ip_stu=0                         #'0' means connected
                    
                        at=thread.Thread(target=code_receive) #Define a thread for data receiving
                        at.setDaemon(True)                    #'True' means it is a front thread,it would close when the mainloop() closes
                        at.start()                            #Thread starts
                        break
                    else:
                        break
                except Exception:
                    print("Cannot connecting to server,try it latter!")
                    l_ip_4.config(text='Try %d/5 time(s)'%i)
                    l_ip_4.config(bg='#EF6C00')
                    print('Try %d/5 time(s)'%i)
                    ip_stu=1
                    time.sleep(1)
                    continue
            if ip_stu == 1:
                l_ip_4.config(text='Disconnected')
                l_ip_4.config(bg='#F44336')

        def code_receive():     #A function for data receiving
            global led_status,ipcon,findline_status,auto_status,opencv_status,speech_status
            while True:
                code_car = tcpClicSock.recv(BUFSIZ) #Listening,and save the data in 'code_car'
                l_ip.config(text=code_car)          #Put the data on the label
                #print(code_car)
                data = code_car.decode()
                if not code_car:
                    continue
                elif 'L0' == data:
                    l_ip_L.config(text='L0')
                elif 'L1' == data:
                    l_ip_L.config(text='L1')
                elif 'L2' == data:
                    l_ip_L.config(text='L2')
                elif 'L3' == data:
                    l_ip_L.config(text='L3')
                elif 'L4' == data:
                    l_ip_L.config(text='L4')
                elif 'L5' == data:
                    l_ip_L.config(text='L5')
                elif 'L6' == data:
                    l_ip_L.config(text='L6')
                elif 'L7' == data:
                    l_ip_L.config(text='L7')
                elif 'L8' == data:
                    l_ip_L.config(text='L8')
                elif 'L9' == data:
                    l_ip_L.config(text='L9')
                elif 'L10' == data:
                    l_ip_L.config(text='L10')
                elif 'L11' == data:
                    l_ip_L.config(text='L11')
                elif 'L12' == data:
                    l_ip_L.config(text='L12')
                elif 'L13' == data:
                    l_ip_L.config(text='L13')
                elif 'L14' == data:
                    l_ip_L.config(text='L14')
                elif 'L15' == data:
                    l_ip_L.config(text='L15')



                elif 'ST1' == data:
                    l_ip_SET.config(text='ST1')
                elif 'ST2' == data:
                    l_ip_SET.config(text='ST2')
                elif 'ST3' == data:
                    l_ip_SET.config(text='ST3')
                elif 'ST4' == data:
                    l_ip_SET.config(text='ST4')
                elif 'ST5' == data:
                    l_ip_SET.config(text='ST5')
                elif 'ST6' == data:
                    l_ip_SET.config(text='ST6')
                elif 'ST7' == data:
                    l_ip_SET.config(text='ST7')
                elif 'ST8' == data:
                    l_ip_SET.config(text='ST8')
                elif 'ST9' == data:
                    l_ip_SET.config(text='ST9')
                elif 'ST10' == data:
                    l_ip_SET.config(text='ST10')
                elif 'ST11' == data:
                    l_ip_SET.config(text='ST11')
                elif 'ST12' == data:
                    l_ip_SET.config(text='ST12')
                elif 'ST13' == data:
                    l_ip_SET.config(text='ST13')
                elif 'ST14' == data:
                    l_ip_SET.config(text='ST14')
                elif 'MAX' == data:
                    l_ip_SET.config(text='MAX')
                elif 'MIN' == data:
                    l_ip_SET.config(text='MIN')

                else:
                    try:
                        org = int(data)
                        var_pwm.set(org)
                    except:
                        pass

        s1 = tk.Scale(root,label="PWM",
        from_=100,to=700,orient=tk.HORIZONTAL,length=740,
        showvalue=1,tickinterval=100,resolution=1,variable=var_pwm,troughcolor='#42A5F5',fg=color_text,command=set_pwm,bg=color_bg,highlightthickness=0)
        s1.place(x=30,y=270)                            #Define a Scale and put it in position

        s2 = tk.Scale(root,label="SETPS",
        from_=1,to=14,orient=tk.HORIZONTAL,length=440,
        showvalue=1,tickinterval=1,resolution=1,variable=var_setps,troughcolor='#42A5F5',fg=color_text,bg=color_bg,highlightthickness=0)
        s2.place(x=330,y=350)                            #Define a Scale and put it in position

        s3 = tk.Scale(root,label="TIME",
        from_=0.1,to=1,orient=tk.HORIZONTAL,length=440,
        showvalue=0.1,tickinterval=0.2,resolution=0.1,variable=var_time,troughcolor='#42A5F5',fg=color_text,bg=color_bg,highlightthickness=0)
        s3.place(x=330,y=450)                            #Define a Scale and put it in position

        Btn_RUN = tk.Button(root, width=18, text='RUN',bd=0,fg=color_text,bg=color_btn,relief='ridge',command=set_run)
        Btn_RUN.place(x=187,y=388)

        Btn_ALL = tk.Button(root, width=18, text='RUN ALL',bd=0,fg=color_text,bg=color_btn,relief='ridge',command=set_all)
        Btn_ALL.place(x=187,y=428)

        Btn_STOP = tk.Button(root, width=18, text='STOP',bd=0,fg=color_text,bg=color_btn,relief='ridge',command=set_stop)
        Btn_STOP.place(x=187,y=488)

        Btn_STEPALL = tk.Button(root, width=18, text='STEP ALL',bd=0,fg=color_text,bg=color_btn,relief='ridge',command=set_stepall)
        Btn_STEPALL.place(x=30,y=488)

        l_ip=tk.Label(root,width=18,text='Status',fg=color_text,bg=color_btn)
        l_ip.place(x=30,y=110)                           #Define a Label and put it in position

        l_ip_2=tk.Label(root,width=18,text='pwm:%s'%(var_pwm.get()),fg=color_text,bg=color_btn)
        l_ip_2.place(x=30,y=145)                         #Define a Label and put it in position

        l_ip_L=tk.Label(root,width=18,text='choose L',fg=color_text,bg=color_btn)
        l_ip_L.place(x=230,y=145) 

        l_ip_SET=tk.Label(root,width=18,text='pos set',fg=color_text,bg=color_btn)
        l_ip_SET.place(x=430,y=145) 

        l_ip_4=tk.Label(root,width=18,text='Disconnected',fg=color_text,bg='#F44336')
        l_ip_4.place(x=637,y=110)                         #Define a Label and put it in position

        l_ip_5=tk.Label(root,width=18,text='Use default IP',fg=color_text,bg=color_btn)
        l_ip_5.place(x=637,y=145)                         #Define a Label and put it in position

        E1 = tk.Entry(root,show=None,width=16,bg="#37474F",fg='#eceff1')
        E1.place(x=170,y=40)                             #Define a Entry and put it in position

        l_ip_3=tk.Label(root,width=10,text='IP Address:',fg=color_text,bg='#000000')
        l_ip_3.place(x=165,y=15)                         #Define a Label and put it in position

        Btn14= tk.Button(root, width=8, text='Connect',fg=color_text,bg=color_btn,command=connect_2,relief='ridge')
        Btn14.place(x=300,y=35)                          #Define a Button and put it in position

        #Define buttons and put these in position
        Btn0 = tk.Button(root, width=3, text='+',bd=0,fg=color_text,bg=color_btn,relief='ridge')
        Btn1 = tk.Button(root, width=3, text='-',bd=0,fg=color_text,bg=color_btn,relief='ridge')

        Btn0.place(x=30,y=195)
        Btn1.place(x=30,y=230)

        Btn_L0 = tk.Button(root, width=3, text='L0',bd=0,fg=color_text,bg=color_btn,relief='ridge',command=set_L0)
        Btn_L0.place(x=65,y=195)

        Btn_L1 = tk.Button(root, width=3, text='L1',bd=0,fg=color_text,bg=color_btn,relief='ridge',command=set_L1)
        Btn_L1.place(x=100,y=195)
        
        Btn_L2 = tk.Button(root, width=3, text='L2',bd=0,fg=color_text,bg=color_btn,relief='ridge',command=set_L2)
        Btn_L2.place(x=135,y=195)

        Btn_L3 = tk.Button(root, width=3, text='L3',bd=0,fg=color_text,bg=color_btn,relief='ridge',command=set_L3)
        Btn_L3.place(x=170,y=195)

        Btn_L4 = tk.Button(root, width=3, text='L4',bd=0,fg=color_text,bg=color_btn,relief='ridge',command=set_L4)
        Btn_L4.place(x=205,y=195)

        Btn_L5 = tk.Button(root, width=3, text='L5',bd=0,fg=color_text,bg=color_btn,relief='ridge',command=set_L5)
        Btn_L5.place(x=240,y=195)

        Btn_L6 = tk.Button(root, width=3, text='L6',bd=0,fg=color_text,bg=color_btn,relief='ridge',command=set_L6)
        Btn_L6.place(x=275,y=195)

        Btn_L7 = tk.Button(root, width=3, text='L7',bd=0,fg=color_text,bg=color_btn,relief='ridge',command=set_L7)
        Btn_L7.place(x=310,y=195)

        Btn_L8 = tk.Button(root, width=3, text='L8',bd=0,fg=color_text,bg=color_btn,relief='ridge',command=set_L8)
        Btn_L8.place(x=345,y=195)

        Btn_L9 = tk.Button(root, width=3, text='L9',bd=0,fg=color_text,bg=color_btn,relief='ridge',command=set_L9)
        Btn_L9.place(x=380,y=195)

        Btn_L10 = tk.Button(root, width=3, text='L10',bd=0,fg=color_text,bg=color_btn,relief='ridge',command=set_L10)
        Btn_L10.place(x=415,y=195)

        Btn_L11 = tk.Button(root, width=3, text='L11',bd=0,fg=color_text,bg=color_btn,relief='ridge',command=set_L11)
        Btn_L11.place(x=450,y=195)

        Btn_L12 = tk.Button(root, width=3, text='L12',bd=0,fg=color_text,bg=color_btn,relief='ridge',command=set_L12)
        Btn_L12.place(x=485,y=195)

        Btn_L13 = tk.Button(root, width=3, text='L13',bd=0,fg=color_text,bg=color_btn,relief='ridge',command=set_L13)
        Btn_L13.place(x=520,y=195)

        Btn_L14 = tk.Button(root, width=3, text='L14',bd=0,fg=color_text,bg=color_btn,relief='ridge',command=set_L14)
        Btn_L14.place(x=555,y=195)

        Btn_L15 = tk.Button(root, width=3, text='L15',bd=0,fg=color_text,bg=color_btn,relief='ridge',command=set_L15)
        Btn_L15.place(x=590,y=195)

        Btn_CONFIG = tk.Button(root, width=18, text='CONFIG',bd=0,fg=color_text,bg=color_btn,relief='ridge',command=set_config)
        Btn_CONFIG.place(x=637,y=195)

        Btn_SAVE = tk.Button(root, width=8, text='SAVE',bd=0,fg=color_text,bg=color_btn,relief='ridge',command=set_save)
        Btn_SAVE.place(x=637,y=230)

        Btn_RESET = tk.Button(root, width=8, text='RESET',bd=0,fg=color_text,bg=color_btn,relief='ridge',command=set_reset)
        Btn_RESET.place(x=707,y=230)


        Btn_ST1 = tk.Button(root, width=3, text='ST1',bd=0,fg=color_text,bg=color_btn,relief='ridge',command=set_ST1)
        Btn_ST1.place(x=65,y=230)
        
        Btn_ST2 = tk.Button(root, width=3, text='ST2',bd=0,fg=color_text,bg=color_btn,relief='ridge',command=set_ST2)
        Btn_ST2.place(x=100,y=230)

        Btn_ST3 = tk.Button(root, width=3, text='ST3',bd=0,fg=color_text,bg=color_btn,relief='ridge',command=set_ST3)
        Btn_ST3.place(x=135,y=230)

        Btn_ST4 = tk.Button(root, width=3, text='ST4',bd=0,fg=color_text,bg=color_btn,relief='ridge',command=set_ST4)
        Btn_ST4.place(x=170,y=230)

        Btn_ST5 = tk.Button(root, width=3, text='ST5',bd=0,fg=color_text,bg=color_btn,relief='ridge',command=set_ST5)
        Btn_ST5.place(x=205,y=230)

        Btn_ST6 = tk.Button(root, width=3, text='ST6',bd=0,fg=color_text,bg=color_btn,relief='ridge',command=set_ST6)
        Btn_ST6.place(x=240,y=230)

        Btn_ST7 = tk.Button(root, width=3, text='ST7',bd=0,fg=color_text,bg=color_btn,relief='ridge',command=set_ST7)
        Btn_ST7.place(x=275,y=230)

        Btn_ST8 = tk.Button(root, width=3, text='ST8',bd=0,fg=color_text,bg=color_btn,relief='ridge',command=set_ST8)
        Btn_ST8.place(x=310,y=230)

        Btn_ST9 = tk.Button(root, width=3, text='ST9',bd=0,fg=color_text,bg=color_btn,relief='ridge',command=set_ST9)
        Btn_ST9.place(x=345,y=230)

        Btn_ST10 = tk.Button(root, width=3, text='ST10',bd=0,fg=color_text,bg=color_btn,relief='ridge',command=set_ST10)
        Btn_ST10.place(x=380,y=230)

        Btn_ST11 = tk.Button(root, width=3, text='ST11',bd=0,fg=color_text,bg=color_btn,relief='ridge',command=set_ST11)
        Btn_ST11.place(x=415,y=230)

        Btn_ST12 = tk.Button(root, width=3, text='ST12',bd=0,fg=color_text,bg=color_btn,relief='ridge',command=set_ST12)
        Btn_ST12.place(x=450,y=230)

        Btn_ST13 = tk.Button(root, width=3, text='ST13',bd=0,fg=color_text,bg=color_btn,relief='ridge',command=set_ST13)
        Btn_ST13.place(x=485,y=230)

        Btn_ST14 = tk.Button(root, width=3, text='ST14',bd=0,fg=color_text,bg=color_btn,relief='ridge',command=set_ST14)
        Btn_ST14.place(x=520,y=230)

        Btn_MIN = tk.Button(root, width=3, text='MIN',bd=0,fg=color_text,bg=color_btn,relief='ridge',command=set_MIN)
        Btn_MIN.place(x=555,y=230)

        Btn_MAX = tk.Button(root, width=3, text='MAX',bd=0,fg=color_text,bg=color_btn,relief='ridge',command=set_MAX)
        Btn_MAX.place(x=590,y=230)


        # Bind the buttons with the corresponding callback function
        Btn0.bind('<ButtonPress-1>', call_forward)
        Btn1.bind('<ButtonPress-1>', call_back)

        # Bind the keys with the corresponding callback function
        root.bind('<KeyPress-w>', call_forward) 
        root.bind('<KeyPress-s>', call_back)

        # When these keys is released,call the function call_stop()


        # Press these keyss to call the corresponding function()
        root.bind('<Return>', connect)

        
        global stat
        if stat==0:              # Ensure the mainloop runs only once
                root.mainloop()  # Run the mainloop()
                stat=1           # Change the value to '1' so the mainloop() would not run again.

if __name__ == '__main__':
    setPWM_threading=thread.Thread(target=set_pwm_thread)      #Define a thread for FPV and OpenCV
    setPWM_threading.setDaemon(True)                             #'True' means it is a front thread,it would close when the mainloop() closes
    setPWM_threading.start()                                     #Thread starts
    try:
        loop()                   # Load GUI
    except KeyboardInterrupt:
        tcpClicSock.close()          # Close socket or it may not connect with the server again

