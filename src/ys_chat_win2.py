#########################################
## Programme YS Chat                   ##
## auteur : VincentWeb, Toulouse, 2006 ##
## licence : GPL                       ##
#########################################

# -*- coding: Latin-1 -*-

# .master -> revenir a la classe parente
#compile in C -> http://python.developpez.com/faq/?page=Optimisation


#New things of the version 0.1074:

#fixed the bug of the client mode by command line
#restrictions for clients: no '|', 255 caracters for the messages
#fixed the problem of the users flying before YSchat runs

## NEW FONTIONALITIES TO DO
#TODO: convert the url in links!
#TODO: debug file for the player list!!
#TODO: command to see the automessage already set
#TODO: japenese version
#TODO: several automated messages
#TODO: clever pilot list updated with the messages xxx took-off
#TODO: infos on players: right-clic pilot list (plane fliyng, ysp?, squad?)
#TODO: scroll-bar for pilot list
#TODO: version ! then version without ! -> change the line to check in the last-version file
#TODO: Backup the automessage after auto-reconnect
#TODO: count the number of planes a pilot has killed

#TODO:#Commands to make:
#/myip print my ip
#/ysfs launch ysflight in client with the current ip and username
#(from ysfs) /lastmess each ysfs client must send the time they sent their last message + the real username + the last message

##BUGS TO FIX :
#FIXME: New connection, name of map shorter, old name isn't cleared
#FIXME: autoserver doesn't work
#FIXME: double player list after connection
#FIXME: map = unknown if server will reset in 10/5 minutes
#FIXME: weird caracters in messages
#FIXME: Still some problems to find the username, replace the :)
#FIXME: loadcolors doesn't work
#FIXME: very long message -> username cut ??
#FIXME: wrong player-list sometimes
#FIXME: sometimes doesn't give the player list after the connection
#FIXME: too long messages : don't cut the words!!
#FIXME: command $thetime only time, why not $time ? -> so detect '$time ' and not '$time'
#FIXME: tkmessagebox in threads doesn't work ??

##############################
## Import external functions :

from socket import *
from Tkinter import *
from random import randrange
from time import localtime,strftime,gmtime,daylight,timezone,sleep,time
from Pmw import ComboBox,initialise
import sys,threading,re,tkMessageBox,os,tkFileDialog,urllib,httplib,glob,webbrowser,struct,random,feedparser
#import pygame

try: import psyco; psyco.full() 
except: pass

##########
## Classes

class Application(Frame):
    "master class with the window and all the widgets, also a method to connect and send a message"
    def __init__(self): 
        Frame.__init__(self)
        #self.racine=Tk()
        self.pingStart=time()
        self.ysc_mode=0
        self.conn_time=0
        self.autodetect=1        
        #not connected at the start
        self.exit=0
        self.autoip=""
        self.folder=os.getcwd()
        self.connected=0
        self.time=time()
        self.canreconnect=0
        self.sendauto=0
        self.autoserver=0
        self.automap=0
        self.th_version=ThreadCheckversion()
        self.th_version.start()
        self.master.title("YSC : YS chat")
        #initialise(self.master)#??????
        self.pack()
        
        #---fermeture du programme
        self.master.protocol("WM_DELETE_WINDOW", self.exit_ysc)
        menubar = Menu(self)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Connect",underline=1,command = lambda conn_version=20080220 : self.connect(conn_version))        
        filemenu.add_command(label="Disconnect",underline=1,command=self.disconnect2)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", underline=1,command=self.exit_ysc)#close the trhead before
        menubar.add_cascade(label="File", menu=filemenu)
                
        #---sound
##        try:
##            pygame.mixer.init()
##            pygame.mixer.music.load("newmess.wav")
##        except:
##            print("Failed to load the sounds")
        #---menu
        insertmenu = Menu(menubar, tearoff=0)        
        menubar.add_cascade(label="Insert", menu=insertmenu)
        insertmenu.add_command(label="Variables",foreground ='blue')
        insertmenu.add_command(label="$datetime",underline=1,command=lambda text ='$datetime ': self.insert(text))
        insertmenu.add_command(label="$daylight",underline=1,command=lambda text ='$daylight ': self.insert(text))
        insertmenu.add_command(label="$time",underline=1,command=lambda text ='$time ': self.insert(text))
        insertmenu.add_command(label="$gmtime",underline=1,command=lambda text ='$gmtime ': self.insert(text))
        insertmenu.add_command(label="$map",underline=1,command=lambda text ='$map ': self.insert(text))
        insertmenu.add_command(label="$me",underline=1,command=lambda text ='$me ': self.insert(text))
        insertmenu.add_command(label="$mynick",underline=1,command=lambda text ='$mynick ': self.insert(text))
        insertmenu.add_command(label="$timezone",underline=1,command=lambda text ='$timezone ': self.insert(text))        
        insertmenu.add_separator()
        insertmenu.add_command(label="Commands",foreground ='blue')
        insertmenu.add_command(label="/auto",underline=1,command=lambda text ='/auto <5>': self.insert(text))
        insertmenu.add_command(label="/autoserver",underline=1,command=lambda text ='/autoserver': self.insert(text))
        insertmenu.add_command(label="/automap",underline=1,command=lambda text ='/automap': self.insert(text))
        insertmenu.add_command(label="/clear",underline=1,command=lambda text ='/clear': self.insert(text))
        insertmenu.add_command(label="/com",underline=1,command=lambda text ='/com': self.insert(text))
        insertmenu.add_command(label="/exit",underline=1,command=lambda text ='/exit': self.insert(text))
        insertmenu.add_command(label="/launchserver",underline=1,command=lambda text ='/launchserver': self.insert(text))
        insertmenu.add_command(label="/loadcolours",underline=1,command=lambda text ='/loadcolours': self.insert(text))
        insertmenu.add_command(label="/list",underline=1,command=lambda text ='/list': self.insert(text))
        insertmenu.add_command(label="/quit",underline=1,command=lambda text ='/quit': self.insert(text))
        insertmenu.add_command(label="/refreshlog",underline=1,command=lambda text ='/refreshlog': self.insert(text))
        insertmenu.add_command(label="/stopauto",underline=1,command=lambda text ='/stopauto': self.insert(text))
        insertmenu.add_command(label="/stopautoserver",underline=1,command=lambda text ='/stopautoserver': self.insert(text))
        insertmenu.add_command(label="/stopautomap",underline=1,command=lambda text ='/stopautomap': self.insert(text))
        
        yspsmenu = Menu(menubar, tearoff=0)  
        menubar.add_cascade(label="YSPS", menu=yspsmenu)
        yspsmenu.add_command(label="Admin",foreground ='blue')
        yspsmenu.add_command(label="/ban (string)username",underline=1,command=lambda text ='/ban ': self.insert(text))
        yspsmenu.add_command(label="/blackout_off",underline=1,command=lambda text ='/blackout_off': self.insert(text))
        yspsmenu.add_command(label="/blackout_on",underline=1,command=lambda text ='/blackout_on': self.insert(text))
        yspsmenu.add_command(label="/collisions_off",underline=1,command=lambda text ='/collisions_off': self.insert(text))
        yspsmenu.add_command(label="/collisions_on",underline=1,command=lambda text ='/collisions_on': self.insert(text))
        yspsmenu.add_command(label="/day",underline=1,command=lambda text ='/day': self.insert(text))
        yspsmenu.add_command(label="/dispell (string)username",underline=1,command=lambda text ='/dispell ': self.insert(text))
        yspsmenu.add_command(label="/flushUsers",underline=1,command=lambda text ='/flushUsers': self.insert(text))
        yspsmenu.add_command(label="/kill_id (number)ID",underline=1,command=lambda text ='/kill_id ': self.insert(text))
        yspsmenu.add_command(label="/kill_user (string) username",underline=1,command=lambda text ='/kill_user ': self.insert(text))
        yspsmenu.add_command(label="/landev_off",underline=1,command=lambda text ='/landev_off': self.insert(text))
        yspsmenu.add_command(label="/landev_on",underline=1,command=lambda text ='/landev_on': self.insert(text))
        yspsmenu.add_command(label="/night",underline=1,command=lambda text ='/night': self.insert(text))
        yspsmenu.add_command(label="/radaralti=nuber in meters",underline=1,command=lambda text ='/radaralti=': self.insert(text))
        yspsmenu.add_command(label="/visib=number in meters",underline=1,command=lambda text ='/visib=': self.insert(text))        
        yspsmenu.add_command(label="/windy=number in m/s",underline=1,command=lambda text ='/windy=': self.insert(text))
        yspsmenu.add_command(label="/windx=number in m/s",underline=1,command=lambda text ='/windx=': self.insert(text))
               
        yspsmenu.add_command(label="All users",foreground ='blue')
        yspsmenu.add_command(label="/distance",underline=1,command=lambda text ='/distance': self.insert(text))
        yspsmenu.add_command(label="/fuel",underline=1,command=lambda text ='/fuel': self.insert(text))
        yspsmenu.add_command(label="/kills",underline=1,command=lambda text ='/kills': self.insert(text))
        yspsmenu.add_command(label="/listuser",underline=1,command=lambda text ='/listuser': self.insert(text))        
        yspsmenu.add_command(label="/lives",underline=1,command=lambda text ='/lives': self.insert(text))
        yspsmenu.add_command(label="/metar",underline=1,command=lambda text ='/metar': self.insert(text))
        yspsmenu.add_command(label="/ping",underline=1,command=lambda text ='/ping': self.insert(text))
        yspsmenu.add_command(label="/pswd%=(string)password",underline=1,command=lambda text ='/pswd%=': self.insert(text))
        yspsmenu.add_command(label="/reset_info",underline=1,command=lambda text ='/reset_info': self.insert(text))
        yspsmenu.add_command(label="/version",underline=1,command=lambda text ='/version': self.insert(text))
        
      
        #---get the path of ysflight
        self.p=Path_ys()
        self.path=self.p.path_ys
        self.sce=self.p.sce
        
        optionmenu = Menu(menubar, tearoff=0)
        optionmenu.add_command(label="Change the YSF path",underline=1,command=self.p.change_path_ys2)
        menubar.add_cascade(label="Options",menu=optionmenu)

        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About",underline=1,command=self.about)
        helpmenu.add_command(label="Help",underline=1,command=self.help)
        menubar.add_cascade(label="Help",menu=helpmenu)
        self.master.config(menu=menubar)
        #Label(self,text='YS chat : tools to discuss with a server',fg='red', font=("Helvetica", 13)).grid(column=0, row=0,columnspan=6)                
        #entry box of the username
        #---boxes
        self.versionbox=Entry(self, width=15)
        self.versionbox.config(bg="#FFFFFF",fg="#FF0000")
        try:
            self.f_ver=open("ver.txt","r")
            self.versionbox.insert(0,self.f_ver.read().replace(' ','').replace('\n','').replace('\r',''))
            self.f_ver.close()
        except:
            self.versionbox.insert(0,"20080220")
        self.versionbox.grid(column=0, row=1) 
        
        self.username = Entry(self, width=25)        
        self.username.config(bg="#EEEEEE",fg="#0000FF") 
        self.username.grid(column=1, row=1)

        #---get the ip-list
        self.ip_list=[]
        try:
            list = feedparser.parse('http://www.yspilots.com/shadowhunters/rssList.php')
            self.ip_list.append('127.0.0.1')
            for ip in list.entries:
                ip=ip.description
                ip=ip[:ip.find(' |')]
                self.ip_list.append(ip)
        except:
            ysip="your ip"
            self.ip_list.append(ysip)
        """try:
            ysfip=open(self.path+"/config/serverhistory.txt",'r')
            while 1:
                ysip=ysfip.readline()
                if ysip=="":
                    break
                ysip=ysip.replace('\n','')   
                ysip=ysip.replace('\r','')
                self.ip_list.append(ysip)
        except:
            ysip="your ip"
            self.ip_list.append(ysip)"""
        self.ip = ComboBox(self,scrolledlist_items = self.ip_list)
        #self.ip=Entry(self, width=15)
        self.ip.grid(column=2, row=1)
        
        #entry box of the port
        self.port = Entry(self, width=6)
        self.port.insert(0,"7915")
        self.port.config(bg="#EEEEEE",fg="#888800") 
        self.port.grid(column=3, row=1)        
        #Label(self.f1, text='').grid(column=0, row=3) #empty line
        #---buttons
        Button(self, text="Connect", command= lambda conn_version ='\x5C\x66\x32\x01': self.connect(conn_version)).grid(column=4, row=1)
        Label(self, text='').grid(column=0, row=5)   
        #scroll bar of the text widget
        self.scroll_y =Scrollbar(self,orient=VERTICAL)
        self.scroll_x =Scrollbar(self,orient=HORIZONTAL)
        #text widget
        self.receive=Text(self,wrap=WORD)
        self.scroll_y.config(command = self.receive.yview)
        self.scroll_x.config(command = self.receive.xview)
        self.receive.config(yscrollcommand = self.scroll_y.set,xscrollcommand = self.scroll_x.set)
        self.receive.grid(column=1, row=6, columnspan=4,rowspan=5)
        self.scroll_y.grid(column=6, row=6,rowspan=5, sticky=S+N)
        self.scroll_x.grid(column=1, row=8, columnspan=4,sticky=W+E)
        
        self.servername=Entry(self,bg="#BBBBFF",width=25)
        try:
            self.f_server=open("servername.txt","r")
            self.servername.insert(0,self.f_server.read().replace(' ','_').replace('\n','').replace('\r',''))
            self.f_ver.close()
        except:            
            self.servername.insert(0,"Name of your server")
        self.servername.grid(column=0, row=6, sticky=N+E)
        #---listbox widget to print the players
        self.players = Listbox(self,bg="#CCCCCC", font=("Helvetica", 8), height=20, width=26)
        self.players.insert(END, "Players: ")
        self.players.grid(column=0, row=7, sticky=N+E)
        self.label_automess= StringVar('')
        self.label_autoserver= StringVar('')
        self.label_automap= StringVar('')
        Label(self, textvariable=self.label_automess).grid(column=0,row=8, sticky=N+W)
        Label(self, textvariable=self.label_autoserver).grid(column=0,row=9, sticky=N+W)
        Label(self, textvariable=self.label_automap).grid(column=0,row=10, sticky=N+W)
        self.label_automess.set("automess off")
        self.label_autoserver.set("autoserver off")
        self.label_automap.set("automap off")
        self.mess = Entry(self,width=107)
        self.mess.config(bg="#FFEEFF",fg="#0000FF") 
        self.mess.grid(column=1, row=12,columnspan=4)
        self.mess.bind("<Return>", self.sendmess)
        #for a text widget
##        self.mess=Text(self.f2,wrap=NONE,height=3)
##        self.mess.grid(column=0, row=9)
##        self.mess.bind("<Control_L>", self.sendmess)

            
        #---get the ys_username            
        try:
            ysfuser=open(self.path+"/config/network.cfg",'r')            
            while 1:
                self.ysusername=ysfuser.readline()
                if self.ysusername=="":
                    break
                if self.ysusername.find("DEFAULTUSR")!=-1:
                    self.ysusername=self.ysusername[11:]
                    self.ysusername=self.ysusername.replace('"','')
                    self.ysusername=self.ysusername.replace('\n','')
                    self.ysusername=self.ysusername.replace('\r','')
                    print "default username: "+self.ysusername
                    break
            ysfuser.close()
        except:
            print 'Impossible to find the file config/network.cfg or to read it!'
            tkMessageBox.showerror('YS_chat', 'Impossible to find the file config/network.cfg or to read it!')      
            self.ysusername="Your username"
        self.username_real=self.ysusername
        self.ip.selectitem(self.ip_list[0])
        self.username.insert(0,self.ysusername)
        
        if "-random" in sys.argv:
            print "args"
            print "ip"+sys.argv[2]
            self.autoip=sys.argv[2]
            self.canreconnect=1
            self.connect("\x5C\x66\x32\x01")
            try:
                self.AutoReconnect=Reconnect(self.mess,self.c,1)
                self.AutoReconnect.start()
            except:
                print "cannot stop the auto reconnect"
        
        if "-connect" in sys.argv:
            print "args"
            print "ip"+sys.argv[2]
            self.autoip=sys.argv[2]
            self.canreconnect=1
            self.connect("\x5C\x66\x32\x01")
            try:
                self.AutoReconnect=Reconnect(self.mess,self.c,1)
                self.AutoReconnect.start()
            except:
                print "cannot stop the auto reconnect"
        
        """HOST="irc.freenode.net"
        PORT=6667
        NICK="yschat"
        for i in random.sample('1234567890',2):
            NICK+=i
        IDENT=NICK
        self.CHANNEL = "#ysflight"
        REALNAME="Eric"
        self.server=socket()
        self.server.connect((HOST,PORT))
        self.server.send("NICK %s\r\n" % NICK)
        self.server.send("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))
        self.server.send('JOIN ' + self.CHANNEL + '\r\n')
        self.server.send('PRIVMSG '+self.CHANNEL+' :YSChat connected from erict15\'s server (et15.ath.cx)\r\n')"""
        
    def about(self):
        "about dialog (help menu)"
        tkMessageBox.showinfo("About YSChat", "YSChat version "+str(yscversion)+" by VincentWeb\nModded by erict15")

    def aduration(self,dic_player):
        self.duration = 0
        try:
            if dic_users[dic_player]!="":
                self.dic_aircraft=dic_users[dic_player][:dic_users[dic_player].find('|)-(|')]
                self.dic_start=float(dic_users[dic_player][dic_users[dic_player].find('|)-(|')+5:])
                self.dic_end=time()
                dic_users[dic_player]=""
                self.duration=self.dic_end-self.dic_start
                dic_player=dic_player.replace('[','(').replace(']',')').replace('.','').replace(' ','')
                if self.ysc_mode=="SERVER":
                    if dic_player[0:1]!="@":
                        #st=ThreadURL("http://marcjeanmougin.free.fr/ys_servers/add_duration.php?server=erict15s_server&username=erict15&aircraft="+self.dic_aircraft+"&duration="+str(self.duration))
                        st=ThreadURL("http://marcjeanmougin.free.fr/ys_servers/add_duration.php?server="+self.servername.get().replace(' ','_')+"&username="+dic_player+"&aircraft="+self.dic_aircraft+"&duration="+str(self.duration))
                        st.start()
                        #p=urllib.urlopen("http://marcjeanmougin.free.fr/ys_servers/add_duration.php?server="+self.servername.get().replace(' ','')+"&username="+dic_player+"&aircraft="+self.dic_aircraft+"&duration="+str(self.duration))
                        
                        #print p.read()                        
                        
                        #p_end=p.read()[-2:]
                        
##                        if p_end!="ok":
##                            self.receive.insert(END,">>> Cannot save "+dic_player+" flight duration: server answered: 'wrong' -> already sent, or cannot delete the key, or problem\n")
##                        elif p_end=="no":
##                            self.receive.insert(END,">>> Cannot save "+dic_player+" flight duration: server answered: 'already sent'\n")
        except:
            print "PB DURATION"
            st=ThreadURL("http://marcjeanmougin.free.fr/ys_servers/add_duration.php?server="+self.servername.get().replace(' ','_')+"&username="+dic_player+"&aircraft=unknown&duration="+str(time()-self.connect_time))
            st.start()
            #p=urllib.urlopen("http://marcjeanmougin.free.fr/ys_servers/add_duration.php?server="+self.servername.get().replace(' ','')+"&username="+dic_player+"&aircraft=unknown&duration="+str(time()-self.connect_time))                        
            self.receive.insert(END,">>> Unknown "+dic_player+" flight duration: not in the dico, flight duration maybe saved with unknown aircraft\n")


    def connect(self,conn_version):
        self.ysc_mode=""
        fver=open("ver.txt",'w')
        fver.write(self.versionbox.get())
        fver.close()
        fserver=open("servername.txt",'w')
        fserver.write(self.servername.get())
        fserver.close()
        try:
            conn_version=hex(int(self.versionbox.get()))
        except:
            print "pb"
            tkMessageBox.showerror('YS_chat', 'YOU MUST PUT IN THE VERSION BOX AN INTEGER (a number)')            
        else:
            conn_version=chr(int(conn_version[len(conn_version)-2:len(conn_version)],16))+chr(int(conn_version[len(conn_version)-4:len(conn_version)-2],16))+chr(int(conn_version[len(conn_version)-6:len(conn_version)-4],16))+chr(int(conn_version[2:len(conn_version)-6]))
            #adebug(conn_version)
            self.conn_time+=1
            self.autodetect=1
            print "version using"
            for n in conn_version:
                print ord(n)
            "to connect a server"
            try:
                self.ip_list.index(self.ip.get())
            except:
                try:
                    print "insert the ip"
                    ysfip=open(self.path+"/config/serverhistory.txt",'a')
                    ysfip.write(self.ip.get()+'\n\r')
                    ysfip.close()
                except:
                    print "cannot do it"
            
            if self.canreconnect==0:
                print 'update'+self.th_version.shallupdate
                if self.th_version.shallupdate=='must':
                    tkMessageBox.showerror('YS_chat', 'The current update of YSChat is mandatory to use it. Probably a security problem.')              
                    sys.exit()
                elif self.th_version.shallupdate=='yes':
                    self.receive.insert(END,'There is a new version of YSChat \n')
            if self.connected!=1:
                self.c=socket()            
                try:
                    if self.autoip=="":
                        self.c.connect((self.ip.get(),int(self.port.get())))
                        myip=self.ip.get()
                        print "simple connect"
                    else:
                        print "autoconnect"
                        if self.autoip.find(":")==-1:
                            self.c.connect((self.autoip,int(self.port.get())))
                            myip=self.autoip
                        else:
                            self.c.connect((self.autoip[0:self.autoip.find(":")],int(self.autoip[self.autoip.find(":")+1:])))
                            print self.autoip[0:self.autoip.find(":")]+self.autoip[self.autoip.find(":")+1:]
                            myip=self.autoip[0:self.autoip.find(":")]
                except:
                    try:
                        print "failed to connect"
                        if self.autoserver==1:
                            thistime=time()
                            print self.time
                            print thistime
                            if abs(thistime - self.time)>600:
                                print 'restart the server2'                                
                                try:
                                    self.StartServer._Thread__stop()
                                except:
                                    print "cannot stop the thread-server2"
                                try:
                                    os.chdir(self.path)
                                    self.StartServer=LaunchServer(self.username_real,self.ys_exec)
                                    self.StartServer.start()
                                except:
                                    print "cannot start the server-thread2"
                            else:
                                print 'too long2'
                        else:
                            print 'not allowed to restart the server2'
                        self.time=time()
                        print self.time
                        print thistime
                    except:
                        print "still cannot restart the server"
                    
                    if self.canreconnect==0:  
                        tkMessageBox.showerror('YS_chat', 'Impossible to connect the server !')              
                else:
                    #we are connected
                    self.connect_time=time()
                    print "connecting"
                    self.time=time()
                    
                    try:
                        self.AutoReconnect.stop()
                    except:
                        print "cannot stop autoreconnect"
                    try:
                        self.th_version.stop()
                        print "stop the check version"
                    except:
                        print "cannot stop the checkversion thread"
                        
                    if myip=="127.0.0.1":    
                        self.ysc_mode="SERVER"
                        self.ysc_char="~"
                    #---get the ips
                    self.ip_info=getaddrinfo(gethostname(), None)
                    self.ips=[]
                    print myip
                    for nb in self.ip_info:
                        self.ips.append(nb[4][0])
                        if myip==nb[4][0]:
                            self.ysc_mode="SERVER" 
                            self.ysc_char="~"
                            
                    if self.ysc_mode!="SERVER":
                        self.ysc_mode="CLIENT, use the ip 127.0.0.1 to be in server mode"
                        self.ysc_char="*"
                        
                    #self.username_real=self.ysc_char+self.username.get()
                    username=self.username.get()
                    username=username.strip('()')
                    username='\x18\x00\x00\x00\x01\x00\x00\x00'+username+"\x00"*(15-len(username))+'\x00'+conn_version
                    self.c.send(username)
                    self.f=open('logfile'+strftime("%Y%m%d",localtime())+'.htm','a')
                    #self.f=open('chat.txt','a')
                    self.f.write('\r\n<br><font color="#FF0000"><em> Connection on :'+self.ip.get()+":"+self.port.get()+" the "+strftime("(%a, %d %b %Y) [%H:%M:%S]", localtime())+" with the username "+self.username.get()+'</em></font>\r\n<br>')
                    print "the log of the conversation will be registered in "+str(os.getcwd())
                    self.f.flush()
                    
                    mess1=self.c.recv(1024)
                    #print "adebug"
                    #print adebug(mess1)
                    if mess1.find("\x08\x00\x00\x00\x1d\x00\x00\x00")==-1:
                        print "pb"                 
                        mess1=self.c.recv(1024)
                        #print adebug(mess1)
                    conn_version=mess1[8:12]
                    print "version found"
                    for n in conn_version:
                        print ord(n)
                    print len(mess1)
                    #sleep(6)
                    if len(mess1)>100000 and self.conn_time<2:
                        print "wrong version"
                        self.receive.insert(END,">>> WRONG VERSION \n")
                        print conn_version
                        self.autodetect=0
                        #self.c.close()
                        self.receive.insert(END,">>> You might disconnect, if the client cannot communicate with the server. \n")
                        if len(conn_version)>3:
                            self.connect(conn_version)
                        
                    else:
                        self.connected=1
                        messem="\x0c\x00\x00\x00\x06\x00\x00\x00\x09\x00\x00\x00\x00\x00\x00\x00\x0c\x00\x00\x00\x06\x00\x00\x00\x0a\x00\x00\x00\x00\x00\x00\x00\x0c\x00\x00\x00\x06\x00\x00\x00\x0b\x00\x00\x00\x00\x00\x00\x00"+mess1[mess1.find("\x1a"):]
                        
                        print "first answer"
                        #adebug(messem)
                        #sleep(4)
                        #self.c.send(messem)
                        #why is it here ?
                        #self.c.send("\x08\x00\x00\x00\x26\x00\x00\x00\x00\x00\x00\x00")
                        
                        #---Get the map
                        if mess1.find('\x40\x00\x00\x00\x04\x00\x00\x00')!=-1:
                            self.map=mess1[mess1.find('\x40\x00\x00\x00\x04\x00\x00\x00')+8:]
                            pos=self.map.find('\x00')
                            self.map=self.map[0:pos]                    
                            lab=Label(self, text='map: ' + self.map)
                            lab.grid(column=1, row=5)
                        # Message to send to get the players
                        self.c.send('\x04\x00\x00\x00\x25\x00\x00\x00')                
                        #load the colors
                        os.chdir(self.folder)
                        load_colors()
                        dic_user={}                
                        #---start the threads
                        self.th_R = ThreadReception(self.c,self.receive,self.f,self.players)
                        #th_E = ThreadEmission(c)
                        self.th_R.start()
                        try:
                            self.receive.tag_config("ysc_mess",background=colors['ys_chat_mess','bg'], foreground=colors['ys_chat_mess','fg'],font=colors['ys_chat_mess','font'])
                        except:
                            print "bad color"
                        self.receive.insert(END,"***You are connected***\n",'ysc_mess')
                        self.canreconnect=0
                        self.receive.insert(END,">>>"+self.ysc_mode+"\n")
                        name=self.username.get()
                        name=name.strip('()')
                        self.username.delete(0, END)
                        self.username.insert(0, "("+name+")")
                        self.thread30s=SendMess30s(self.c)
                        self.thread30s.start()
                        #self.ircserver=IRC(self.c,self.server)
                        #self.ircserver.start()
                    
            #else:
            #    print "you cannot connect twice"
            #    tkMessageBox.showerror('YS_chat', 'You cannot connect twice, enter "/quit" to disconnect !')              
            
    def exit_ysc(self):
        "exit the program"
        print "exiting"
        self.exit=1
        self.canreconnect=0
        if self.connected==1:
            print "try to disconnect"
            self.disconnect2()
        try:
            self.th_version.stop()
            print "stop the check version"
        except:
            print "cannot stop the checkversion thread"
##        try:
##            self.AutoReconnect.stop()
##            print "stopped the auto reconnect thread"
##        except:
##            print "cannot stop the auto reconnect thread"
        try:
            self.AutoReconnect._Thread__stop()
            print "stop the autoreconnect"
        except:
            print "cannot stop the auto reconnect"
        try:
                self.thread30s.stop()
        except:
                print("cannot stop the 30s thread")

        
        
        print "exit"
        sys.exit()
        
    def disconnect2(self):
        #disconnect without retrying to restart
        self.conn_time=0
        self.canreconnect=0
        "disconnect a server"
        for nb in dic_users:
            self.aduration(nb)
        try:
            self.th_R.stop()
        except:
            print 'cannot stop the reception thread'
        try:
            self.th_R._Thread__stop()
        except:
            print "problem to stop it"
        try:
            self.c.close()
        except:
            print 'cannot close the log file'
        self.connected=0
        try:
            self.thread30s.stop()
        except:
            print("cannot stop the 30s thread")
        """try:
            self.IRC.stop()
        except:
            print "cannot stop the IRC thread"""

        if self.exit==0:
            try:
                self.Sendauto.stop()
                self.sendauto=0
            except:
                print "cannot stop the auto thread"
        time=1
    
    def disconnect(self):
        for nb in dic_users:
            self.aduration(nb)
        self.conn_time=0
        "disconnect a server"
        try:
            self.th_R.stop()
        except:
            print 'cannot stop the reception thread'
        try:
            self.c.close()
        except:
            print 'cannot close the log file'
        self.connected=0
        try:
                self.thread30s.stop()
        except:
                print("cannot stop the 30s thread")

##        if self.exit==0:
##            try:
##                self.Sendauto.stop()
##                self.sendauto=0
##            except:
##                print "cannot stop the auto thread"
        time=1
        print "will auto reconnect"
        if self.canreconnect==1:
            try:
##                self.AutoReconnect._Thread__stop()
                self.AutoReconnect=Reconnect(self.mess,self.c,time)
                self.AutoReconnect.start()
            except:
                print "cannot stop the auto reconnect"
        
    
    def help(self):
        "help dialog (help menu)"
        webbrowser.open("http://www.yspilots.com/shadowhunters/yschat/doc_yschat.pdf")
    
    def insert(self,text):
        "add a text/command to the entry widget"
        pos=len(self.mess.get())
        self.mess.insert(INSERT,text)
        
    def return_username(self):
        return self.username.get()

    def sendmess(self,event,message=0):
        #print(str(time()))	
        if message==0:
            message=self.mess.get() #1.0, END
        else :
            message=message
            if self.ysc_mode!="SERVER":
                message=message[0:255]
        #message=message.encode("Latin-1")#to encode the string we send (if there are special chars)
        message=message.replace('$mynick ',self.username.get())
        message=message.replace('$me ',self.username_real)
        message=message.replace('$gmtime ',strftime("%H:%M:%S +0000", gmtime()))
        message=message.replace('$datetime ',strftime("%a, %d %b %Y %H:%M:%S", localtime()))
        message=message.replace('$daylight ',str(daylight))
        message=message.replace('$timezone ',str(timezone))
        message=message.replace('$time ',strftime("%H:%M:%S", localtime()))
        #message=message.replace("-ping","-ping "+str(time()))
        try:
            message=message.replace('$map',self.map)
        except:
            message=message.replace('$map','no map : (not connected)')
        
        fin=len(self.mess.get()) #1.0, END
        if event!='eventauto' and event!='eventmap' and event!='eventlist':
            self.mess.delete(0,fin) #1.0, END
        if self.ysc_mode=="SERVER":
            messaget=message.split('|')
        else:
            messaget=[]
            messaget.append(message)
        if event!='eventauto' and event!='eventmap' and event!='eventlist':
            maxlength=92-len(self.username.get()) #112(max length of the packet) - '(*' - username - ')'  - 1(/x00) - 6(protection)   
        else:
            maxlength=92
        a=0
        for message in messaget:
            if len(message)>maxlength and message.find('/com')==-1 and message.find('/listusers')==-1: 
                print 'cut'
                messaget.insert(a+1,message[maxlength:])
                message=message[0:maxlength]
            if self.connected==1:
                if message.find("/quit")!=-1:
                    self.disconnect2()
                elif message.find("/exit")!=-1:
                    self.disconnect2()
                    sys.exit()
                #--- launchserver
                elif message.find('/launchserver')!=-1:
                    try:
                        servernick=self.username.get()
                        servernick=servernick.replace(' ','')                        
                        pos=message.find('/launchserver')
                        if len(message)==pos+13:
                            self.ys_exec="fsmain.exe"
                        else:                                
                            self.ys_exec=message[pos+14:]
                        print self.ys_exec
                        os.chdir(self.path)
                    except:
                        print "problem to launch the server"
                    try:
                        self.StartServer=LaunchServer(servernick,self.ys_exec)
                        self.StartServer.start()
                    except:
                        print "cannot start the server-thread"
                #elif message.find("-ping")!=-1:
                    #try:
                        #self.pingStart=time()
                    #except:
                        #print "cannot ping"
                elif message.find('/ysfs')!=-1:
                    try:
                        oldpath=os.getcwd()
                        os.chdir(self.path)
                        os.system("fsmain.exe -client "+self.username.get().replace(' ','')+' '+self.ip.get())
                        os.chdir(oldpath)
                    except:
                        print "cannot do it"
                    
                elif message.find("/clear")!=-1:
                    self.receive.delete(1.0, END)
                
                elif message.find("/autoserver")!=-1:
                    if self.ysc_mode=="SERVER":
                        pos=message.find('/autoserver')
                        if len(message)==pos+11:
                            self.ys_exec="fsmain.exe"
                        else:                                
                            self.ys_exec=message[pos+12:]
                        print self.ys_exec
                        self.label_autoserver.set("autoserver on ")
                        print "auto server"
                        self.autoserver=1
                        self.receive.insert(END,">>> Autoserver on: will restart the server if I see a reset message, and autoclose the old server if it's me who launched it\n")
                    else:
                        tkMessageBox.showerror('YS_chat', 'You can only use this command on SERVER mode \n (only if you connect your server with the ip 127.0.0.1)')
                    
                elif message.find("/automap")!=-1:
                    if self.ysc_mode=="SERVER":
                        print "auto map"
                        self.automap=1
                        self.label_automap.set("automap on ")
                        self.receive.insert(END,">>> Automap on: allow to chose a random map after 30min and allow the command /changemap NameOfMap\n")
                    else:
                        tkMessageBox.showerror('YS_chat', 'You can only use this command on SERVER mode \n (only if you connect your server with the ip 127.0.0.1)')
                    
                elif message.find("/stopautoserver")!=-1:
                    print "stop auto server"
                    self.label_autoserver.set("autoserver off")
                    self.autoserver=0
                    self.receive.insert(END,">>> Autoserver off\n")
                    
                elif message.find("/stopautomap")!=-1:
                    print "stop auto map"
                    self.label_automap.set("automap off")
                    self.automap=0    
                    self.receive.insert(END,">>> Automap off\n")
                
                elif message.find("/auto")!=-1:
                    if self.ysc_mode=="SERVER":
                        self.label_automess.set("automess on ")
                        if self.sendauto!=1:
                            try:
                                time=float(message[message.find("<")+1:message.find(">")])
                            except:
                                print "ERROR with the time in auto-message"
                            if time <1:
                                time=1
                            message=message[message.find(">")+1:]
                            print "automated message running: " + message + " every " + str(time) + "minutes"       
                            self.sendauto=1
                            self.Sendauto=ThreadSendautomated(self.mess,message,time)
                            self.Sendauto.start()
                        else:
                            print "you can schedule only 1 automessage"
                            tkMessageBox.showerror('YS_chat', 'You can schedule only 1 auto message !')              
                    else:
                        tkMessageBox.showerror('YS_chat', 'You can only use this command on SERVER mode \n (only if you connect your server with the ip 127.0.0.1)')
                        
                elif message.find("/stopauto")!=-1:
                    try:
                        self.label_automess.set("automess off")
                        self.Sendauto.stop()
                        self.sendauto=0
                    except:
                        print "cannot stop the auto thread"
                    
                elif message=='/list':
                    self.c.send('\x04\x00\x00\x00\x25\x00\x00\x00')
                    
                elif message.find('/loadcolours')!=-1:
                    print "loading the colors"
                    self.receive.insert(END,">>> colors loaded\n")
                    load_colors()  
                
                elif message.find('/refreshlog')!=-1:
                    self.f.flush()
                    self.receive.insert(END,">>> log refreshed\n")
                    
                elif message.find('/kill ')!=-1:
                    message=message.strip(' ')
                    id2=message[message.find('/kill ')+6:]
                    #strength=int(16777215) #struct.pack('<I', strength)
                    try:
                        id=int(id2)
                        messaget=struct.pack('<I', id)
                        messaget='\x18\x00\x00\x00\x16\x00\x00\x00\x01\x00\x00\x00'+messaget+'\x01\x00\x00\x00\x01\x00\x01\x00\xFF\x7F\x0B\x00'
                        self.c.send(messaget)
                        print "kill signal sent to ID: "+id2
                    except:
                        try:
                            #print ids
                            messaget=struct.pack('<I', ids[id2])
                            messaget='\x18\x00\x00\x00\x16\x00\x00\x00\x01\x00\x00\x00'+messaget+'\x01\x00\x00\x00\x01\x00\x01\x00\xFF\x7F\x0B\x00'
                            self.c.send(messaget)
                            print "kill signal sent to user: "+id2
                        except:
                            print 'username \"'+id2+'\" not found'
                    try:
                        self.receive.tag_config("mess",background=colors['default_mess','bg'], foreground=colors['default_mess','fg'],font=colors['default_mess','font'])
                    except:
                        print "bad color"
                    self.receive.insert(END,self.username.get()+message+'\n','mess')

                elif message.find('/com')!=-1:
                    message=message.replace('/com','')
                    message=message.strip(' ')
                    messaget=message.split()
                    message=""
                    for nb in messaget:
                        message=message+chr(int(nb,16))
##                    regex = re.compile(r'\\x([a-f0-9]){2}', re.I)
##                    message = regex.sub(lambda o: chr(int(o.group(1), 16)), message)
                    self.c.send(message)

                else:
                    message=message.replace('\\n','\x0A')
                    if event!='eventauto' and event!='eventmap' and event!='eventlist':
                        message_emis="\x6c\x00\x00\x00\x20\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"+self.username.get()+message
                    else:
                        message_emis="\x6c\x00\x00\x00\x20\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"+message
                    message_emis+='\x00'*(112-len(message_emis))
                    self.c.send(message_emis)
            else:            
                if message.find("/exit")!=-1:
                    sys.exit()
                elif message.find("/clear")!=-1:
                        self.receive.delete(0,fin)#1.0, END for text widget
                #--- launch server thread        
                elif message.find('/launchserver')!=-1:
                    try:
                        servernick=self.username.get()
                        servernick=servernick.replace(' ','')                        
                        pos=message.find('/launchserver')
                        if len(message)==pos+13:
                            self.ys_exec="fsmain.exe"
                        else:                                
                            self.ys_exec=message[pos+14:]
                        print self.ys_exec
                        os.chdir(self.path)
                    except:
                        print "problem to launch the server"
                    try:
                        self.StartServer=LaunchServer(servernick,self.ys_exec)
                        self.StartServer.start()
                    except:
                        print "cannot start the server-thread"
                else:
                    if tkMessageBox.askyesno("YSChat", "You must be connected to send a message. Shall I connect ?")==True:
                        self.connect("\x5C\x66\x32\x01")
            a+=1
            
    def useversion(self):
        useversion = self.version.get()
        if useversion=="":
            useversion='20080220'
        print useversion
        return useversion

def load_colors():
    global colors
    colors={}
    fc=open('ysc_colors.txt')
    while 1:
        line=fc.readline()
        if line=="":
            break
        else:
            try:
                bg=line[line.find('<bg>')+4:line.find('</bg>')].strip()
                fg=line[line.find('<fg>')+4:line.find('</fg>')].strip()
                font=line[line.find('<font>')+6:line.find('</font>')].strip()
                font_t=font.split()
                colors[(line[0:12],'bg')]=bg
                colors[(line[0:12],'fg')]=fg
                if len(font_t)==3:
                    colors[(line[0:12],'font')]=(font_t[0].replace('_',' '),int(font_t[1]),font_t[2].replace('_',' '))
                if len(font_t)==2:
                    colors[(line[0:12],'font')]=(font_t[0].replace('_',' '),int(font_t[1]))
                if len(font_t)==1:
                    colors[(line[0:12],'font')]=font_t[0].replace('_',' ')
                if len(font_t)==0:
                    colors[(line[0:12],'font')]=''
            except:
                print "cannot read the ysc_colors.txt file for " + line[0:12]



def adebug(var):    
    global debug
    debug=var
    debug=debug.replace('\x01','-01-')
    debug=debug.replace('\x02','-02-')
    debug=debug.replace('\x03','-03-')
    debug=debug.replace('\x04','-04-')
    debug=debug.replace('\x05','-05-')
    debug=debug.replace('\x06','-06-')
    debug=debug.replace('\x07','-07-')
    debug=debug.replace('\x08','-08-')
    debug=debug.replace('\x09','-09-')
    debug=debug.replace('\x10','-10-')
    debug=debug.replace('\x11','-11-')
    debug=debug.replace('\x12','-12-')
    debug=debug.replace('\x13','-13-')
    debug=debug.replace('\x14','-14-')
    debug=debug.replace('\x15','-15-')
    debug=debug.replace('\x16','-16-')
    debug=debug.replace('\x17','-17-')
    debug=debug.replace('\x18','-18-')
    debug=debug.replace('\x19','-19-')
    debug=debug.replace('\x20','-20-')
    debug=debug.replace('\x0A','-0A-')
    debug=debug.replace('\x0B','-0B-')
    debug=debug.replace('\x0C','-0C-')
    debug=debug.replace('\x0D','-0D-')
    debug=debug.replace('\x0E','-0E-')
    debug=debug.replace('\x0F','-0F-')
    debug=debug.replace('\x1A','-1A-')
    debug=debug.replace('\x1B','-1B-')
    debug=debug.replace('\x1C','-1C-')
    debug=debug.replace('\x1D','-1D-')
    debug=debug.replace('\x1E','-1E-')
    debug=debug.replace('\x1F','-1F-')
    debug=debug.replace('\x80','-80-')
    debug=debug.replace('\x8c','-8c-')
    print "start debug"
    print debug.replace('\x00','.')
    print "end debug"
    return debug

class ThreadCheckversion(threading.Thread):
    """thread to check the last version"""
    def __init__(self):
        threading.Thread.__init__(self)
        self.shallupdate=""
    def run(self):
        self.running = True
        if self.running:
            try:
                p=urllib.urlopen('http://www.yspilots.com/shadowhunters/yschat/yscversion.txt')
            except:
                print "cannot check the version"
                  #break
            else:
                lastversion=p.read()
                try:
                    lastyscversion=float(lastversion[1:])
                except:
                    print "cannot read the version"
                    #break
                else:
                    if lastyscversion>float(yscversion):
                        if lastversion[0:1]=='!':
                            print "you cannot use this version, you should update it"
                            self.shallupdate='must'
                            
                            #break         
                        else:
                            print "there is a new version"
                            self.shallupdate='yes'
                            
                            
                    else:
                        print "no new version"
                        self.shallupdate='no'
            #break
            self.running=False
##        if thever==1:
##             
##        elif thever==2:
##            tkMessageBox.showinfo('YSChat', 'There is a new version of YSChat')              
                
            
    def stop(self):
        self.running = False 

class SendMess30s(threading.Thread):
    """thread which send the messages"""
    def __init__(self, conn):
        threading.Thread.__init__(self)
        #self.c = conn            # ref. du socket de connexion
        self.c = conn
        self.running = threading.Event( )
        #print "30s thread auto mess"
    def run(self):
        
        while not self.running.isSet(): 
            self.running.wait(30)
            try:          
                self.c.send("\x04\x00\x00\x00\x11\x00\x00\x00")
                #print("30s")
            except:
                print "disconnected ?"
            
    
    def stop(self):
        self.running.set( )
        
"""class IRC(threading.Thread):
    def __init__(self, conn, serv):
        threading.Thread.__init__(self)
        self.c = conn
        self.server = serv
        self.prev=''
        self.running = threading.Event( )
    
    def run(self):
        while not self.running.isSet():
            try:
                data=self.server.recv(2048)
                #print data
                if data.find('PING')!=-1:
                    self.server.send('PONG'+data.split()[1]+'\r\n')
                elif data.find('PRIVMSG')!=-1:
                    nick=data.split('!')[0].replace(':','')
                    message=':'.join(data.split(':')[2:]).replace('\n','')
                    if nick.find('yschat')==-1 and nick.find('frigg')==-1:
                        mess="("+nick+")"+message
                        line_emis="\x6c\x00\x00\x00\x20\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"+mess
                        if len(mess)<92:
                            line_emis+='\x00'*(112-len(line_emis))
                        elif len(mess)>92:
                            line_emis="\x6c\x00\x00\x00\x20\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"+mess[0:91]
                        try:
                            self.c.send(line_emis)
                        except:
                            print "disconnected from ys server?"
                    elif nick.find('yschat')!=-1:
                        if self.prev!=message:
                            self.prev=message
                            line_emis="\x6c\x00\x00\x00\x20\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"+message
                            if len(message)<92:
                                line_emis+='\x00'*(112-len(line_emis))
                            elif len(message)>92:
                                line_emis="\x6c\x00\x00\x00\x20\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"+message[0:91]
                            try:
                                self.c.send(line_emis)
                            except:
                                print "disconnected from ys server?"
            except:
                print "disconnected from IRC server?"
    def stop(self):
        self.running.set( )
"""
class ThreadSendautomated(threading.Thread):
    """thread which send the messages"""
    def __init__(self, entry_mess,message,time):
        threading.Thread.__init__(self)
        #self.c = conn            # ref. du socket de connexion
        self.entry_mess=entry_mess
        self.appli=entry_mess.master
        self.message="*"+message+"*"
        self.time=time
        self.running = threading.Event( )
        print "automated message running"
    def run(self):
        
        while not self.running.isSet(): 
            try:          
                self.appli.sendmess('eventauto',self.message)
            except:
                print "disconnected ?"
            self.running.wait(self.time*60)
    
    def stop(self):
        self.running.set( )

class Reconnect(threading.Thread):
    """thread which send the messages"""
    def __init__(self, entry_mess, conn, time):
        threading.Thread.__init__(self)
        self.c = conn            # ref. du socket de connexion
        self.time=time
        self.appli=entry_mess.master
        print "auto reconnect"
        self.running = threading.Event( )
    def run(self):
        if self.appli.canreconnect==1:
            while not self.running.isSet():   
                print "trying to reconnect this time"
                try:
                    self.appli.connect("\x5C\x66\x32\x01")
                except:
                    print "problem in auto_reconnect_thread"
                self.running.wait(self.time*60)
    def stop(self):
        self.running.set( )


class ThreadURL(threading.Thread):
    """object thread for the reception of the messages, print the players"""
    def __init__(self,url):
        threading.Thread.__init__(self)
        self.url=url
    def run(self):        
        try:
            p=urllib.urlopen(self.url)
            if p.read()[-2:]!="ok":
                print "FLIGHT DURATION NOT SAVED"
                print p.read()
            else:
                print "ok"
        except:
            print "cannot do it"

class ThreadReception(threading.Thread):
    """object thread for the reception of the messages, print the players"""
    def __init__(self, conn,text,f,players):
        threading.Thread.__init__(self)
        self.connexion = conn            # ref. du socket de connexion
        self.text=text
        self.f=f
        self.players=players
        self.t1=0
        self.appli=text.master
        
    def run(self):
        players=[]
        global ids
        ids={}
        try:
            map=self.appli.map
        except:
            map="unknown"
        self.running = True
        self.appli.time=time()
        while self.running:
            #print(strftime("%H:%M:%S", localtime()))
            if int(strftime("%M", localtime()))%2==0 and self.t1!=strftime("%M", localtime()):
                try:
                    self.t1=strftime("%M", localtime())
                    self.connexion.send('\x04\x00\x00\x00\x25\x00\x00\x00')
                    #print "update the player list"
                except:
                    print "pb to upload the player list"
            try:   
                mess = self.connexion.recv(2048)
            except:
                self.appli.canreconnect=1
                self.appli.disconnect()
                print "auto reconnect soon2"
                break
            if mess =='':
                self.appli.canreconnect=1
                self.appli.disconnect()
                print "auto reconnect soon"
                break
            #adebug(mess)
            m1=""
            for n in mess:
                m1=m1 + ' ' + str(ord(n))
            #print m1
            if mess.find("\x00\x00\x2c\x00\x00\x00\x01")!=-1:
                messem=mess[mess.find("\x00\x00\x2c\x00\x00\x00\x01")-2:]
                #adebug(messem)
                self.connexion.send(messem)
                #print "sending data"
            
            #--- read the player list
            if mess.find('\x00\x00\x25\x00\x00\x00')!=-1:
                players=[]
                ids={}
                self.players.delete(0,END)
                self.players.insert(END, "Players: ")
                players2=""
                while mess.find('\x00\x00\x25\x00\x00\x00')!=-1:
                    pos = mess.find('\x00\x00\x25\x00\x00\x00') + 2
                    packet_size = struct.unpack('I', mess[pos-4:pos])[0]
                    player = mess[pos:packet_size+pos]
                    mess = mess[packet_size+pos:]

                    status=struct.unpack('H', player[4:6])[0]
                    iff=struct.unpack('H', player[6:8])[0]
                    id=struct.unpack('I', player[8:12])[0]
                    username=player[16:]
                    username=username[:username.find('\x00')]
                    if status == 1:
                        #flying, regular user
                        players2='['+str(id)+'] '+username+' (IFF='+str(iff)+')'
                        ids[username]=id
##                        if iff==1:
##                            messaget=struct.pack('<I', id)
##                            messaget='\x18\x00\x00\x00\x16\x00\x00\x00\x01\x00\x00\x00'+messaget+'\x01\x00\x00\x00\x01\x00\x01\x00\xFF\x7F\x0B\x00'
##                            self.appli.c.send(messaget)
##                            print "kill signal sent to user: "+username
##                            self.appli.sendmess('eventlist','(YSChat)get on IFF 1 '+username)
                    elif status == 2:
                        #not flying, server
                        players2='[****] '+username+' (SERVER)'
                    elif status == 3:
                        #flying, server
                        players2='['+str(id)+'] '+username+' (IFF='+str(iff)+') (SERVER)'
                        ids[username]=id
                    else:
                        #not flying, regular user
                        players2='[****] '+username+' (IFF=*)'            
                    players.append(players2)
                    self.players.insert(END,players2)
                    #print players2

##                for player in messt:
##                    if a!=0 and len(player)<50 and player.find('')==-1:
##                        playert=player.split()                        
##                        try:
##                            if player.find('(-!-)')!=-1:
##                                c=0
##                                player=player[5:]                                
##                                player=player.replace('($)',' ')
##                                player=player.replace('(-!-)','')
##                                #print player[1:] + ' is flying'
##                                self.players.insert(END,'(F) '+player[1:])
##                                players.append('(F) '+player[1:])
##                                players2=players2+player[1:]
##                            else:
##                                player=playert[0]
##                                player=player.replace('($)',' ')
##                                #print player + ' is not flying'
##                                players.append(player)
##                                players2=players2+player
##                                self.players.insert(END,player )
##                        except:
##                            print "BAD ERROR WHILE UPDATING THE PLAYER LIST"
##                    a+=1
                #for nb in dic_users:
                    #if players2.find(nb)==-1:
                        #print "not found "+nb
                        #self.appli.aduration(nb)
            #--- took-off message ?? or chat message
            is_mess=mess.find('\x00\x00\x00\x20\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
            while is_mess!=-1:
                mess3=""
                if is_mess!=-1:      #could be a problem
                     #print "took off message ???"
                     mess2=mess[is_mess+15:]
                     pos=mess2.find('\x00')
                     mess2=mess2[0:pos]
                     mess=mess[is_mess+15+pos:]
                     mess3=mess2.replace('\x00','')
                     is_mess=mess.find('\x00\x00\x00\x20\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

                mess3=mess3+"\n"
                mess3=mess3.replace('(-!-)',' ')
                usern=''
                """prev=''
                data=self.server.recv(1024)
                if data.find('PRIVMSG')!=-1:
                    nick=data.split('!')[0].replace(':','')
                    message=':'.join(data.split(':')[2:]).replace('\n','')
                    if nick.find('yschat')!=-1:
                        prev=message
                if prev!=mess3:
                try:
                    self.appli.server.send('PRIVMSG '+self.appli.CHANNEL+' :'+mess3+'\r\n')
                except:
                    print "disconnected from IRC server?"
                """
                if mess3.find('has left the airplane')!=-1 and mess3[0]!="*":
                    try:
                        self.text.tag_config("left",background=colors['leftairplane','bg'], foreground=colors['leftairplane','fg'],font=colors['leftairplane','font'])
                    except:
                        print "bad color"
                        
                    self.text.insert(END,mess3,'left')
                    #try:
                    self.dic_player=mess3[:mess3.find(" has left the airplane.")]
                    print '!'+self.dic_player+'!'
                    self.appli.aduration(self.dic_player)

                elif mess3.find("-ping")!=-1:
		    self.text.insert(END,str(time())+'\n')
                    
                elif mess3.find('/kill ')!=-1:
                    mess3=mess3.strip(' ')
                    mess3=mess3.strip('\n')
                    username=mess3[1:mess3.find('/kill ')-1]
                    if username.find("erict15")!=-1 or username.find("~{241st}~Omni")!=-1 or username.find("[VFA49CO]VicViper")!=-1 or username.find("[VFA-49]Waspe414")!=-1:
                        id2=mess3[mess3.find('/kill ')+6:]
                        try:
                            id=int(id2)
                            messaget=struct.pack('<I', id)
                            messaget='\x18\x00\x00\x00\x16\x00\x00\x00\x01\x00\x00\x00'+messaget+'\x01\x00\x00\x00\x01\x00\x01\x00\xFF\x7F\x0B\x00'
                            self.appli.c.send(messaget)
                            print "kill signal sent to ID: "+id2
                        except:
                            try:
                                #print ids
                                messaget=struct.pack('<I', ids[id2])
                                messaget='\x18\x00\x00\x00\x16\x00\x00\x00\x01\x00\x00\x00'+messaget+'\x01\x00\x00\x00\x01\x00\x01\x00\xFF\x7F\x0B\x00'
                                self.appli.c.send(messaget)
                                print "kill signal sent to user: "+id2
                            except:
                                print 'username \"'+id2+'\" not found'
                    try:
                        self.text.tag_config("mess",background=colors['default_mess','bg'], foreground=colors['default_mess','fg'],font=colors['default_mess','font'])
                    except:
                        print "bad color"
                    self.text.insert(END,mess3+'\n','mess')
                
                # elif mess3.find('/report')!=-1:
                    # try:
                        # username=mess3[1:mess3.find("/report ")-1]
                        # rulebreaker=mess3[mess3.find("/report ")+8:]
                        # try:
                            # p=urllib.urlopen("http://erict15.x10hosting.com/submitban2.php?rulebreaker="+rulebreaker+"&username="+username+"&time="+strftime("[%H:%M:%S] ", localtime())+"&reason=YSChat&email=N/A")
                        # except:
                            # print "error submitting ban request"
                        # self.appli.sendmess('eventlist','PLAYER '+username+' REPORTED USER '+rulebreaker)
                    # except:
                        # print "error reporting user"
                    # self.text.insert(END,mess3,'mess')
                
                elif mess3.find('INTERCEPT MISSION/ENDURANCE MODE/CLOSE AIR SUPPORT MISSION is terminated.')!=-1 and mess3.find('(')==-1:
                    try:
                        self.text.tag_config("endM",background=colors['end_missions','bg'], foreground=colors['end_missions','fg'],font=colors['end_missions','font'])
                    except:
                        print "bad color"
                    self.text.insert(END,mess3,'endM')
                    
                elif mess3.find('took off (')!=-1 and mess3[0]!="*":
                    try:
                        self.text.tag_config("tookoff",background=colors['takeoffplane','bg'], foreground=colors['takeoffplane','fg'],font=colors['takeoffplane','font'])
                    except:
                        print "bad color"
                    if self.appli.ysc_mode=="SERVER":
                        #try:
                        self.dic_player=mess3[:mess3.find(" took off (")]
                        self.dic_aircraft=mess3[mess3.find(" took off (")+11:-2]
                        self.dic_start=time()
                        print "recorded"+self.dic_player+self.dic_aircraft+str(self.dic_start)
                        #st=ThreadURL("http://marcjeanmougin.free.fr/ys_servers/tookoff.php?server=erict15s_server&ip="+self.appli.ip.get()+"&username=erict15&aircraft="+self.dic_aircraft)
                        st=ThreadURL("http://marcjeanmougin.free.fr/ys_servers/tookoff.php?server="+self.appli.servername.get().replace(' ','_')+"&ip="+self.appli.ip.get()+"&username="+self.dic_player.replace('[','(').replace(']',')').replace('.','').replace(' ','')+"&aircraft="+self.dic_aircraft)
                        st.start()
                        #p=urllib.urlopen("http://marcjeanmougin.free.fr/ys_servers/tookoff.php?server="+self.appli.servername.get().replace(' ','')+"&ip="+self.appli.ip.get()+"&username="+self.dic_player.replace('[','(').replace(']',')').replace('.','').replace(' ','')+"&aircraft="+self.dic_aircraft)
                        #print p.read()
                        #p_end=p.read()[-2:]
                        #if p_end!="ok":
                         #   self.appli.receive.insert(END,">>> Cannot insert "+self.dic_player+" take-off event: server answered: 'wrong'\n")
                        dic_users[self.dic_player]=self.dic_aircraft+'|)-(|'+str(self.dic_start)
##                        except:
##                            print "pb tookoff"
                    self.text.insert(END,mess3,'tookoff')
                    
                elif mess3.find('**** ENDURANCE MODE START')!=-1 or mess3.find('**** END ENDURANCE MODE ****')!=-1 and mess3.find('(')==-1:
                    try:
                        self.text.tag_config("endu",background=colors['endurancemod','bg'], foreground=colors['endurancemod','fg'],font=colors['endurancemod','font'])
                    except:
                        print "bad color"
                    self.text.insert(END,mess3,'endu')
                elif mess3.find('**** INTERCEPT MISSION START ****')!=-1 or mess3.find('**** END INTERCEPT MISSION ****')!=-1 and mess3.find('(')==-1:
                    try:
                        self.text.tag_config("inter",background=colors['interception','bg'], foreground=colors['interception','fg'],font=colors['interception','font'])
                    except:
                        print "bad color"
                    self.text.insert(END,mess3,'inter')
                elif mess3.find('**** CLOSE AIR SUPPORT MISSION START ****')!=-1 or  mess3.find('**** END CLOSE AIR SUPPORT MISSION ****')!=-1 and mess3.find('(')==-1:
                    try:
                        self.text.tag_config("closeair",background=colors['closeairsupp','bg'], foreground=colors['closeairsupp','fg'],font=colors['closeairsupp','font'])
                    except:
                        print "bad color"
                    self.text.insert(END,mess3,'closeair')
                elif mess3.find('**** Server will be reset in ')!=-1:
                    #---random map
                    if self.appli.automap==1:
                        if mess3.find('30 minutes')!=-1:
                            try:
                                try:
                                    rct=os.stat(self.appli.path +'/config/network.cfg')
                                except:
                                    print "cannot found the date of lm"
                                try:
                                    if rct[8]<self.appli.connect_time:
                                        print "choose a random map"
    
                                        try:
                                            nextmap=self.appli.sce[randrange(0,len(self.appli.sce))]
                                            map=nextmap
                                            print "next will be: " + nextmap
                                            newmapline='DEFLTFIELD "'+nextmap+'"\n'
                                        except:
                                            print "cannot choose a random map"
                                        try:
                                            f=open(self.appli.path +'/config/network.cfg','r')
                                            f2=f.read()
                                            f.seek(0)
                                            while 1:
                                                
                                                text=f.readline()
                                                if text=="":
                                                    break  
                                                #print text                                  
                                                if text.find('DEFLTFIELD')!=-1:
                                                    mapline=text
                                                    print "found"
                                                    #print mapline
                                                    break                                
                                            f.close()
                                        except:
                                            print "cannot open1"
                                        else:
                                            try:
                                                #f2.replace(self.appli.map,nextmap)
                                                f2=f2.replace(mapline, newmapline)
                                            except:
                                                print "cannot replace"
                                            try:    
                                                f=open(self.appli.path +'/config/network.cfg','w')
                                                f.write(f2)
                                                f.close()
                                            except:
                                                print "cannot write"
                                    else:
                                        print "someone already chose a map"
                                        self.appli.receive.insert(END,">>> Someone already chose a map\n")
                                except:
                                    print "cannot compare the dates"
                            except:
                                print "cannot choose a random map"
                                self.appli.receive.insert(END,">>> Cannot choose a random map\n")
                    try:
                        self.text.tag_config("reset1",background=colors['willreset_in','bg'], foreground=colors['willreset_in','fg'],font=colors['willreset_in','font'])
                        if self.appli.automap==1:
                            self.appli.sendmess('eventmap',"the next map will be " + map)
                    except:
                        print "bad color"
                    self.text.insert(END,mess3,'reset1')
                 
                elif mess3.find('**** Resetting Server ****')!=-1 and mess3.find('(')==-1:
                    try:
                        self.text.tag_config("reset2",background=colors['reset_server','bg'], foreground=colors['reset_server','fg'],font=colors['reset_server','font'])                        
                    except:
                        print "bad color for reset"
                    if self.appli.autoserver==1:
                        self.appli.canreconnect=1
                    try:
                        #---restart server
                        servernick=self.appli.username.get()
                        servernick=servernick.replace(' ','')                        
                        if self.appli.autoserver==1:
                            thistime=time()
                            
                            if thistime - self.appli.time>300:
                                print 'restart the server' 
                                try:
                                    self.StartServer._Thread__stop()
                                except:
                                    print "cannot stop the thread-server"
                                try:
                                    os.chdir(self.appli.path)
                                    self.StartServer=LaunchServer(servernick,self.appli.ys_exec)
                                    self.StartServer.start()
                                except:
                                    print "cannot start the server-thread"
                            else:
                                print 'too long'
                        else:
                            print 'not allowed to restart'
                        self.appli.time=time()
                        print self.appli.time
                        print thistime
                    except:
                        print "cannot launch the server"
                    self.text.insert(END,mess3,'reset2')
                elif mess3.find('** This Server Disables Chat. **')!=-1 or mess3.find('** Cannot Send the Message. **')!=-1 and mess3.find('(')==-1:
                    try:
                        self.text.tag_config("dischat",background=colors['disable_chat','bg'], foreground=colors['disable_chat','fg'],font=colors['disable_chat','font'])
                    except:
                        print "bad color"    
                    self.text.insert(END,mess3,'dischat')
                else:
                    #---Changemap
                    if mess3.find('/changemap')!=-1:
                        if self.appli.automap==1:
                            try:
                                map2=mess3.split()
                                n=0
                                for a in map2:
                                    n+=1
                                    if a.find('/changemap')!=-1:
                                        map3=map2[n]
                                        
                                newmapline='DEFLTFIELD "'+map3+'"\n'
                                print newmapline
                            except:
                                print "cannot find the map"
                            else:
                                if (map3 in self.appli.sce):
                                    print map3
                                    map=map3
                                    print self.appli.path
                                    try:
                                        f=open(self.appli.path +'/config/network.cfg','r')
                                        f2=f.read()
                                        f.seek(0)
                                        while 1:
                                            
                                            text=f.readline()
                                            if text=="":
                                                break  
                                            print text                                  
                                            if text.find('DEFLTFIELD')!=-1:
                                                mapline=text
                                                print "found"
                                                print mapline
                                                break                                
                                        f.close()
                                    except:
                                        print "cannot open2"
                                    else:    
                                        try:
                                            try:
                                                f=open(self.appli.path +'/config/network.cfg','w+')
                                            except:
                                                print "cannot open it"
                                            else:
                                                
                                                print f2
                                                try:
                                                    f2=f2.replace(mapline, newmapline)
                                                    print f2
                                                except:
                                                    print "cannot replace"
                                                try:
                                                    f.write(f2)
                                                except:
                                                    print "problem to write"
                                                f.close()
                                                self.appli.sendmess('eventmap',"Map changed successfully")
                                        except:
                                            print "cannot write2"
                                        
                                else:
                                    print "map doesn't exist"
                                    self.appli.sendmess('eventmap',"sorry, this map doesn't exist")
 
                    #---List users
                    if mess3.find('/listusers')!=-1 and self.appli.ysc_mode=="SERVER":
                        p_players=""
                        self.appli.c.send('\x04\x00\x00\x00\x25\x00\x00\x00')
                        for d in players:
                            if d.find('[****]')!=-1:
                                p_players+=d[d.find('] ')+2:d.find(' (')]+', '
                            elif d.find('[****]')==-1:
                                p_players+='(F) '+d[d.find('] ')+2:d.find(' (')]+', '
                        print p_players
                        self.appli.sendmess('eventlist',p_players)
                    
                    if mess3.find('/listfags')!=-1:
                        p_players=""
                        self.appli.c.send('\x04\x00\x00\x00\x25\x00\x00\x00')
                        for d in players:
                            if d.find('(IFF=*)')!=-1:
                                p_players+=d[d.find('] ')+2:d.find(' (')]+', '
                        self.appli.sendmess('eventlist',p_players+'chrisye1[FA]')
                        #self.appli.sendmess('eventlist','YOU!\nNOW GTFO!')
                    if mess3.find('/listn00bs')!=-1:
                        p_players=""
                        self.appli.c.send('\x04\x00\x00\x00\x25\x00\x00\x00')
                        for d in players:
                            if d.find('(IFF=1)')!=-1:
                                p_players+=d[d.find('] ')+2:d.find(' (')]+', '
                        self.appli.sendmess('eventlist',p_players+'chrisye1[FA]')
                        #self.appli.sendmess('eventlist','YOU!\nNOW GTFO!')
                        
                    """if mess3.find('/google')!=-1:
                        query=urllib.urlencode({'q':mess3[mess3.find('/google ')+8:]})
                        start='<h2 class=r style="font-size:138%"><b>'
                        end='</b>'
                        google=httplib.HTTPConnection("www.google.com")
                        google.request("GET","/search?"+query)
                        search=google.getresponse()
                        data=search.read()
                        print data
                        #self.appli.sendmess('eventlist',data)
                        if data.find(start)==-1: self.appli.sendmess('eventlist',"Google results not found.")
                        else:
                            begin=data.index(start)
                            result=data[begin+len(start):begin+data[begin:].index(end)]
                            result = result.replace("<font size=-2> </font>",",").replace(" &#215; 10<sup>","E").replace("</sup>","").replace("\xa0",",")
                            self.appli.sendmess('eventlist',result)"""
                    
                    if mess3[0:10].find('nameless')!=-1:
                        self.appli.sendmess('eventlist','CHANGE YOUR USERNAME NAMELESS!')
                    
                    mess4=mess3.lower()
                    """
                    #swear detection
                    words=open("badwords.txt",'r')            
                    while 1:
                        self.line=words.readline()
                        self.line=self.line.lower()
                        if self.line=="":
                            break
                        if mess4.find(self.line)!=-1:
                            self.appli.sendmess('eventlist','NO SWEARING ON THE SERVER!')
                    words.close()
                    
                    if mess4.find("vulch")!=-1 and mess3.find("DO NOT VULCH!")==-1:
                        self.appli.sendmess('eventlist','DO NOT VULCH!')
                    """
                    if mess4.find('anyone there')!=-1 or mess4.find('anyone here')!=-1:
                        self.appli.sendmess('eventlist','(YSChat)/listusers')
                    """if (mess4.find('stfu')!=-1 or mess4.find('shut up')!=-1) and mess3.find('(YSChat)NO U STFU!')==-1:
                        self.appli.sendmess('eventlist','(YSChat)NO U STFU!')
                    if mess4.find('suck')!=-1 and mess3.find('(YSChat)SUCK MY VIRTUAL DICK!')==-1:
                        self.appli.sendmess('eventlist','(YSChat)SUCK MY VIRTUAL DICK!')"""
                    
                    #print "mess"
                    mess3=mess3.replace('(241st)','[241st]')
                    mess3=mess3.replace('(171st)','[171st]')
                    mess3=mess3.replace('(YGL)','[YGL]')
                    mess3=mess3.replace('(RPFS)','[RPFS]')
                    mess3=mess3.replace('(RPFW)','[RPFW]')
                    mess3=mess3.replace('(194th)','[194th]')
                    mess3=mess3.replace('(922nd)','[922nd]')
                    mess3=mess3.replace('(Sahola)','[Sahola]')
                    mess3=mess3.replace('(VNA)','[VNA]')
                    mess3=mess3.replace('(IBIS)','[IBIS]')
                    mess3=mess3.replace('(SAR)','[SAR]')
                    mess3=mess3.replace('(FF)','[FF]')
                    mess3=mess3.replace('(GAF)','[GAF]')
                    mess3=mess3.replace('(RAF)','[RAF]')
                    mess3=mess3.replace('(NAFC)','[NAFC]')
                    mess3=mess3.replace('(VA-171)','[VA-171]')
                    mess3=mess3.replace('(VFA-171)','[VFA-171]')
                    mess3=mess3.replace('(VFA-49)','[VFA-49]')
                    
                    if mess3.find(')')!=-1:#---to add color, font... to the username
                        try:
                            p_f=mess3.find(')',2)
                            p_f2=mess3.index(')',p_f+1) #nick(squad)
                            if p_f2-p_f <3:
                                p_f=p_f2 #nick message :(
                        except:
                            p_f=mess3.find(')')
                        usern=mess3[0:p_f+1]+' '
                        mess3=mess3[p_f+1:]
                        #print "pf: "+str(p_f)
                        try:
                            self.text.tag_config("pilotname",background=colors['pilotnicknam','bg'], foreground=colors['pilotnicknam','fg'],font=colors['pilotnicknam','font'])
                        except:
                            print "bad color"
                        self.text.insert(END,usern,'pilotname')
                    try:
                        self.text.tag_config("mess",background=colors['default_mess','bg'], foreground=colors['default_mess','fg'],font=colors['default_mess','font'])
                    except:
                        print "bad color"
                    self.text.insert(END,mess3,'mess')
                self.text.yview(END)
                try:
                    self.f.write('<br><font color="#333333" size="2">'+strftime("[%H:%M:%S] ", localtime())+'</font><font color="#0000FF"><strong>'+usern+'</strong></font>'+mess3)
                    self.f.flush()
                    #self.f.write(strftime("[%H:%M:%S] ", localtime())+usern+mess3)
                except:
                    print "1 message hasn't been saved in the log"
                #print mess3
                username=self.appli.return_username()
##                if usern.find(username)==-1:
##                    try:
##                        pygame.mixer.music.play()
##                    except:
##                        print("no sound")

        print '***Connection stopped (conversation saved in logfile'+strftime("%Y%m%d",localtime())+'.htm) ***'
        try:
            self.text.tag_config("ysc_mess",background=colors['ys_chat_mess','bg'], foreground=colors['ys_chat_mess','fg'],font=colors['ys_chat_mess','font'])
        except:
            print "bad color"
        self.text.insert(END,'***Connection stopped*** (conversation saved in logfile'+strftime("%Y%m%d",localtime())+'.htm) \n','ysc_mess')
        self.text.yview(END)
        self.connexion.close()
        try:
            self.f.write('<font color="#FF0000"><em>Connection stopped at '+strftime("%H:%M:%S", localtime())+'</em></font><br>')
            self.f.write("\r\n\r\n<br><br>===========================================<br>\r\n")
            self.f.flush()
            self.f.close()
        except:
            print "cannot write in the log"
        #self.appli.disconnect2()
   
    def stop(self):
        self.running = False 
        

class ThreadEmission(threading.Thread):
    """old thread to send a message, not used"""
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn            # ref. du socket de connexion
    def run(self):
        while 1:
             message_emis = raw_input("SEND: ")
             if message_emis=="exit":
                    th_R._Thread__stop()
                    print "***Connection stopped***"
                    self.connexion.close()
                    sys.exit()
             message_emis="\x6c\x00\x00\x00\x20\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"+"("+"Dos user"+")"+message_emis
             regex = re.compile(r'\\x([a-f0-9]){2}', re.I)
             message_emis = regex.sub(lambda o: chr(int(o.group(1), 16)), message_emis)
             message_emis+='\x00'*(112-len(message_emis))
             print len(message_emis) #for debug
             self.connexion.send(message_emis)

class Path_ys:
    def __init__(self):
        "read the path of Ysflight, if it exists"
        print "looking for options.txt"        
        try :
            self.f_path=open("options.txt",'r')
            self.path_ys=self.f_path.read()
            self.f_path.close()
            print "options.txt has been found in " + os.getcwd()
        except:
            print "options.txt has not been found in " + os.getcwd()
            self.win=Toplevel()
            self.win.title("YSChat first launch")
            Message(self.win,text="Thank you to use YS Chat \n").pack()
            Message(self.win,text="Have a look at the documentation if you have any question. If you have a problem you cannot solve, contact me on the forum of www.yspilots.com \n or send me an email at vincentweb984@hotmail.com").pack()
            Message(self.win,text="\n Basic commands : \n - '|' to cut the message on an other line \n - '/auto <nb of min> message' -> to send an automatic message \n - '/clear' -> clear the messages \n - '/list' -> update the player list \n - '/loadcolors' -> refresh the colors defined by ysc_colors.txt ...").pack()
            self.change_path_ys()
        self.path_ys=self.path_ys.replace('\n','')
        if self.path_ys=="":
            self.win=Toplevel()
            self.win.title("YSChat changing the YSpath")
            Message(self.win,text="YS Chat is changing the path of Ysflight \n This window will be closed automatically").pack()
            self.change_path_ys()
            self.win.destroy()
            
        print "the path of ysflight is " + self.path_ys
        print "\n Loading Scenery Templates (scenery/sce*.lst)"
        f2=open('sce_list.txt','w')
        self.sce=[]
        for nomfichier in glob.glob(self.path_ys+"/scenery/[Ss][Cc][Ee]*.lst"):
            print nomfichier
                     
            try :
                f=open(nomfichier, 'r')                
                while 1:
                    text=f.readline()
                    if text=="":
                        break
                    n_sce=text.split(' ',1)
                    if n_sce[0]!="" and n_sce[0]!="\n":
                        self.sce.append(n_sce[0])
                        f2.write(n_sce[0]+"\n")
                f.close()

            except :
                print "the file " + nomfichier + "has not been found or a problem happened while I was reading it"
                break
            
        f2.close()
    
    def change_path_ys(self):
        "change the path of Ysflight in the options"
        print "please, select the directory where ysflight is installed"
        self.f_path=open("options.txt",'w')#put it at the end of the functions, else clear even if the user selected no folder
        self.path_ys=tkFileDialog.askdirectory(parent=self.win,title="Select the directory where Ysflight is installed")
        self.f_path.write(self.path_ys)
        self.f_path.close()
        
    def change_path_ys2(self):
        self.f_path=open("options.txt",'w')
        "change the path of Ysflight in the options"
        print "please, select the directory where ysflight is installed"        
        self.path_ys=tkFileDialog.askdirectory(title="Select the directory where Ysflight is installed")
        self.f_path.write(self.path_ys)
        self.f_path.close()
        self.f_path=open("options.txt",'r')
        

class LaunchServer(threading.Thread):
    """object thread to """
    def __init__(self,servernick,ys_exec):
        threading.Thread.__init__(self)
        #self.appli=value.master
        self.servernick=servernick
        self.running = threading.Event( ) 
        self.ys_exec=ys_exec      
        
    def run(self):
        
        if not self.running.isSet():
            datetime=strftime("%Y%m%d%H%M",localtime())
            print datetime
            command=self.ys_exec + ' -server ' + self.servernick.replace('~','') +' -saveflight '+datetime+'.yfs -autoexit'
            print command
            os.system(command)
            print "doing it"
            
    def stop(self):
        self.running.set( )
            

###########################
## Programme principal : ##

colors={}
dic_users={}
yscversion=0.1082
newversion=0
if __name__ =='__main__':
    Application().mainloop()

#message maximum : 78
#max number of messages views in flight : 10
#theoric limit for username :15char

                        
                        print "first answer"
                        #adebug(messem)
                        #sleep(4)
                        #self.c.send(messem)
                        #why is it here ?
                        #self.c.send("\x08\x00\x00\x00\x26\x00\x00\x00\x00\x00\x00\x00")
                        
                        #---Get the map
                        if mess1.find('\x40\x00\x00\x00\x04\x00\x00\x00')!=-1:
                            self.map=mess1[mess1.find('\x40\x00\x00\x00\x04\x00\x00\x00')+8:]
                            pos=self.map.find('\x00')
                            self.map=self.map[0:pos]                    
                            lab=Label(self, text='map: ' + self.map)
                            lab.grid(column=1, row=5)
                        # Message to send to get the players
                        self.c.send('\x04\x00\x00\x00\x25\x00\x00\x00')                
                        #load the colors
                        os.chdir(self.folder)
                        load_colors()
                        dic_user={}                
                        #---start the threads
                        self.th_R = ThreadReception(self.c,self.receive,self.f,self.players)
                        #th_E = ThreadEmission(c)
                        self.th_R.start()
                        try:
                            self.receive.tag_config("ysc_mess",background=colors['ys_chat_mess','bg'], foreground=colors['ys_chat_mess','fg'],font=colors['ys_chat_mess','font'])
                        except:
                            print "bad color"
                        self.receive.insert(END,"***You are connected***\n",'ysc_mess')
                        self.canreconnect=0
                        self.receive.insert(END,">>>"+self.ysc_mode+"\n")
                        name=self.username.get()
                        name=name.strip('()')
                        self.username.delete(0, END)
                        self.username.insert(0, "("+name+")")
                        self.thread30s=SendMess30s(self.c)
                        self.thread30s.start()
                        #self.ircserver=IRC(self.c,self.server)
                        #self.ircserver.start()
                    
            #else:
            #    print "you cannot connect twice"
            #    tkMessageBox.showerror('YS_chat', 'You cannot connect twice, enter "/quit" to disconnect !')              
            
    def exit_ysc(self):
        "exit the program"
        print "exiting"
        self.exit=1
        self.canreconnect=0
        if self.connected==1:
            print "try to disconnect"
            self.disconnect2()
        try:
            self.th_version.stop()
            print "stop the check version"
        except:
            print "cannot stop the checkversion thread"
##        try:
##            self.AutoReconnect.stop()
##            print "stopped the auto reconnect thread"
##        except:
##            print "cannot stop the auto reconnect thread"
        try:
            self.AutoReconnect._Thread__stop()
            print "stop the autoreconnect"
        except:
            print "cannot stop the auto reconnect"
        try:
                self.thread30s.stop()
        except:
                print("cannot stop the 30s thread")

        
        
        print "exit"
        sys.exit()
        
    def disconnect2(self):
        #disconnect without retrying to restart
        self.conn_time=0
        self.canreconnect=0
        "disconnect a server"
        for nb in dic_users:
            self.aduration(nb)
        try:
            self.th_R.stop()
        except:
            print 'cannot stop the reception thread'
        try:
            self.th_R._Thread__stop()
        except:
            print "problem to stop it"
        try:
            self.c.close()
        except:
            print 'cannot close the log file'
 