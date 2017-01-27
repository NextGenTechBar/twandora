#Titter + gui
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

#import for gui
import Tkinter
import tkMessageBox

#import for processes using rabbitmq
import pika
from multiprocessing import Process, Manager


#Global Variable keys (I got these from the twitter app page)
#need to change them for other twitter accounts
consumer_key = "3gI3AIYm8OkxfkU9Er81DZ4Kd"
consumer_secret = "drCThGHlqjHfF3QcFiEWB1LjvsglEiHoiKQ5OeB1UiYCx7PyMl"
access_token = "2462366071-WHcsSVijoOa9tHWokK8ZNd1zQRJSseJPojGQGut"
access_token_secret = "gtbePKnCgIl6UpkrUGLks3o77WYgKoWeRnVKXOLIg2kQ4"


class simpleapp_tk(Tkinter.Tk):
    def __init__(self, parent):
        Tkinter.Tk.__init__(self, parent)
        self.parent = parent
        
        #this determines the size/amount of things in the gui
        label_amount = 10
        text_variable_list = [[0]*3 for _ in range (0,label_amount)]
        label_list = [[0]*3 for _ in range (0,label_amount)]
        time.sleep(3)
        self.initialize(text_variable_list, label_list, label_amount)
        


    def get_station_list(self, label_amount):
        f = open("/home/pi/Desktop/pydora-test/DICT_SAVE", "r")
        station_list = []
        
        for i in range (label_amount):
            temp = f.readline()
            station = temp.split('  -')
            station_list.append(station[0])

        return station_list

    def get_station_number(self, label_amount):
        f = open("/home/pi/Desktop/pydora-test/DICT_SAVE", "r")
        station_number = []
        
        for i in range (label_amount):
            temp = f.readline()
            station = temp.split('-')
            station_number.append(station[-1].strip('\n'))

        return station_number


    def initialize(self, text_variable_list, label_list, label_amount):
        self.grid()
        label_list = []
        


        station_list = self.get_station_list(label_amount)
        #print (station_list)

        station_number = self.get_station_number(label_amount)
        #print (station_number)

        
        self.flashing_text = Tkinter.StringVar()
        self.flashing_label = Tkinter.Label(self, textvariable=self.flashing_text,
                                  anchor="center", fg="white", bg="red",
                                  width=15, height=3,
                                  justify='left', relief='groove',
                                  cursor='spider', font=("Times",20))
        self.flashing_label.grid(column=0, row=0, columnspan=4, sticky='EW')
        self.flashing_text.set("Hello World!")


        for i in range (0,label_amount):
            text_variable_list[i][0] = Tkinter.StringVar()
            station = Tkinter.Label(self, textvariable=text_variable_list[i][0],
                                  anchor="nw", fg="white", bg="#090",
                                  width=15, height=1,
                                  justify='left', relief='groove',
                                  cursor='gumby', font=("Times",20))
            station.grid(column=0, row=i+1, columnspan=1, sticky='EW')
            text_variable_list[i][0].set(station_list[i])


        for i in range (0,label_amount):
            
            text_variable_list[i][1] = Tkinter.StringVar()
            station = Tkinter.Label(self, textvariable=text_variable_list[i][1],
                                  anchor="nw", fg="white", bg="#990",
                                  width=5, height=1,
                                  justify='left', relief='groove',
                                  cursor='gobbler', font=("Times",20))
            station.grid(column=1, row=i+1, columnspan=1, sticky='EW')
            text_variable_list[i][1].set("Image goes here")

        for i in range (0,label_amount):
            text_variable_list[i][2] = Tkinter.StringVar()
            station = Tkinter.Label(self, textvariable=text_variable_list[i][2],
                                  anchor="nw", fg="white", bg="#990",
                                  width=5, height=1,
                                  justify='left', relief='groove',
                                  cursor='gumby', font=("Times",20))
            station.grid(column=2, row=i+1, columnspan=1, sticky='EW')
            text_variable_list[i][2].set(station_number[i])

        for i in range (0, label_amount):
            self.b = Tkinter.Button(self, text="Tweet",
                                    width=5, height=1,
                                    justify='left', relief='groove',
                                    cursor='trek', font=("Times",20),
                                    command=self.on_button_click)
            self.b.grid(column=3, row=i+1, columnspan=1, sticky='EW')


     
        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,False)
        self.update()
        self.geometry(self.geometry())




    def on_button_click(self):
        result = tkMessageBox.askquestion("Tweet?", "Tweet 'Now playing:  *song*'?", icon='warning')
        if result == 'yes':
            self.start_blink()
            #Would make some function that connects to twitter and sends out a tweet real quick
        else:
            self.stop_blink()

    def start_blink(self):
        self.do_blink = True
        for i in range(10):
            self.after(250*i,self.blink)

    def stop_blink():
        self.do_blink = False

    def blink(self):
        if self.do_blink:
            current_color = self.flashing_label.cget('background')
            new_color = 'red' if current_color == 'green' else 'green'
            self.flashing_label.configure(background=new_color)

            

'''
    def OnButtonClick(self):
        i = 0
        lst = []
        string = ''
        
        station_list = open('/home/pi/Desktop/pydora-test/DICT_SAVE', 'r')
        for station in station_list:
            lst.append(station)
            string = string + station
        i = 0
        #print (string)
        self.labelVariable.set(string)
  


    def OnPressEnter(self, event):
        self.labelVariable.set(self.entryVariable.get()+"You pressed enter")
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)
'''



def twitter():
    def search(tweet):
        print ("running")
        client = get_client()
        print("Connected")

        search = (client.search(tweet,include_genre_stations=True))
        print ("About to sort stations")
        artists_score = 0
        songs_score = 0
        genre_score = 0

        print(search)

        if (len(search.artists) != 0):
            artists_score = search.artists[0].score
            artists_token = search.artists[0].token
            artists_name = search.artists[0].artist
            print("did artist search "+artists_name)
        print("#1")      
        if (len(search.songs) != 0):

            songs_score = search.songs[0].score
            songs_token = search.songs[0].token
            songs_name = search.songs[0].song_name
            print("did song search " +songs_name)
        print("#2")
        if (len(search.genre_stations) != 0):
     
            genre_score = search.genre_stations[0].score
            genre_token = search.genre_stations[0].token
            genre_name = search.genre_stations[0].station_name
            print("did genre search "+genre_name)
        print ("#3")
        print("Done sorting")

        if (artists_score > 80):
            print("Returning artist: ", artists_name)
            return artists_name
        elif(genre_score > 80):
            print("Returning genre: ", genre_name)
            return genre_name
        elif(songs_score > 80):
            print("Retruning song: ", songs_name)
            return songs_name

        else:
            print("Error: no station matches your request")
            return ("error")


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


    def save_stuff(name, time, body, station):
        #We want to keep name, timestamp, tweet, and the returned station in a file

        
        string = ('\nname: ' + name + '\ntime: ' + time + '\ntweet: ' + body + 'station: ' + station)

        f = open('/home/pi/Desktop/pydora-test/SAVE_FILE', 'a')
        f.write('\n' + string)

        s = open('/home/pi/Desktop/pydora-test/STATION_SAVE', 'a')
        s.write(station + '\n')
        
        

   
    #Acual main file. This is what runs when you execute the file
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        print 'Error! Failed to get request token.'

    request_token = auth.request_token


    class StdOutListener(tweepy.StreamListener):
        def on_data(self,data):
            tweet = json.loads(data)

            
            
            #print (tweet)
            #this has a lot of valuable information
            
            temp = tweet['text'] #prints out contents of tweet
            lst = temp.split('#')  #gets rid of #hemmingson
            print lst
            body = lst[0]
            print body
            
            #gets the user that sent the tweet
            user = tweet.get('user')
            name = user['screen_name']
            
            
            #gets the time the tweet was created.
            #Printed in tweet to prevent duplicate tweet errors
            time = tweet['created_at']
            time = time[:-10]
            '''
            #Grabs an image from local device and posts it
            image = os.path.abspath('/home/pi/Desktop/something.png')
            #prints out the screen name
            #api.update_status("@" + name + "\nRetweet Test\n" + time + "/n")
            api.update_with_media(image, status="@" + name + "\nRetweet Test\n" + time + "/n")
            '''

            
            station = search(body)
            print ("Recieved the station")
            print (station)
            if station != ('error'):
                save_stuff(name, time, body, station)
        
        def on_error(self, status):
            print (status)
    
    l = StdOutListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    print "Scanning for Hemmingson Playlist Requests"
    stream = tweepy.Stream(auth, l)
    stream.filter(track=['hemmingson'])
    while(stream.running):
        #time.sleep(0)
        pass



def gui():
    app = simpleapp_tk(None)
    app.title('Test Stuff')
    app.mainloop()



def sort():
    SAVE_BUFFER = {}
    
    def dict_to_string(dictionary):
        total_string = ''
        for key in dictionary:
            string = key + "  - - - - - - - - - - - - - - - - - - - - -"
            string = string[:30]
            count = str(dictionary[key])
            total_string = total_string + string + count + '\n'
        return total_string
    
    def __init__():
        if len(SAVE_BUFFER) == 0:
            station_list = open('/home/pi/Desktop/pydora-test/STATION_SAVE', 'r')
            for station in station_list:
                #print (station)
                temp = station[:len(station)-1]
                if temp != '':
                    if temp in SAVE_BUFFER.keys():
                        SAVE_BUFFER[temp] = SAVE_BUFFER[temp] + 1
                    else:
                        SAVE_BUFFER[temp] = 1
    while True:
        __init__()
        dictionary = open('/home/pi/Desktop/pydora-test/DICT_SAVE', 'w')
        string = dict_to_string(SAVE_BUFFER)
        #print (string)
        dictionary.write(string)
        time.sleep(2)
    
    '''
    while (True):
        station_list = open('STATION_SAVE', 'r')
        for station in station_list:
            print station

        time.sleep(20)
    '''      

def twitter_process():
    twitter()



if (__name__ == "__main__"):
    p = Process(target=twitter_process, args=())
    q = Process(target=gui, args=())
    r = Process(target=sort, args=())

    p.start()
    q.start()
    r.start()

    p.join()
    q.join()
    r.join()






    

