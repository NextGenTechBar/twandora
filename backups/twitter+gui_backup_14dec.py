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
import re

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

        #self.stations = file_load()
        
        #this determines the size/amount of things in the gui
        self.label_amount = 10
        self.text_variable_list = [[0]*3 for _ in range (0,self.label_amount)]
        self.label_list = [[0]*3 for _ in range (0,self.label_amount)] #Do I need this? Can i just use text_varaible_list.get?
        time.sleep(2)
        self.initialize()
        


    def get_station_list(self):
        f = open("/home/pi/Desktop/pydora-test/DICT_SAVE", "r")
        station_list = []
        
        for i in range (self.label_amount):
            temp = f.readline()
            station = temp.split('  -')
            station_list.append(station[0])
        f.close()
        return station_list

    def get_station_number(self):
        f = open("/home/pi/Desktop/pydora-test/DICT_SAVE", "r")
        station_number = []
        
        for i in range (self.label_amount):
            temp = f.readline()
            station = temp.split('-')
            station_number.append(station[-1].strip('\n'))
        f.close()
        return station_number


    def initialize(self):
        self.grid()  
        self.start_sort()
        #self.station_list = self.get_station_list()
        #self.station_number = self.get_station_number()

        #Defines the top bar
        self.flashing_text = Tkinter.StringVar()
        self.flashing_label = Tkinter.Label(self, textvariable=self.flashing_text,
                                  anchor="center", fg="white", bg="red",
                                  width=15, height=2,
                                  justify='left', relief='groove',
                                  cursor='spider', font=("Times",20))
        self.flashing_label.grid(column=0, row=0, columnspan=4, sticky='EW')
        self.flashing_text.set("Hello World!")

        #makes the first column, which is the titles of the stations
        for i in range (0,self.label_amount):
            self.text_variable_list[i][0] = Tkinter.StringVar()
            station = Tkinter.Label(self, textvariable=self.text_variable_list[i][0],
                                  anchor="nw", fg="white", bg="#090",       #change colors
                                  width=15, height=1,
                                  justify='left', relief='groove',
                                  cursor='gumby', font=("Times",20))
            station.grid(column=0, row=i+1, columnspan=1, sticky='EW')
            self.text_variable_list[i][0].set(self.sorted_lst[i][0])

         #makes the second column, which are the recent tweet indicator. Need to implament image          
        for i in range (0,self.label_amount):
            
            self.text_variable_list[i][1] = Tkinter.StringVar()
            station = Tkinter.Label(self, textvariable=self.text_variable_list[i][1],
                                  anchor="nw", fg="white", bg="#990",      #Change colors
                                  width=5, height=1,
                                  justify='left', relief='groove',
                                  cursor='gobbler', font=("Times",20))
            station.grid(column=1, row=i+1, columnspan=1, sticky='EW')
            self.text_variable_list[i][1].set("Image goes here")

        #makes third column, which is number of times Station has been requested
        for i in range (0,self.label_amount):
            self.text_variable_list[i][2] = Tkinter.StringVar()
            station = Tkinter.Label(self, textvariable=self.text_variable_list[i][2],
                                  anchor="nw", fg="white", bg="#990",   #change colors
                                  width=5, height=1,
                                  justify='left', relief='groove',
                                  cursor='gumby', font=("Times",20))
            station.grid(column=2, row=i+1, columnspan=1, sticky='EW')
            self.text_variable_list[i][2].set(self.sorted_lst[i][1])

        #makes last column, which is the button
        for i in range (0, self.label_amount):
            self.b = Tkinter.Button(self, text="Delete",
                                    width=5, height=1,
                                    justify='left', relief='groove',
                                    cursor='trek', font=("Times",15))
            self.b.config(command= lambda position=i: self.on_button_click(position))  #added i+1 argument to on_button_click. 
            self.b.grid(column=3, row=i+1, columnspan=1, sticky='EW')  #Maybe will store which button was pressed?


     
        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,False)
        self.update()
        self.geometry(self.geometry())

        
        self.start_check_stations()

    def start_sort(self):
        self.sorted_lst = self.sort()
        self.after(5000, self.start_sort)

    #need to make a working sort function
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
        print(unsorted_lst)
        return (unsorted_lst)

    def file_load(self):
        SAVE_BUFFER = []
        station_list = open('/home/pi/Desktop/pydora-test/STATION_SAVE', 'r').read()
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


    #What the botton does when pressed.
    #Implament delete item from list function in this? Need to open dict_save and remove item.
    #Check_stations should update after 5 seconds
    def on_button_click(self, position):
        result = tkMessageBox.askquestion("Delete", "Delete this entry?", icon='warning')
        if result == 'yes':
            self.do_blink = True
            self.start_blink()
            #Make function that removes passed in station from DICT_SAVE
            self.station = self.get_station_list()
            self.delete_station(position,self.station[position])
        else:
            self.stop_blink()

    #prototype delete station function. 9/11/2016
    def delete_station(self, position,del_station):
        print (' [%] Deleting...')
        d = open("/home/pi/Desktop/pydora-test/DICT_SAVE", "r")
        lines = d.split('~')
        d.close()

        d = open("/home/pi/Desktop/pydora-test/DICT_SAVE", "w")
        for line in lines:
            entry = line.split(' ')
            #print(entry[0])
            if entry[0] != del_station:
                #print('not in ' + line)
                d.write(line)
        print(lines)
        d.close

        s = open("/home/pi/Desktop/pydora-test/STATION_SAVE", "r")
        lines = s.readlines()
        s.close()
        s = open("/home/pi/Desktop/pydora-test/STATION_SAVE", "w")
        for line in lines:
            entry = re.sub("[^a-zA-Z ]+", "", line)
            #del_sub = re.sub("[^a-zA-Z]+", "", del_station)
            print(del_station)
            #print(del_sub + '\n')
            if entry != del_station:
                print(entry)
                s.write(line)
        s.close
        self.check_stations()



    def start_blink(self):
        self.do_blink = True
        for i in range(10):
            self.after(250*i,self.blink)

    def stop_blink(self):
        self.do_blink = False

    def blink(self):
        if self.do_blink:
            current_color = self.flashing_label.cget('background')
            new_color = 'red' if current_color == 'green' else 'green'      #change colors of blink
            self.flashing_label.configure(background=new_color)


    def start_check_stations(self):
        self.check_stations()
        self.after(1000, self.start_check_stations)
                
    #Runs every 1 seconds. Called by start_check_stations
    def check_stations(self):
        #Checks stations in DICT_SAVE against what is currently being dispalyed
        for i in range (self.label_amount):
            if(self.sorted_lst[i][0] != str(self.text_variable_list[i][0].get())):
                print('not equal')
                self.start_blink()
                for i in range (self.label_amount):
                    self.text_variable_list[i][0].set(self.sorted_lst[i][0])
                    self.text_variable_list[i][2].set(self.sorted_lst[i][1])
          #Checks numbers in DICT_SAVE againt what is currently being displayed
        for i in range (self.label_amount):
            if (self.sorted_lst[i][1] != int(self.text_variable_list[i][2].get())):
                print('not equal')
                self.start_blink()
                for i in range (self.label_amount):
                    self.text_variable_list[i][0].set(self.sorted_lst[i][0])
                    self.text_variable_list[i][2].set(self.sorted_lst[i][1])
                    
    
        
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
        s.write('~' + station + '~')
        

   
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
    stream.filter(track=['ngtbtest'])
    while(stream.running):
        #time.sleep(0)
        pass



'''
def sort():    
    def lst_to_string(lst):
        total_string = ''
        for i in range (len(lst)):
            string = lst[i][0] + " - - - - - - - - - - - - - - - - - - -"
            string = string[:30]
            count = str(lst[i][1])
            total_string = total_string + string + count + '\n'
        return total_string


    def dict_to_tup(dictionary):
        #ned to finish 
        pass

    #Current Working on fuction. 
    def buffer_load():
        #list load
        SAVE_BUFFER = []
        station_list = open('/home/pi/Desktop/pydora-test/STATION_SAVE', 'r').read()
        lst = station_list.split('~')
        no_duplicates = list(set(lst))
        for item in no_duplicates:
            if item != '':
                SAVE_BUFFER.append([item,0])
        
        for station in lst:
            for i in range(len(SAVE_BUFFER)):
                if (station == SAVE_BUFFER[i][0]):
                    SAVE_BUFFER[i][1] = SAVE_BUFFER[i][1] + 1  #adds one if in list already

        print(SAVE_BUFFER)
        return (SAVE_BUFFER)
    

    def sort(dictionary):
        pass


    while True:  
        print('[S] opening STATION_SAVE to grab stations')
        dictionary = buffer_load()
        print('[D] opening DICT_SAVE to save things from STATION_SAVE')
        dictionary_file = open('/home/pi/Desktop/pydora-test/DICT_SAVE', 'w')
        dictionary_file.write(str(dictionary))
        
        #string = lst_to_string(dictionary)
        #dictionary_file.write(string)
        dictionary_file.close()
        time.sleep(5)
         
'''
def twitter_process():
    twitter()


def gui():
    app = simpleapp_tk(None)
    app.title('Twitter Poll')
    app.mainloop()



if (__name__ == "__main__"):
    p = Process(target=twitter_process, args=())
    q = Process(target=gui, args=())
    #r = Process(target=sort, args=())

    p.start()
    q.start()
    #r.start()

    p.join()
    q.join()
    #r.join()






    

