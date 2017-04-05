#twitter_music_poll
from Tkinter import *
from time import sleep

import os
import tweepy
import requests
import json
from pydora import player
from pandora import clientbuilder
import sys
import termios
import getpass
import subprocess
import time
import re

#import for gui
import Tkinter
import tkMessageBox

#import needed to run gui and twitter process simultaneously
from multiprocessing import Process, Manager

#Keys for the Hemmingson Playlist Twitter Account
CK = "cmqxmjAz0jMrpTKKgRnNnEgbW"
CS = "G6QSGbXhhNk5OqDvFv16FncfVSX3knzImX6BuEFrAM4oKjKzdL"
AT = "846480128859254784-A4pfADcsSdjqucrkI72BEWagua52oWn"
ATS = "JgIczODmNBHjb7KIHNs79HR0Pmx4zBPwCCbc1dRTLJOJP"



#Keys for the Robert's twitter account Account
#consumer_key = "3gI3AIYm8OkxfkU9Er81DZ4Kd"
#consumer_secret = "drCThGHlqjHfF3QcFiEWB1LjvsglEiHoiKQ5OeB1UiYCx7PyMl"
#access_token = "2462366071-WHcsSVijoOa9tHWokK8ZNd1zQRJSseJPojGQGut"
#access_token_secret = "gtbePKnCgIl6UpkrUGLks3o77WYgKoWeRnVKXOLIg2kQ4"


#File directiory locations. Change to directory that holds twitter_music_poll
SAVE_FILE = '/home/pi/Desktop/pydora-test/SAVE_FILE'
STATION_SAVE = '/home/pi/Desktop/pydora-test/STATION_SAVE'
TWITTER_LOG = '/home/pi/Desktop/pydora-test/TWITTER_LOG'



class simpleapp_tk(Tkinter.Tk):
    def __init__(self, parent):
        Tkinter.Tk.__init__(self, parent)
        self.parent = parent

        #self.stations = file_load()
        
        #this determines the size/amount of things in the gui
        self.label_amount = 11
        self.text_variable_list = [[0]*3 for _ in range (0,self.label_amount*2)]
        self.label_list = [[0]*3 for _ in range (0,self.label_amount*2)] #Do I need this? Can i just use text_varaible_list.get?
        time.sleep(2)
        self.initialize()
        


    def initialize(self):
        self.grid()  
        self.start_sort()
############################################################################################################################################

        #Defines the top bar
        self.recent_tweet_text = Tkinter.StringVar()
        self.recent_tweet_text_label = Tkinter.Label(self, textvariable=self.recent_tweet_text,
                                  anchor="center", fg="white", bg="#CC0033",
                                  width=7, height=2,
                                  justify='left', relief='groove',
                                  cursor='dot', font=("Times",20))
        self.recent_tweet_text_label.grid(column=0, row=0, columnspan=4, sticky='EW')
        self.recent_tweet_text.set("No tweets today yet.")
        #time for most recent tweet
        self.recent_tweet_time = Tkinter.StringVar()
        self.recent_tweet_time_label = Tkinter.Label(self, textvariable=self.recent_tweet_time,
                                  anchor="center", fg="white", bg="#CC0033",
                                  width=7, height=2,
                                  justify='left', relief='groove',
                                  cursor='dot', font=("Times",20))
        self.recent_tweet_time_label.grid(column=4, row=0, columnspan=4, sticky='EW')
        self.recent_tweet_time.set("Have a nice day!")

##############################################################################################
        #Makes the "Now Playing" button
        for i in range (0, self.label_amount):
            self.b = Tkinter.Button(self, text="Now \n Playing",
                                    width=5, height=2,
                                    justify='center', relief='groove',
                                    cursor='dot', font=("Times",8))
            self.b.config(command= lambda position=i: self.now_playing_button(position))  #added i+1 argument to on_button_click. 
            self.b.grid(column=0, row=i+1, columnspan=1, sticky='EW')        

        #makes the first column, which is the titles of the stations
        for i in range (0,self.label_amount):
            self.text_variable_list[i][0] = Tkinter.StringVar()
            station = Tkinter.Label(self, textvariable=self.text_variable_list[i][0],
                                  anchor="nw", fg="white", bg="#06274F",       #change colors
                                  width=14, height=1,
                                  justify='left', relief='groove',
                                  cursor='dot', font=("Times",23))
            station.grid(column=1, row=i+1, columnspan=1, sticky='EW')
            self.text_variable_list[i][0].set(self.sorted_lst[i][0])

        #makes second column, which is number of times Station has been requested
        for i in range (0,self.label_amount):
            self.text_variable_list[i][2] = Tkinter.StringVar()
            station = Tkinter.Label(self, textvariable=self.text_variable_list[i][2],
                                  anchor="nw", fg="white", bg="#0072CE",   #change colors
                                  width=2, height=1,
                                  justify='left', relief='groove',
                                  cursor='dot', font=("Times",23))
            station.grid(column=2, row=i+1, columnspan=1, sticky='EW')
            self.text_variable_list[i][2].set(self.sorted_lst[i][1])

        #makes third column, which is the delete button
        for i in range (0, self.label_amount):
            self.b = Tkinter.Button(self, text="Delete",
                                    width=5, height=1,
                                    justify='left', relief='groove',
                                    cursor='dot', font=("Times",16))
            self.b.config(command= lambda position=i: self.delete_button(position))  #added i+1 argument to on_button_click. 
            self.b.grid(column=3, row=i+1, columnspan=1, sticky='EW')  


#################################################################################################
        
        #Makes the "Now Playing" button
        for i in range (0, self.label_amount):
            self.b = Tkinter.Button(self, text="Now \n Playing",
                                    width=5, height=2,
                                    justify='center', relief='groove',
                                    cursor='dot', font=("Times",8))
            self.b.config(command= lambda position=i+self.label_amount: self.now_playing_button(position)) 
            self.b.grid(column=4, row=i+1, columnspan=1, sticky='EW')  
        

        #makes the fourth column, which is the titles of the stations
        for i in range (0,self.label_amount):
            self.text_variable_list[i+self.label_amount][0] = Tkinter.StringVar()
            station = Tkinter.Label(self, textvariable=self.text_variable_list[i+self.label_amount][0],
                                  anchor="nw", fg="white", bg="#06274F",       #change colors
                                  width=14, height=1,
                                  justify='left', relief='groove',
                                  cursor='dot', font=("Times",23))
            station.grid(column=5, row=i+1, columnspan=1, sticky='EW')
            self.text_variable_list[i+self.label_amount][0].set(self.sorted_lst[i+self.label_amount][0])


        #makes the fifth column, which is number of times Station has been requested
        for i in range (0,self.label_amount):
            self.text_variable_list[i+self.label_amount][2] = Tkinter.StringVar()
            station = Tkinter.Label(self, textvariable=self.text_variable_list[i+self.label_amount][2],
                                  anchor="nw", fg="white", bg="#0072CE",   #change colors
                                  width=2, height=1,
                                  justify='left', relief='groove',
                                  cursor='dot', font=("Times",23))
            station.grid(column=6, row=i+1, columnspan=1, sticky='EW')
            self.text_variable_list[i+self.label_amount][2].set(self.sorted_lst[i+self.label_amount][1])

        #makes last column, which is the button
        for i in range (0, self.label_amount):
            self.b = Tkinter.Button(self, text="Delete",
                                    width=5, height=1,
                                    justify='left', relief='groove',
                                    cursor='dot', font=("Times",16),
                                    highlightbackground='grey')
            self.b.config(command= lambda position=i+self.label_amount: self.delete_button(position))  #added i+1 argument to on_button_click. 
            self.b.grid(column=7, row=i+1, columnspan=1, sticky='EW')  
#####################################################################################################

     
        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,True)
        self.update()
        self.start_check_stations()

        #needed for fullscreen stuff
        self.frame = Frame(self)
        self.frame.grid()
        self.attributes('-fullscreen', True)
        self.overrideredirect(1)
        self.state = False


        self.geometry("{0}x{1}+0+0".format(
            self.winfo_screenwidth(), self.winfo_screenheight()))
        self.bind('<Escape>', self.toggle_fullscreen)  
##################################################################################################################3
        #Assortment of functions to make the GUI work
        
    def toggle_fullscreen(self, event=None):
        self.state = not self.state
        self.attributes('-fullscreen', self.state)
        return 'break'


    def start_sort(self):
        self.sorted_lst = self.sort()
        self.after(500, self.start_sort)


    #quick version of bubble sort
    def sort(self):
        unsorted_lst = self.file_load()
        update = True
        n = len(unsorted_lst)
        while(update == True and n>1):
            update = False
            for i in range(len(unsorted_lst)-1):
                if unsorted_lst[i][1] < unsorted_lst[i+1][1]:
                    unsorted_lst[i][1],unsorted_lst[i+1][1] = unsorted_lst[i+1][1], unsorted_lst[i][1]
                    unsorted_lst[i][0],unsorted_lst[i+1][0] = unsorted_lst[i+1][0], unsorted_lst[i][0]
                    update = True
            n = n-1
        while(len(unsorted_lst)<self.label_amount*2+1):
            unsorted_lst.append(['',0])
        return (unsorted_lst)


    #loads data from STATION_SAVE into a 2d array of stations and number of that station
    def file_load(self):
        SAVE_BUFFER = []
        f = open(STATION_SAVE, 'r')
        station_list = f.read()
        f.close
        lst = station_list.split('~')
        no_dupes = list(set(lst))
        for item in no_dupes:
            if item != '':
                SAVE_BUFFER.append([item,0])

        for station in lst:
            for i in range(len(SAVE_BUFFER)):
                if station == SAVE_BUFFER[i][0]:
                    SAVE_BUFFER[i][1] = SAVE_BUFFER[i][1] + 1
        return (SAVE_BUFFER)


    def now_playing_button(self,position):
        print ("help me")
        result = tkMessageBox.askquestion("Tweet?", "Tweet out " + self.sorted_lst[position][0] + "?", icon='warning')
        if result == 'yes':
            self.now_playing(self.sorted_lst[position][0])
            time.sleep(0.5)
        else:
            self.stop_blink()


    def now_playing(self,station):
        auth = tweepy.OAuthHandler(CK, CS)
        auth.set_access_token(AT, ATS)
        api = tweepy.API(auth)
        api.update_status("You voice has been heard! is now playing the " + station + " radio station!\n" + time.strftime("%a %b %d, %I:%M %p"))
        
        
        

    #Deletes the entries of the pressed button
    def delete_button(self, position):
        result = tkMessageBox.askquestion("Delete", "Delete this entry?", icon='warning')
        if result == 'yes':
            self.do_blink = True
            self.delete_station(self.sorted_lst[position][0])
            time.sleep(0.5)
            self.check_stations()
        else:
            self.stop_blink()


    #deletes station from STATION_SAVE and updates gui
    def delete_station(self,del_station):
        print('deleting station ['+del_station+']')
        string = ''
        d = open(STATION_SAVE, "r")
        s = d.read()
        d.close()

        lines = s.split('~')
        for line in lines:
            if len(line) > 1:
                if str(line) != str(del_station):
                    string = string +'~' + line
        string = string + '~'
        d = open(STATION_SAVE, "w")
        d.write(string)
        d.close




    #Blinks bacground colors for top label
    def start_blink(self):
        self.do_blink = True
        for i in range(10):
            self.after(250*i,self.blink)


    def stop_blink(self):
        self.do_blink = False
        
    #Actual blink function
    def blink(self):
        if self.do_blink:
            current_color = self.recent_tweet_text_label.cget('background')
            new_color = '#CC0033' if current_color == '#DAAA00' else '#DAAA00'  
            self.recent_tweet_text_label.configure(background=new_color)
            self.recent_tweet_time_label.configure(background=new_color)


    #Schedules check_stations for every second
    def start_check_stations(self):
        self.check_stations()
        self.after(500, self.start_check_stations)
                
    #Checks if anything has changed in STATION_SAVE, then updates gui
    def check_stations(self):
        #Checks stations in STATION_SAVE against what is currently being displayed
        for i in range (self.label_amount):
            if(self.sorted_lst[i][0] != str(self.text_variable_list[i][0].get()) or self.sorted_lst[i+self.label_amount][0] != str(self.text_variable_list[i+self.label_amount][0].get()) ):
                self.start_blink()
                for i in range (self.label_amount):
                    self.text_variable_list[i][0].set(self.sorted_lst[i][0])
                    self.text_variable_list[i][2].set(self.sorted_lst[i][1])
                    self.text_variable_list[i+self.label_amount][0].set(self.sorted_lst[i+self.label_amount][0])
                    self.text_variable_list[i+self.label_amount][2].set(self.sorted_lst[i+self.label_amount][1])
                    
                #updates most recent tweet label
                f=open(STATION_SAVE, "r")
                s = f.read()
                f.close()
                lines = s.split('~')
                self.recent_tweet_text.set(lines[len(lines)-2])
                self.recent_tweet_time.set(time.strftime("%a %b %d, %I:%M %p"))
                    
                    
        #Checks numbers in STATION_SAVE againt what is currently being displayed
        for i in range (self.label_amount):
            if (self.sorted_lst[i][1] != int(self.text_variable_list[i][2].get()) or self.sorted_lst[i+self.label_amount][1] != int(self.text_variable_list[i+self.label_amount][2].get())):
                self.start_blink()
                for i in range (self.label_amount):
                    self.text_variable_list[i][0].set(self.sorted_lst[i][0])
                    self.text_variable_list[i][2].set(self.sorted_lst[i][1])
                    self.text_variable_list[i+self.label_amount][0].set(self.sorted_lst[i+self.label_amount][0])
                    self.text_variable_list[i+self.label_amount][2].set(self.sorted_lst[i+self.label_amount][1])
                #updates most recent tweet label
                f=open(STATION_SAVE, "r")
                s = f.read()
                f.close()
                lines = s.split('~')
                self.recent_tweet_text.set(lines[len(lines)-2])
                self.recent_tweet_time.set(time.strftime("%a %b %d, %I:%M %p"))
                    
                    
                    
    
#Twitter handler class   
def twitter():
    #connects using Pandora api. Searches for and returns actual radio station names
    def search(tweet):
        #Gets api client. Needs config file .pydora.cfg in /root to work
        client = get_client()

        search = (client.search(tweet,include_genre_stations=True))
        artists_score = 0
        songs_score = 0
        genre_score = 0

        if (len(search.genre_stations) != 0):
            genre_score = search.genre_stations[0].score
            genre_token = search.genre_stations[0].token
            genre_name = search.genre_stations[0].station_name
        
        if (len(search.artists) != 0):
            artists_score = search.artists[0].score
            artists_token = search.artists[0].token
            artists_name = search.artists[0].artist
     
        if (len(search.songs) != 0):
            songs_score = search.songs[0].score
            songs_token = search.songs[0].token
            songs_name = search.songs[0].song_name

        


        if (artists_score > 80):
            #print("Returning artist: ", artists_name)
            return artists_name
        elif(genre_score > 80):
            #print("Returning genre: ", genre_name)
            return genre_name
        elif(songs_score > 80):
            #print("Retruning song: ", songs_name)
            return songs_name

        else:
            print("Error: no station matches your request")
            return ("error")


    #install pydora (apt-get install pydora) Run pydora-configure in terminal
    #Copy the created .pydora.cfg file into /root
    def get_client():
        cfg_file = os.environ.get("PYDORA_CFG", "")
        builder = clientbuilder.PydoraConfigFileBuilder(cfg_file)
        if builder.file_exists:
            return builder.build()
 
        builder = clientbuilder.PianobarConfigFileBuilder()
        if builder.file_exists:
            return builder.build()

        if not client:
            Screen.print_error("No valid config found")
            sys.exit(1)

    #Logs tweet metadata into a SAVE_FILE for later analysis.
    #Stores station names in STATION_SAVE for use by gui
    def save_station(station):
        s = open(STATION_SAVE, 'a')
        s.write('~' + station + '~')
        print('Found the Pandora Station ['+station+']')
        s.close()
        

    def save_tweet (name, time, body):
        #We want to keep name, timestamp, tweet, and the returned station in a file
        string = ('\nname: ' + name + '\ntime: ' + time + '\ntweet: ' + body)
        f = open(SAVE_FILE, 'a')
        f.write('\n' + string)
        f.close()  
    #Acual main file. This is what runs when you execute the file
    auth = tweepy.OAuthHandler(CK, CS)
    auth.set_access_token(AT, ATS)
    api = tweepy.API(auth)

    def tweet_parse(body):
        str_lst = body.split()
        string = ""
        for i in range(len(str_lst)):
            if (str_lst[i][0] != "#" and str_lst[i][0] != "@"):
                string = string + str_lst[i] + " "
        return (string)
        


    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        print 'Error! Failed to get request token.'
        time.sleep(3)
        s = open(TWITTER_LOG, 'a')
        s.write('Error! Failed to get request token ' + time.strftime("%a %b %d, %I:%M %p") + '\n')
        s.close()
        
        subprocess.call("/home/pi/Desktop/pydora-test/reboot_script", shell=True)
        s = open(TWITTER_LOG, 'a')
        s.write('Failed to reboot ' + time.strftime("%a %b %d, %I:%M %p") + '\n')
        s.close()
    request_token = auth.request_token

    #Tweepy streamer. Executes when receiving a tweet with the searched for keywords
    class StdOutListener(tweepy.StreamListener):
        def on_data(self,data):
            print("got data")
            tweet = json.loads(data)

            body = tweet['text'] #prints out contents of tweet
                    
            #gets the user that sent the tweet
            user = tweet.get('user')
            name = user['screen_name']
            
            #gets the time the tweet was created.
            #Printed in tweet to prevent duplicate tweet errors
            time = tweet['created_at']
            time = time[:-10]

            #gets the tweet id for in_reply_to_status
            tweet_id = tweet['id']
            

            save_tweet(name,time,body)

            body = tweet_parse(body)
            station = search(body)
            if station != 'error':
                print ("station not error " + station)
                save_station(station)
                api.update_status(status="@" + name + "\nTweet recived! Logging " + station + " into our system.\n" + time, in_reply_to_status_id=tweet_id)    
            if station == ('error'):
                print("station error")
                api.update_status(status="@" + name + "\nWe couldn't find that station. Try tweeting just a Pandora radio statio and the hashtag!\n" + time, in_reply_to_status_id=tweet_id)
        
        def on_error(self, status):
            time.sleep(3)
            s = open(TWITTER_LOG, 'a')
            s.write("Error Status: " + str(status) + " []Time: "+ time.strftime("%a %b %d, %I:%M %p") + '\n')
            s.close()
        
            subprocess.call("/home/pi/Desktop/pydora-test/reboot_script", shell=True)
            s = open(TWITTER_LOG, 'a')
            s.write('Failed to reboot ' + time.strftime("%a %b %d, %I:%M %p") + '\n')
            s.close()


    #establishes streaming connection with twitter
    auth = tweepy.OAuthHandler(CK, CS)
    auth.set_access_token(AT, ATS)
    l = StdOutListener()
    
    print "Scanning for Hemmingson Playlist Requests"
    stream = tweepy.Stream(auth, l)
    
    #determines what keywords to track. Best if used on a twitter handle or hashtag
    stream.filter(track=['hemmplaylist'])
    
    #Prevents weird erros in streaming. I forget what, but leave it in.
    while(stream.running):
        time.sleep(0)
        pass

            
    
#defines the twitter process
def twitter_process():
    twitter()

#defines the gui process
def gui():
    app = simpleapp_tk(None)
    app.title('Twitter Poll')
    app.mainloop()


#main file. Starts and runs both twitter and gui processes
if (__name__ == "__main__"):
    time.sleep(10)
    s = open(TWITTER_LOG, 'a')
    s.write("Starting up program... " + ' ' + time.strftime("%a %b %d, %I:%M %p") + '\n')
    s.close()


    
    p = Process(target=twitter_process, args=())
    q = Process(target=gui, args=())

    p.start()
    q.start()

    p.join()
    q.join()
