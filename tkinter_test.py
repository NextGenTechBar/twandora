#GUI Test
import Tkinter
import time
from PIL import Image, ImageTk

class simpleapp_tk(Tkinter.Tk):
    def __init__(self, parent):
        Tkinter.Tk.__init__(self, parent)
        self.parent = parent
        #this determines the size/amount of things in the gui
        label_amount = 10
        
        text_variable_list = [[0]*3 for _ in range (0,label_amount)]
        label_list = [[0]*9 for _ in range (0,3)]
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

        print (text_variable_list)
        print(label_list)

        station_list = self.get_station_list(label_amount)
        #print (station_list)

        station_number = self.get_station_number(label_amount)
        #print (station_number)

        for i in range (0,label_amount):
            #self.stationVariable = Tkinter.StringVar()
            #text_variable_list[i][1] = self.stationVariable
            text_variable_list[i][0] = Tkinter.StringVar()
            station = Tkinter.Label(self, textvariable=text_variable_list[i][0],
                                  anchor="nw", fg="white", bg="#090",
                                  width=10, height=1,
                                  justify='left', relief='groove',
                                  cursor='gumby', font=("Times",20))
            station.grid(column=0, row=i, columnspan=1, sticky='EW')
            #self.stationVariable.set(station_list[i])
            text_variable_list[i][0].set(station_list[i])

        print (text_variable_list)
        for i in range (0,label_amount):
            self.stationVariable = Tkinter.StringVar()
            #text_variable_list[i][j] = self.stationVariable
            station = Tkinter.Label(self, textvariable=self.stationVariable,
                                  anchor="nw", fg="white", bg="#990",
                                  width=5, height=1,
                                  justify='left', relief='groove',
                                  cursor='gumby', font=("Times",20))
            station.grid(column=1, row=i, columnspan=1, sticky='EW')
            self.stationVariable.set("Image")

        for i in range (0,label_amount):
            self.stationVariable = Tkinter.StringVar()
            #text_variable_list[i][j] = self.stationVariable
            station = Tkinter.Label(self, textvariable=self.stationVariable,
                                  anchor="nw", fg="white", bg="#990",
                                  width=5, height=1,
                                  justify='left', relief='groove',
                                  cursor='gumby', font=("Times",20))
            station.grid(column=2, row=i, columnspan=1, sticky='EW')
            self.stationVariable.set(station_number[i])


        for i in range (0, label_amount):
            self.b = Tkinter.Button(self, text="Playing Station",
                                    width=5, height=1,
                                    justify='left', relief='groove',
                                    cursor='gumby', font=("Times",20))
            self.b.grid(column=3, row=i, columnspan=1, sticky='EW')


     
        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,False)
        self.update()
        self.geometry(self.geometry())
        #self.entry.focus_set()
        #self.entry.selection_range(0, Tkinter.END)

        #self.after(1000, self.plop)
        time.sleep(2)
        text_variable_list[1][0].set("this changed")



if __name__ == "__main__":
    app = simpleapp_tk(None)
    app.title('my application')
    app.mainloop()
    print("Out of mainloop")


































'''

class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self,*args, **kwargs)
        self.clock = tk.Label(self, text="")
        self.clock.pack()

        self.update_clock()

    def update_clock(self):
        now = time.strftime("%H:%M:%S", time.gmtime())
        self.clock.configure(text=now)
        self.after(1000, self.update_clock)

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()


'''




'''
from Tkinter import *
from time import sleep

root = Tk()
var = StringVar()
var.set('hello')

l = Label(root, textvariable = var, height=5, width=15)
l.pack()

for i in range(15):
    sleep(1) # Need this to slow the changes down
    var.set('goodbye' if i%2 else 'hello')
    root.update_idletasks()
'''



'''
import Tkinter as tk
import random
    
root = tk.Tk()
# width x height + x_offset + y_offset:
root.geometry("170x200+30+30") 
     
languages = ['Python','Perl','C++','Java','Tcl/Tk']
labels = range(5)
for i in range(5):
   ct = [random.randrange(256) for x in range(3)]
   brightness = int(round(0.299*ct[0] + 0.587*ct[1] + 0.114*ct[2]))
   ct_hex = "%02x%02x%02x" % tuple(ct)
   bg_colour = '#' + "".join(ct_hex)
   l = tk.Label(root, 
                text=languages[i], 
                fg='White' if brightness < 120 else 'Black', 
                bg=bg_colour)
   l.place(x = 20, y = 30 + i*30, width=120, height=25)
          
root.mainloop()

'''


'''

from Tkinter import *
import time

root = Tk()
S = Scrollbar(root)
var = StringVar()
L = Label(root, height=4, textvariable=var, width=50, relief=RAISED)
var.set("Hello World!")

#T = Text(root, height=4, width=50)
S.pack(side=RIGHT, fill=Y)
#T.pack(side=LEFT, fill=Y)
#S.config(command=T.yview)
#T.config(yscrollcommand=S.set)
quote = StringVar()
quote.set("Hello World!")

L.pack()
#T.insert(END, quote)
mainloop(  )

for i in range (10):
    quote.set(i)
    time.sleep(1)
    mainloop()
'''


