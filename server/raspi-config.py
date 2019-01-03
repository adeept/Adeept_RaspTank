#!/usr/bin/python3
# File name   : server.py
# Description : The main program server takes control of Ultrasonic,Motor,Servo by receiving the order from the client through TCP and carrying out the corresponding operation.
# Website     : www.adeept.com
# E-mail      : support@adeept.com
# Author      : William
# Date        : 2018/10/12

import socket
import time
import Adafruit_PCA9685
import os


pwm = Adafruit_PCA9685.PCA9685()    #Ultrasonic Control
pwm.set_pwm_freq(50)

def replace_num(initial,new_num):   #Call this function to replace data in '.txt' file
    global r
    newline=""
    str_num=str(new_num)
    with open("config.txt","r") as f:
        for line in f.readlines():
            if(line.find(initial) == 0):
                line = initial+"%s" %(str_num+"\n")
            newline += line
    with open("config.txt","w") as f:
        f.writelines(newline)

def num_import_int(initial):        #Call this function to import data from '.txt' file
    global r
    with open("config.txt") as f:
        for line in f.readlines():
            if(line.find(initial) == 0):
                r=line
    begin=len(list(initial))
    snum=r[begin:]
    n=int(snum)
    return n

#L0
L0_MAX = num_import_int('L0_MAX:')
L0_MIN = num_import_int('L0_MIN:')
L0_ST1 = num_import_int('L0_ST1:')
L0_ST2 = num_import_int('L0_ST2:')
L0_ST3 = num_import_int('L0_ST3:')
L0_ST4 = num_import_int('L0_ST4:')
L0_ST5 = num_import_int('L0_ST5:')
L0_ST6 = num_import_int('L0_ST6:')
L0_ST7 = num_import_int('L0_ST7:')
L0_ST8 = num_import_int('L0_ST8:')
L0_ST9 = num_import_int('L0_ST9:')
L0_ST10 = num_import_int('L0_ST10:')
#L1
L1_MAX = num_import_int('L1_MAX:')
L1_MIN = num_import_int('L1_MIN:')
L1_ST1 = num_import_int('L1_ST1:')
L1_ST2 = num_import_int('L1_ST2:')
L1_ST3 = num_import_int('L1_ST3:')
L1_ST4 = num_import_int('L1_ST4:')
L1_ST5 = num_import_int('L1_ST5:')
L1_ST6 = num_import_int('L1_ST6:')
L1_ST7 = num_import_int('L1_ST7:')
L1_ST8 = num_import_int('L1_ST8:')
L1_ST9 = num_import_int('L1_ST9:')
L1_ST10 = num_import_int('L1_ST10:')
#L2
L2_MAX = num_import_int('L2_MAX:')
L2_MIN = num_import_int('L2_MIN:')
L2_ST1 = num_import_int('L2_ST1:')
L2_ST2 = num_import_int('L2_ST2:')
L2_ST3 = num_import_int('L2_ST3:')
L2_ST4 = num_import_int('L2_ST4:')
L2_ST5 = num_import_int('L2_ST5:')
L2_ST6 = num_import_int('L2_ST6:')
L2_ST7 = num_import_int('L2_ST7:')
L2_ST8 = num_import_int('L2_ST8:')
L2_ST9 = num_import_int('L2_ST9:')
L2_ST10 = num_import_int('L2_ST10:')
#L3
L3_MAX = num_import_int('L3_MAX:')
L3_MIN = num_import_int('L3_MIN:')
L3_ST1 = num_import_int('L3_ST1:')
L3_ST2 = num_import_int('L3_ST2:')
L3_ST3 = num_import_int('L3_ST3:')
L3_ST4 = num_import_int('L3_ST4:')
L3_ST5 = num_import_int('L3_ST5:')
L3_ST6 = num_import_int('L3_ST6:')
L3_ST7 = num_import_int('L3_ST7:')
L3_ST8 = num_import_int('L3_ST8:')
L3_ST9 = num_import_int('L3_ST9:')
L3_ST10 = num_import_int('L3_ST10:')
#L4
L4_MAX = num_import_int('L4_MAX:')
L4_MIN = num_import_int('L4_MIN:')
L4_ST1 = num_import_int('L4_ST1:')
L4_ST2 = num_import_int('L4_ST2:')
L4_ST3 = num_import_int('L4_ST3:')
L4_ST4 = num_import_int('L4_ST4:')
L4_ST5 = num_import_int('L4_ST5:')
L4_ST6 = num_import_int('L4_ST6:')
L4_ST7 = num_import_int('L4_ST7:')
L4_ST8 = num_import_int('L4_ST8:')
L4_ST9 = num_import_int('L4_ST9:')
L4_ST10 = num_import_int('L4_ST10:')
#L5
L5_MAX = num_import_int('L5_MAX:')
L5_MIN = num_import_int('L5_MIN:')
L5_ST1 = num_import_int('L5_ST1:')
L5_ST2 = num_import_int('L5_ST2:')
L5_ST3 = num_import_int('L5_ST3:')
L5_ST4 = num_import_int('L5_ST4:')
L5_ST5 = num_import_int('L5_ST5:')
L5_ST6 = num_import_int('L5_ST6:')
L5_ST7 = num_import_int('L5_ST7:')
L5_ST8 = num_import_int('L5_ST8:')
L5_ST9 = num_import_int('L5_ST9:')
L5_ST10 = num_import_int('L5_ST10:')
#L6
L6_MAX = num_import_int('L6_MAX:')
L6_MIN = num_import_int('L6_MIN:')
L6_ST1 = num_import_int('L6_ST1:')
L6_ST2 = num_import_int('L6_ST2:')
L6_ST3 = num_import_int('L6_ST3:')
L6_ST4 = num_import_int('L6_ST4:')
L6_ST5 = num_import_int('L6_ST5:')
L6_ST6 = num_import_int('L6_ST6:')
L6_ST7 = num_import_int('L6_ST7:')
L6_ST8 = num_import_int('L6_ST8:')
L6_ST9 = num_import_int('L6_ST9:')
L6_ST10 = num_import_int('L6_ST10:')
#L7
L7_MAX = num_import_int('L7_MAX:')
L7_MIN = num_import_int('L7_MIN:')
L7_ST1 = num_import_int('L7_ST1:')
L7_ST2 = num_import_int('L7_ST2:')
L7_ST3 = num_import_int('L7_ST3:')
L7_ST4 = num_import_int('L7_ST4:')
L7_ST5 = num_import_int('L7_ST5:')
L7_ST6 = num_import_int('L7_ST6:')
L7_ST7 = num_import_int('L7_ST7:')
L7_ST8 = num_import_int('L7_ST8:')
L7_ST9 = num_import_int('L7_ST9:')
L7_ST10 = num_import_int('L7_ST10:')
#L8
L8_MAX = num_import_int('L8_MAX:')
L8_MIN = num_import_int('L8_MIN:')
L8_ST1 = num_import_int('L8_ST1:')
L8_ST2 = num_import_int('L8_ST2:')
L8_ST3 = num_import_int('L8_ST3:')
L8_ST4 = num_import_int('L8_ST4:')
L8_ST5 = num_import_int('L8_ST5:')
L8_ST6 = num_import_int('L8_ST6:')
L8_ST7 = num_import_int('L8_ST7:')
L8_ST8 = num_import_int('L8_ST8:')
L8_ST9 = num_import_int('L8_ST9:')
L8_ST10 = num_import_int('L8_ST10:')
#L9
L9_MAX = num_import_int('L9_MAX:')
L9_MIN = num_import_int('L9_MIN:')
L9_ST1 = num_import_int('L9_ST1:')
L9_ST2 = num_import_int('L9_ST2:')
L9_ST3 = num_import_int('L9_ST3:')
L9_ST4 = num_import_int('L9_ST4:')
L9_ST5 = num_import_int('L9_ST5:')
L9_ST6 = num_import_int('L9_ST6:')
L9_ST7 = num_import_int('L9_ST6:')
L9_ST8 = num_import_int('L9_ST6:')
L9_ST9 = num_import_int('L9_ST6:')
L9_ST10 = num_import_int('L9_ST10:')
#L10
L10_MAX = num_import_int('L10_MAX:')
L10_MIN = num_import_int('L10_MIN:')
L10_ST1 = num_import_int('L10_ST1:')
L10_ST2 = num_import_int('L10_ST2:')
L10_ST3 = num_import_int('L10_ST3:')
L10_ST4 = num_import_int('L10_ST4:')
L10_ST5 = num_import_int('L10_ST5:')
L10_ST6 = num_import_int('L10_ST6:')
L10_ST7 = num_import_int('L10_ST7:')
L10_ST8 = num_import_int('L10_ST8:')
L10_ST9 = num_import_int('L10_ST9:')
L10_ST10 = num_import_int('L10_ST10:')
#L11
L11_MAX = num_import_int('L11_MAX:')
L11_MIN = num_import_int('L11_MIN:')
L11_ST1 = num_import_int('L11_ST1:')
L11_ST2 = num_import_int('L11_ST2:')
L11_ST3 = num_import_int('L11_ST3:')
L11_ST4 = num_import_int('L11_ST4:')
L11_ST5 = num_import_int('L11_ST5:')
L11_ST6 = num_import_int('L11_ST6:')
L11_ST7 = num_import_int('L11_ST7:')
L11_ST8 = num_import_int('L11_ST8:')
L11_ST9 = num_import_int('L11_ST9:')
L11_ST10 = num_import_int('L11_ST10:')
#L12
L12_MAX = num_import_int('L12_MAX:')
L12_MIN = num_import_int('L12_MIN:')
L12_ST1 = num_import_int('L12_ST1:')
L12_ST2 = num_import_int('L12_ST2:')
L12_ST3 = num_import_int('L12_ST3:')
L12_ST4 = num_import_int('L12_ST4:')
L12_ST5 = num_import_int('L12_ST5:')
L12_ST6 = num_import_int('L12_ST6:')
L12_ST7 = num_import_int('L12_ST7:')
L12_ST8 = num_import_int('L12_ST8:')
L12_ST9 = num_import_int('L12_ST9:')
L12_ST10 = num_import_int('L12_ST10:')
#L13
L13_MAX = num_import_int('L13_MAX:')
L13_MIN = num_import_int('L13_MIN:')
L13_ST1 = num_import_int('L13_ST1:')
L13_ST2 = num_import_int('L13_ST2:')
L13_ST3 = num_import_int('L13_ST3:')
L13_ST4 = num_import_int('L13_ST4:')
L13_ST5 = num_import_int('L13_ST5:')
L13_ST6 = num_import_int('L13_ST6:')
L13_ST7 = num_import_int('L13_ST7:')
L13_ST8 = num_import_int('L13_ST8:')
L13_ST9 = num_import_int('L13_ST9:')
L13_ST10 = num_import_int('L13_ST10:')
#L14
L14_MAX = num_import_int('L14_MAX:')
L14_MIN = num_import_int('L14_MIN:')
L14_ST1 = num_import_int('L14_ST1:')
L14_ST2 = num_import_int('L14_ST2:')
L14_ST3 = num_import_int('L14_ST3:')
L14_ST4 = num_import_int('L14_ST4:')
L14_ST5 = num_import_int('L14_ST5:')
L14_ST6 = num_import_int('L14_ST6:')
L14_ST7 = num_import_int('L14_ST7:')
L14_ST8 = num_import_int('L14_ST8:')
L14_ST9 = num_import_int('L14_ST9:')
L14_ST10 = num_import_int('L14_ST10:')
#L15
L15_MAX = num_import_int('L15_MAX:')
L15_MIN = num_import_int('L15_MIN:')
L15_ST1 = num_import_int('L15_ST1:')
L15_ST2 = num_import_int('L15_ST2:')
L15_ST3 = num_import_int('L15_ST3:')
L15_ST4 = num_import_int('L15_ST4:')
L15_ST5 = num_import_int('L15_ST5:')
L15_ST6 = num_import_int('L15_ST6:')
L15_ST7 = num_import_int('L15_ST7:')
L15_ST8 = num_import_int('L15_ST8:')
L15_ST9 = num_import_int('L15_ST9:')
L15_ST10 = num_import_int('L15_ST10:')


ip_con  = ''


org=425

set_L = 1
set_ST = 1

def destroy():               #Clean up
    connection.close()

def run():                   #Main loop
    global org,ip_con,set_L,set_ST,r
    while True:              #Connection
        s =socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.connect(("1.1.1.1",80))
        ipaddr_check=s.getsockname()[0]
        s.close()
        print(ipaddr_check)
        print('waiting for connection...')
        tcpCliSock, addr = tcpSerSock.accept()#Determine whether to connect
        print('...connected from :', addr)
        pwm.set_pwm(2, 0, 0)
        pwm.set_pwm(1, 0, 0)
        pwm.set_pwm(0, 0, 0)
        pwm.set_pwm(15, 0, 0)
        break

    while True: 
        data = ''
        data = tcpCliSock.recv(BUFSIZ).decode()
        if not data:
            continue
        elif 'L0' == data:
            set_L = 0
            tcpCliSock.send(('L0').encode())
        elif 'L1' == data:
            set_L = 1
            tcpCliSock.send(('L1').encode())
        elif 'L2' == data:
            set_L = 2
            tcpCliSock.send(('L2').encode())
        elif 'L3' == data:
            set_L = 3
            tcpCliSock.send(('L3').encode())
        elif 'L4' == data:
            set_L = 4
            tcpCliSock.send(('L4').encode())
        elif 'L5' == data:
            set_L = 5
            tcpCliSock.send(('L5').encode())
        elif 'L6' == data:
            set_L = 6
            tcpCliSock.send(('L6').encode())
        elif 'L7' == data:
            set_L = 7
            tcpCliSock.send(('L7').encode())
        elif 'L8' == data:
            set_L = 8
            tcpCliSock.send(('L8').encode())
        elif 'L9' == data:
            set_L = 9
            tcpCliSock.send(('L9').encode())
        elif 'L10' == data:
            set_L = 10
            tcpCliSock.send(('L10').encode())
        elif 'L11' == data:
            set_L = 11
            tcpCliSock.send(('L11').encode())
        elif 'L12' == data:
            set_L = 12
            tcpCliSock.send(('L12').encode())
        elif 'L13' == data:
            set_L = 13
            tcpCliSock.send(('L13').encode())
        elif 'L14' == data:
            set_L = 14
            tcpCliSock.send(('L14').encode())
        elif 'L15' == data:
            set_L = 15
            tcpCliSock.send(('L15').encode())



        elif 'ST1' == data:
            set_ST = 'ST1'
            pwm.set_pwm(set_L, 0, num_import_int('L%d_%s:'%(set_L,set_ST)))
            tcpCliSock.send(('ST1').encode())
        elif 'ST2' == data:
            set_ST = 'ST2'
            pwm.set_pwm(set_L, 0, num_import_int('L%d_%s:'%(set_L,set_ST)))
            tcpCliSock.send(('ST2').encode())
        elif 'ST3' == data:
            set_ST = 'ST3'
            pwm.set_pwm(set_L, 0, num_import_int('L%d_%s:'%(set_L,set_ST)))
            tcpCliSock.send(('ST3').encode())
        elif 'ST4' == data:
            set_ST = 'ST4'
            pwm.set_pwm(set_L, 0, num_import_int('L%d_%s:'%(set_L,set_ST)))
            tcpCliSock.send(('ST4').encode())
        elif 'ST5' == data:
            set_ST = 'ST5'
            pwm.set_pwm(set_L, 0, num_import_int('L%d_%s:'%(set_L,set_ST)))
            tcpCliSock.send(('ST5').encode())
        elif 'ST6' == data:
            set_ST = 'ST6'
            pwm.set_pwm(set_L, 0, num_import_int('L%d_%s:'%(set_L,set_ST)))
            tcpCliSock.send(('ST6').encode())
        elif 'ST7' == data:
            set_ST = 'ST7'
            pwm.set_pwm(set_L, 0, num_import_int('L%d_%s:'%(set_L,set_ST)))
            tcpCliSock.send(('ST7').encode())
        elif 'ST8' == data:
            set_ST = 'ST8'
            pwm.set_pwm(set_L, 0, num_import_int('L%d_%s:'%(set_L,set_ST)))
            tcpCliSock.send(('ST8').encode())
        elif 'ST9' == data:
            set_ST = 'ST9'
            pwm.set_pwm(set_L, 0, num_import_int('L%d_%s:'%(set_L,set_ST)))
            tcpCliSock.send(('ST9').encode())
        elif 'ST10' == data:
            set_ST = 'ST10'
            pwm.set_pwm(set_L, 0, num_import_int('L%d_%s:'%(set_L,set_ST)))
            tcpCliSock.send(('ST10').encode())
        elif 'ST11' == data:
            set_ST = 'ST11'
            pwm.set_pwm(set_L, 0, num_import_int('L%d_%s:'%(set_L,set_ST)))
            tcpCliSock.send(('ST11').encode())
        elif 'ST12' == data:
            set_ST = 'ST12'
            pwm.set_pwm(set_L, 0, num_import_int('L%d_%s:'%(set_L,set_ST)))
            tcpCliSock.send(('ST12').encode())
        elif 'ST13' == data:
            set_ST = 'ST13'
            pwm.set_pwm(set_L, 0, num_import_int('L%d_%s:'%(set_L,set_ST)))
            tcpCliSock.send(('ST13').encode())
        elif 'ST14' == data:
            set_ST = 'ST14'
            pwm.set_pwm(set_L, 0, num_import_int('L%d_%s:'%(set_L,set_ST)))
            tcpCliSock.send(('ST14').encode())
        elif 'MIN' == data:
            set_ST = 'MIN'
            pwm.set_pwm(set_L, 0, num_import_int('L%d_%s:'%(set_L,set_ST)))
            tcpCliSock.send(('MIN').encode())
        elif 'MAX' == data:
            set_ST = 'MAX'
            pwm.set_pwm(set_L, 0, num_import_int('L%d_%s:'%(set_L,set_ST)))
            tcpCliSock.send(('MAX').encode())



        elif 'add' == data:
            org+=1
            pwm.set_pwm(set_L, 0, org)
            send_pwm=str(org)
            tcpCliSock.send(send_pwm.encode())
            continue

        elif 'sub' == data:                 #Camera Adjustment
            org-=1
            pwm.set_pwm(set_L, 0, org)
            send_pwm=str(org)
            tcpCliSock.send(send_pwm.encode())
            continue

        elif 'config' == data:
            replace_num(('L%d_%s:'%(set_L,set_ST)),org)

        elif 'reset' == data:
            replace_num(('L%d_%s:'%(set_L,set_ST)),org)

        elif 'save' == data:
            replace_num(('L%d_%s:'%(set_L,set_ST)),org)

        elif 'run' in data:
            set_list=data.split()
            try:
                setps = int(set_list[1])
                time_get = round(float(set_list[2]),1)
                print(setps)
                print(time_get)
                for i in range (1,(setps+1)):
                    pwm.set_pwm(set_L, 0, num_import_int('L%d_ST%d:'%(set_L,i)))
                    time.sleep(time_get)
            except:
                print('wrong args')
                pass

        elif 'all' in data:
            try:
                set_list=data.split()
                setps = int(set_list[1])
                time_get = round(float(set_list[2]),1)
                print(setps)
                print(time_get)
                for i in range (1,(setps+1)):
                    for x in range (0,16):
                        pwm.set_pwm(x, 0, num_import_int('L%d_ST%d:'%(x,i)))
                    time.sleep(time_get)
            except:
                print('wrong args')
                pass

        elif 'frame' in data:
            try:
                for i in range (0,16):
                    pwm.set_pwm(i, 0, num_import_int('L%d_%s:'%(i,set_ST)))
            except:
                print('wrong args')
                pass

        elif 'stop' in data:
            pwm.set_pwm(2, 0, 0)
            pwm.set_pwm(1, 0, 0)
            pwm.set_pwm(0, 0, 0)
            pwm.set_pwm(15, 0, 0)
            pwm.set_pwm(14, 0, 0)
            pwm.set_pwm(13, 0, 0)
            pwm.set_pwm(12, 0, 0)
            pwm.set_pwm(11, 0, 0)
            pwm.set_pwm(10, 0, 0)
            pwm.set_pwm(9, 0, 0)
            pwm.set_pwm(8, 0, 0)
            pwm.set_pwm(7, 0, 0)
            pwm.set_pwm(6, 0, 0)
            pwm.set_pwm(5, 0, 0)
            pwm.set_pwm(4, 0, 0)
            pwm.set_pwm(3, 0, 0)  


        else:
            try:
                org = int(data)
                print(org)
                pwm.set_pwm(set_L, 0, org)
            except:
                pass





if __name__ == '__main__':    
    HOST = ''
    PORT = 10223                              #Define port serial 
    BUFSIZ = 1024                             #Define buffer size
    ADDR = (HOST, PORT)

    tcpSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpSerSock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    tcpSerSock.bind(ADDR)
    tcpSerSock.listen(5)
                          #Start server,waiting for client
    try:
        run()

    except KeyboardInterrupt:
        pwm.set_pwm(2, 0, 0)
        pwm.set_pwm(1, 0, 0)
        pwm.set_pwm(0, 0, 0)
        pwm.set_pwm(15, 0, 0)
        pwm.set_pwm(14, 0, 0)
        pwm.set_pwm(13, 0, 0)
        pwm.set_pwm(12, 0, 0)
        pwm.set_pwm(11, 0, 0)
        pwm.set_pwm(10, 0, 0)
        pwm.set_pwm(9, 0, 0)
        pwm.set_pwm(8, 0, 0)
        pwm.set_pwm(7, 0, 0)
        pwm.set_pwm(6, 0, 0)
        pwm.set_pwm(5, 0, 0)
        pwm.set_pwm(4, 0, 0)
        pwm.set_pwm(3, 0, 0)

        destroy()
