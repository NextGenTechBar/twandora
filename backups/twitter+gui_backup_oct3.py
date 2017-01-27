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
        self.initialize()

    def initialize(self):
        self.grid()

        self.entryVariable = Tkinter.StringVar()
        self.entry = Tkinter.Entry(self, textvariable=self.entryVariable)
        self.entry.grid(column=0, row=0, sticky='EW')
        self.entry.bind("<Return>", self.OnPressEnter)
        self.entryVariable.set(u"Enter Text Here")

        button = Tkinter.Button(self, text=u"Click here",
                                command=self.OnButtonClick)
        button.grid(column=1, row=0)
        
        self.labelVariable = Tkinter.StringVar()
        label = Tkinter.Label(self, textvariable=self.labelVariable,
                              anchor="nw", fg="white", bg="#235",
                              width=25, height=25,
                              justify='right')
        label.grid(column=0, row=1, columnspan=2, sticky='EW')
        self.labelVariable.set(u"requested stations go here")
        '''       
        self.labelVariable2 = Tkinter.StringVar()
        label2 = Tkinter.Label(self, textvariable=self.labelVariable2,
                              anchor="nw", fg="white", bg="#235",
                              width=25, height=25,
                              justify='left')
        label2.grid(column=1, row=1, columnspan=1, sticky='EW')
        self.labelVariable2.set(u"Number of tweets go here")
        '''

        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,True)
        self.update()
        self.geometry(self.geometry())
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)



    def OnButtonClick(self):
        i = 0
        lst = []
        string = ''
        
        station_list = open('DICT_SAVE', 'r')
        for station in station_list:
            lst.append(station)
            string = string + station
        i = 0
        #print (string)
        self.labelVariable.set(string)
        '''
        for i in range (len(lst)):
            print (lst[i])
            self.labelVariable.set(lst[i])
         '''   

        '''
        self.labelVariable.set(self.entryVariable.get()+"You clicked the button!")
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)
        '''
    def OnPressEnter(self, event):
        self.labelVariable.set(self.entryVariable.get()+"You pressed enter")
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)









def twitter():
    #Trying to implement this dictonary as a file
    #user_time = {}
    
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
        if (len(search.songs) != 0):

            songs_score = search.songs[0].score
            songs_token = search.songs[0].token
            songs_name = search.songs[0].song_name
            print("did song search " +songs_name)
        if (len(search.genre_stations) != 0):
     
            genre_score = search.genre_stations[0].score
            genre_token = search.genre_stations[0].token
            genre_name = search.genre_stations[0].station_name
            print("did genre search "+genre_name)

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

        f = open('SAVE_FILE', 'a')
        f.write('\n' + string)

        s = open('STATION_SAVE', 'a')
        s.write('\n' + station + '\n')
        #s.write('\n'  station)






    def user_ban(name, date, time):
        f = open('USER_TIME', 'r+')
        for line in f:
            temp = line.split()
            if temp[0] == name:
                if temp[1] == time:
                    if temp[2]-time < 1:
                        pass
        
        
        


        '''
        for user in user_time:
            if user == new_user:
                if user_time[user] - new_time < 0:
                    print("This will fail. You have tweeted within the last hour")
                    return ("User is banned")
            else:
                user_time[new_user] = new_time
                print("added new user")
                return user_time
        '''
    
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
            time_list = time.split()
            hour_min_sec = time_list[3]
            hour_min_sec_list = hour_min_sec.split(':')
            just_hour = hour_min_sec_list[0]
            date = time_list[2]
            print (date)
            print(just_hour)
            '''
            #Grabs an image from local device and posts it
            image = os.path.abspath('/home/pi/Desktop/something.png')
            #prints out the screen name
            #api.update_status("@" + name + "\nRetweet Test\n" + time + "/n")
            api.update_with_media(image, status="@" + name + "\nRetweet Test\n" + time + "/n")
            '''


            ban = user_ban(name, date, time)
            print(ban)
            
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
    app.title('Pandora Suggestions')
    app.mainloop()



def sort():
    SAVE_BUFFER = {}
    
    def dict_to_string(dictionary):
        total_string = ''
        for key in dictionary:
            if len(key) > 1:
                string = key + "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
                string = string[:30]
                count = str(dictionary[key])
                total_string = total_string + string + count + '\n'
        return total_string
    
    def __init__():
        if len(SAVE_BUFFER) == 0:
            station_list = open('STATION_SAVE', 'r')
            for station in station_list:
                print (station)
                temp = station[:len(station)-1]
                if temp in SAVE_BUFFER.keys():
                    SAVE_BUFFER[temp] = SAVE_BUFFER[temp] + 1
                else:
                    SAVE_BUFFER[temp] = 1
    __init__()
    print(SAVE_BUFFER)
    dictionary = open('DICT_SAVE', 'w')
    string = dict_to_string(SAVE_BUFFER)
    print (string)
    dictionary.write(string)
    
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
    p = Process(target=twitter, args=())
    q = Process(target=gui, args=())
    r = Process(target=sort, args=())

    p.start()
    q.start()
    r.start()

    p.join()
    q.join()
    r.join()






    

