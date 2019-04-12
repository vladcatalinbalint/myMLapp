from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import tkinter.scrolledtext as tkst
import tkinter.font as tkFont
import matplotlib.pyplot as plt
plt.rc("font", size=14)
from matplotlib.figure import Figure
import pygame
from functools import partial
from time import sleep
import pandas as pd
import numpy as np
import xlrd
from termcolor import *
import colorama
colorama.init()
import webbrowser
from subprocess import PIPE, Popen
from inspect import getsource
from io import StringIO
from termcolor import colored
import time
import os
import sys
import re
import xlsxwriter
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
import seaborn as sns
import statsmodels.api as sm
from imblearn.over_sampling import SMOTE
sns.set(style="white")
sns.set(style="whitegrid", color_codes=True)

# bundle files and images within the exe doc
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# stop the additional Tk window from popping up
balint=Tk()
balint.withdraw()

#initialize passes and users
username=("vlad")
password=("balint")

# select a theme
s = ttk.Style()
s.theme_use("alt")

file_path = StringVar
# new key function
def browse_button():
    try:
        filename = filedialog.askopenfilename(filetypes=(("Template files", "*.type"), ("All files", "*")), title="Select a file")
        myfilename = os.path.normpath(filename)
        global mypath
        mypath = os.path.dirname(filename)
        mypath = mypath.replace(os.sep, '/')
        global mydata
        if myfilename.lower().endswith(('.csv')) == True:
            mydata = pd.read_csv(myfilename, sep=mycsv1.get(), header=mycsv2, usecols=mycsv3, nrows=mycsv4, na_values=mycsv5)
        elif myfilename.lower().endswith(('.xls', '.xlsx', '.xlsm')) == True:
            mydata = pd.read_excel(myfilename, header=myxl2, usecols=myxl3, nrows=myxl4, na_values=myxl5,
                                   convert_float=myxl6)
        elif myfilename.lower().endswith(('.txt')) == True:
            with open(myfilename, 'r') as f:
                mydata = pd.DataFrame(f.readlines())
                f.close()
        else:
            pass
    except Exception:
        pass

def combine_funcs(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
    return combined_func

class quitButton(Button):
    def __init__(self):
        Button.__init__(self)
        self['text'] = 'Cancel'
        # Command to close the window (the destroy method)
        self['command'] = self.destroy
        self.pack()

class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master=master
        self._geom = "{0}x{1}+0+0".format(
            master.winfo_screenwidth(), master.winfo_screenheight())
        w = 1150  # width for the Tk root
        h = 750  # height for the Tk root
        # get screen width and height
        ws = master.winfo_screenwidth()  # width of the screen
        hs = master.winfo_screenheight()  # height of the screen
        # calculate x and y coordinates for the Tk root window
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        master.geometry('%dx%d+%d+%d' % (w, h, x, y))
        master.bind('<Escape>', self.toggle_geom)
    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        self.master.geometry(self._geom)
        self._geom=geom

# multiple menus
class DblMenu(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        items = {"Theme": ["blank","sylvania","berlin","amelia"],
                 "Sound": ["w/ Sound", "w/o Sound"],
                 "Colors": ["magenta","ivory","turquoise"]}
        self.the_value = StringVar()
        self.the_value.set("File")
        self.menubutton = Menubutton(self, textvariable=self.the_value, indicatoron=True, relief=FLAT)
        self.topMenu = Menu(self.menubutton, tearoff=False)
        self.menubutton.configure(menu=self.topMenu)
        for key in sorted(items.keys()):
            menu = Menu(self.topMenu)
            self.topMenu.add_cascade(label=key, menu=menu)
            for value in items[key]:
                menu.add_radiobutton(label=value, variable = self.the_value, value=value)
        self.menubutton.pack()

# select themes
belcolors=["white", "black"]
def option_changed(*args):
    global belcolors
    if myoptlist.get() == "blank":
        belcolors=[]
        belcolors.append("white")
        belcolors.append("black")
    elif myoptlist.get()=="sylvania":
        belcolors = []
        belcolors.append("Dark Slate Gray")
        belcolors.append("lightgray")
    elif myoptlist.get()=="berlin":
        belcolors = []
        belcolors.append("black")
        belcolors.append("lawngreen")
    elif myoptlist.get()== "amelia":
        belcolors = []
        belcolors.append("maroon")
        belcolors.append("orange")
    else:
        belcolors = []
        belcolors.append("white")
        belcolors.append("black")
    return(belcolors)

# select levels
mylevels=["Intro", "Intermediate", "Advanced"]
def levels_changed(*args):
    global mylevels
    if myoptlist1.get() == "Intro":
        combine_funcs(root.withdraw(), mypane1())
    elif myoptlist1.get()=="Intermediate":
        pass
    elif myoptlist1.get()== "Advanced":
        pass
    else:
        combine_funcs(mypane1(), root.withdraw())

class HoverButton(Button):
    def __init__(self, master, **kwargs):
        Button.__init__(self, master=master, **kwargs)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
    def on_enter(self, e):
        self['background'] = self['activebackground']
    def on_leave(self, e):
        self['background'] = self.defaultBackground

# a subclass of Canvas for dealing with resizing of windows
class ResizingCanvas(Canvas):
    def __init__(self,parent,**kwargs):
        Canvas.__init__(self,parent,**kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()
    def on_resize(self,event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all",0,0,wscale,hscale)

class ResizePic(Frame):
    def __init__(self, master, *pargs):
        Frame.__init__(self, master, *pargs)
        self.image = Image.open(resource_path("darback.gif"))
        self.img_copy = self.image.copy()
        self.background_image = ImageTk.PhotoImage(self.image)
        self.background = Label(self, image=self.background_image)
        self.background.pack(fill=BOTH, expand=YES)
        self.background.bind('<Configure>', self._resize_image)
    def _resize_image(self, event):
        new_width = event.width
        new_height = event.height
        self.image = self.img_copy.resize((new_width, new_height))
        self.background_image = ImageTk.PhotoImage(self.image)
        self.background.configure(image=self.background_image)

teams = range(100)
def progress_command():
    #start progress bar
    popup = Toplevel()
    Label(popup, text="Files being downloaded").grid(row=0,column=0)
    progress = 0
    progress_var = DoubleVar()
    progress_bar = ttk.Progressbar(popup, variable=progress_var, maximum=100)
    progress_bar.grid(row=1, column=0)#.pack(fill=tk.X, expand=1, side=tk.BOTTOM)
    popup.pack_slaves()
    progress_step = float(100.0/len(teams))
    for team in teams:
        popup.update()
        time.sleep(5) # lauch task
        progress += progress_step
        progress_var.set(progress)
    return 0
#-----------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------
# create sound
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
pygame.mixer.unpause()

thispause=0
def mypause():
    global thispause
    thispause += 3

mysound=pygame.mixer.Sound(resource_path(r"cordless_drill.wav"))
def thismysound():
    if (thispause%2)==0:
        pygame.mixer.Sound.play(mysound)
    else:
        pygame.mixer.pause()

mysound2=pygame.mixer.Sound(resource_path(r"Deadbolt_Lock.wav"))
def thismysound2():
    if (thispause % 2) == 0:
        pygame.mixer.Sound.play(mysound2)
    else:
        pygame.mixer.pause()

#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
# redirect output function
class StdoutRedirector(object):
    def __init__(self,text_widget):
        self.text_space = text_widget
        self.text_space.tag_config('mynormal', foreground=belcolors[1])
    def write(self,string, *args):
        self.text_space.insert('end', string, "mynormal")
        self.text_space.see('end')

class StderrRedirector(object):
    def __init__(self, text_widget):
        self.text_space = text_widget
        self.text_space.tag_config('myerror', foreground="red")
    def write(self, string, *args):
        self.text_space.insert('end', string, "myerror")
        self.text_space.see('end')

#########################################################################################################
# add images to the text box below
img = PhotoImage(file = resource_path(r"myreg.png")) # this is the graph image in 'mytheory'
# textbox for new commands
myinput2=[]
myinput3=[]
mydrop=[]
class mycode(object):
    def __init__(self,parent):
        self.parent = parent
        self.myinit()
    def myexec_r(self, *args):
        print(20 * '=')
        file = self.myentrybox.get('1.00', END)
        if file.startswith('"') and file.endswith('"'):
            file = '"""' + file[1:-1] + '"""'
        exec(file)
    def retrieve_inputP(self,*args):
        global myinput2, myinput3
        print(20* '=')
        myinput1 = self.myentrybox.selection_get()
        [exec('print(line)') for line in myinput1.splitlines() if 'import' or 'from' in line]
        myinput4 = [line for line in myinput1.splitlines() if '=' not in line]
        myinput5 = '\n'.join(myinput4)
        try:
            exec(myinput5)
        except Exception:
            pass
        del myinput1, myinput4, myinput5
    # multiple menus
    class DblMenu_intro(Frame):
        def __init__(self, parent):
            Frame.__init__(self, parent)
            items = {"Classifications": ["Logistic Regression", "Linear Discriminant Analysis",
                                         "Naive Bayes Classifier", "K-Nearest Neighbours",
                                         "Support Vector Machines", "Decision Trees", "Random Forest",
                                         "Bagging","Boosting"],
                     "Regressions": ["Linear Regression", "Logistic Regression", "Polynomial Regression",
                                     "Ridge Regression", "Lasso Regression",
                                     "ElasticNet Regression", "Quantile Regression", "Principal Component Regression",
                                     "Partial Least Squares Regression", "Support Vector Regression",
                                     "Ordinal Regression", "Poisson Regression", "Negative Binomial Regression",
                                     "Quasi-Poisson Regression", "Cox Regression"]
                     }
            self.the_value = StringVar()
            self.the_value.set("Supervised Learning")
            self.menubutton = Menubutton(self, textvariable=self.the_value, indicatoron=False,
                                         relief=FLAT, highlightthickness=0)
            self.topMenu = Menu(self.menubutton, tearoff=False)
            self.menubutton.configure(menu=self.topMenu, bg=belcolors[0], fg=belcolors[1])
            for key in sorted(items.keys()):
                menu = Menu(self.topMenu, tearoff=False)
                self.topMenu.add_cascade(label=key, menu=menu)
                if key == "Classifications":
                    try:
                        menu.add_command(label="Logistic Regression", command=mylogreg)
                        menu.add_command(label="Linear Discriminant Analysis")
                        menu.add_command(label="Naive Bayes Classifier")
                        menu.add_command(label="K-Nearest Neighbours")
                        menu.add_command(label="Support Vector Machines")
                        menu.add_command(label="Decision Trees")
                        menu.add_command(label="Bagging")
                        menu.add_command(label="Random Forest")
                        menu.add_command(label="Boosting")
                    except Exception:
                        print('Please import data')
                elif key == "Regressions":
                    try:
                        menu.add_command(label="Linear Regression")
                        menu.add_command(label="Logistic Regression")
                        menu.add_command(label="Polynomial Regression")
                        menu.add_command(label="Ridge Regression")
                        menu.add_command(label="Lasso Regression")
                        menu.add_command(label="ElasticNet Regression")
                        menu.add_command(label="Quantile Regression")
                        menu.add_command(label="Principal Component Regression")
                        menu.add_command(label="Partial Least Squares Regression")
                        menu.add_command(label="Support Vector Regression")
                        menu.add_command(label="Ordinal Regression")
                        menu.add_command(label="Poisson Regression")
                        menu.add_command(label="Negative Binomial Regression")
                        menu.add_command(label="Quasi-Poisson Regression")
                        menu.add_command(label="Cox Regression")
                    except Exception:
                        print('Please import data')
                pass
            self.menubutton.pack()
    # display data
    def mytab(self,*args):
        dataroot = Toplevel()
        dataroot.geometry("600x300")
        dataroot.title("View Data")
        data = mydata.iloc[0:20, 0:mydata.shape[1]]
        frame = Frame(dataroot)
        frame.pack()
        mytuple = tuple(i for i in range(len(data.iloc[0, :])))
        tree = ttk.Treeview(frame, columns=mytuple, height=10, show="headings")
        scrolly = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        scrolly.pack(side='right', fill='y')
        scrollx = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
        scrollx.pack(side='bottom', fill='x')
        tree.configure(yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        tree.tag_configure('monospace', font='courier')
        tree.pack(side='left')
        for i, j in enumerate(data):
            tree.heading(i, text=data.columns[i])
            tree.column(column=i, width=100, minwidth=0)
        data2 = data.values.tolist()
        for val in data2:
            myval = [val[0]]
            for i in range(len(data2[0])):
                myval.append(val[i])
            del myval[0]
            tree.insert('', 'end', values=myval)
        def selectItem(a):
            curItem = tree.focus()
            print(tree.item(curItem, "value"))
        tree.bind('<ButtonRelease-1>', selectItem)
        b1 = Button(dataroot, text="Export",
                    command=data.to_excel(mypath + '/' + 'My_export_file.xlsx', sheet_name="sheet1", index=False))
        b1.pack()
        b2 = Button(dataroot, text="Exit", command=dataroot.destroy)
        b2.pack()
    def myinit(self):
        f2 = Frame(self.parent)
        f2.config(background=belcolors[0])
        f2.pack(fill=BOTH, expand=1)
        b1 = Button(f2, text="Start", command=self.myexec_r, relief=FLAT)
        b1.config(bg=belcolors[0], fg=belcolors[1], activebackground=belcolors[1], activeforeground=belcolors[0])
        b1.grid(column=0, row=0)
        b2 = Button(f2, text="View", command=self.mytab, relief=FLAT)
        b2.config(bg=belcolors[0], fg=belcolors[1], activebackground=belcolors[1], activeforeground=belcolors[0])
        b2.grid(column=1, row=0)
        b3 = Button(f2, text="Home", command=root.deiconify, relief=FLAT)
        b3.config(bg=belcolors[0], fg=belcolors[1], activebackground=belcolors[1], activeforeground=belcolors[0])
        b3.grid(column=2, row=0)
        b4 = self.DblMenu_intro(f2)
        b4.config()
        b4.grid(column=3, row=0)
        #b4.config(bg=belcolors[0], fg=belcolors[1], activebackground=belcolors[1], activeforeground=belcolors[0])
        #b4.grid(column=3, row=0)
        # dictionary to hold words and colors
        highlightwords = {' False': 'orange', 'False ': 'orange', ' False ': 'orange',
                          'class ': 'orange', ' class ': 'orange',
                          'finally ': 'orange', ' finally ': 'orange',
                          'is ': 'orange', ' is ': 'orange',
                          'return ': 'orange', ' return ': 'orange',
                          'None ': 'orange', ' None ': 'orange',
                          'continue ': 'orange', ' continue ': 'orange',
                          'for ': 'orange', ' for ': 'orange',
                          'lambda ': 'orange', ' lambda ': 'orange',
                          'try:': 'orange', ' try': 'orange', 'try ': 'orange', ' try ': 'orange',
                          'True ': 'orange', ' True ': 'orange',
                          'and ': 'orange', ' and ': 'orange',
                          'def ': 'orange', ' def ': 'orange',
                          'as ': 'orange', ' as ': 'orange',
                          'from ': 'orange', ' from ': 'orange',
                          'nonlocal ': 'orange', ' nonlocal ': 'orange',
                          'assert ': 'orange', ' assert ': 'orange',
                          'break ': 'orange', ' break ': 'orange',
                          'except ': 'orange', ' except ': 'orange',
                          'in ': 'orange', ' in ': 'orange',
                          'raise ': 'orange', ' raise ': 'orange',
                          'else:': 'orange', ' else': 'orange', 'else ': 'orange', ' else ': 'orange',
                          'while ': 'orange', ' while ': 'orange',
                          'del ': 'orange', ' del ': 'orange',
                          'global ': 'orange', ' global ': 'orange',
                          'not ': 'orange', ' not ': 'orange',
                          'with ': 'orange', ' with ': 'orange',
                          'elif:': 'orange', ' elif': 'orange', 'elif ': 'orange', ' elif ': 'orange',
                          'if ': 'orange', ' if ': 'orange',
                          'or ': 'orange', ' or ': 'orange',
                          'yield ': 'orange', ' yield ': 'orange',
                          'import ': 'orange', ' import ': 'orange',
                          'pass ': 'orange', ' pass ': 'orange',
                          '0': 'royalblue', '1': 'royalblue', '2': 'royalblue', '3': 'royalblue', '4': 'royalblue',
                          '5': 'royalblue', '6': 'royalblue', '7': 'royalblue', '8': 'royalblue', '9': 'royalblue',
                          '@': 'orange', ' @': 'orange', "'": 'green', '"': "green", "''": 'green',
                          '""': "green", '@ ': 'orange', ' @ ': 'orange', '__init__': 'purple',
                          ' __init__': 'purple', '__init__ ': 'purple', ' __init__ ': 'purple',
                          'self': 'purple', ' self': 'purple', 'self ': 'purple', ' self ': 'purple'}
        def highlighter(event, *args):
            '''the highlight function, called when a Key-press event occurs'''
            for k, v in highlightwords.items():  # iterate over dict
                startIndex = '1.0'
                while True:
                    startIndex = self.myentrybox.search(k, startIndex, END)  # search for occurence of k
                    if startIndex:
                        endIndex = self.myentrybox.index('%s+%dc' % (startIndex, (len(k))))  # find end of k
                        self.myentrybox.tag_add(k, startIndex, endIndex)  # add tag to k
                        self.myentrybox.tag_config(k, foreground=v)  # and color it with v
                        startIndex = endIndex  # reset startIndex to continue searching
                    else:
                        break
        def thequote1(event, *args):
            self.myentrybox.insert(INSERT,'"', 'myquote1')
            self.myentrybox.tag_config('myquote1', foreground="green")
        def thequote2(event, *args):
            self.myentrybox.insert(INSERT, "'", 'myquote2')
            self.myentrybox.tag_config('myquote2', foreground="green")
        def thetab(event, *args):
            self.myentrybox.insert(INSERT, " " * 4)
            return 'break'
        def do_backspace(event, *args):
            tabWidth = 4
            # get previous <tabWidth> characters; if they are all spaces, remove them
            previous = self.myentrybox.get("insert -%d chars" % tabWidth, "insert")
            if previous == " " * tabWidth:
                self.myentrybox.delete("insert-%d chars" % tabWidth, "insert")
                # return "break" so that the default behavior doesn't happen
                return "break"
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)
        self.font = tkFont.Font(family="Courier New", size=10)
        self.myentrybox = tkst.ScrolledText(self.parent, height=50, width=50, bg=belcolors[0], fg=belcolors[1],
                                            font=self.font)
        self.myentrybox.pack(fill=BOTH, expand=1)
        self.myentrybox.bind("<Control-r>", self.myexec_r)
        self.myentrybox.bind("<Control-p>", self.retrieve_inputP)
        self.myentrybox.bind('<Key>', highlighter)  # bind key event to highlighter()
        self.myentrybox.bind('<Shift-">', thequote1)
        self.myentrybox.bind("<'>", thequote2)
        self.myentrybox.bind('<Tab>', thetab)
        self.myentrybox.bind('<Shift-Tab>', do_backspace)

class mygui(object):
    def __init__(self, parent):
        self.parent = parent
        self.InitUI()
    # plotting in canvas
    def main(self):
        missing_values_table(mydata)
        print(mymean(mydata))
    def mytheory(self):
        root9 = Toplevel()
        # info for windows placement on the screen
        w = 820  # width for the Tk root
        h = 550  # height for the Tk root
        # get screen width and height
        ws = root9.winfo_screenwidth()  # width of the screen
        hs = root9.winfo_screenheight()  # height of the screen
        # calculate x and y coordinates for the Tk root window
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        app9=FullScreenApp(root9)
        root9.overrideredirect(False)
        # create the window
        root9.title('test')
        root9.geometry('%dx%d+%d+%d' % (w, h, x, y))
        left = tkst.ScrolledText(master=root9, wrap='word', width=30, height=30, bg=belcolors[0])
        left.pack(fill=BOTH, expand=1)
        left.insert(INSERT, mytxt4, 'name')
        left.insert(INSERT, "\n\n")
        hyperlink = HyperlinkManager(left)
        left.insert(INSERT, "Hello, ")
        left.insert(INSERT, "Stack Overflow",
                    hyperlink.add(partial(webbrowser.open, "http://stackoverflow.com")))
        left.insert(INSERT, "!\n\n")
        left.insert(INSERT, "And here's ")
        left.insert(INSERT, "a search engine",
                    hyperlink.add(partial(webbrowser.open, "http://duckduckgo.com")))
        left.insert(INSERT, ".")
        left.tag_config('name', foreground=belcolors[1])
        left.config(foreground=belcolors[1], state=DISABLED)
        f1 = Frame(root9)
        f1.pack(side=LEFT)
        b1 = Button(f1, text="Console", command=combine_funcs(mypane1,root9.destroy))
        b2 = Button(f1, text="Quit", command=root9.destroy)
        b1.pack(side=LEFT)
        b2.pack(side=LEFT)
        left.image_create(END, image=img)
# select command options
    mycommands = ["mytheory"]
    def option1_changed(self, *args):
        global mycommands
        if myoptlist1.get() == "option1":
            mycommands=[]
            mycommands = self.mytheory()
        elif myoptlist1.get() == "option2":
            mycommands = []
            mycommands = self.mytheory()
        elif myoptlist1.get() == "option3":
            mycommands = []
            mycommands = self.mytheory()
        elif myoptlist1.get() == "option4":
            mycommands = []
            mycommands = self.mytheory()
        else:
            mycommands = []
            mycommands = self.mytheory()
        return (mycommands)
    def InitUI(self):
        f1 = Frame(self.parent)
        f1.config(background=belcolors[0])
        f1.pack(fill=BOTH, expand=1)
        global myoptlist1
        myitems1 = ["option1", "option2", "option3", "option4", "option5"]
        myoptlist1 = StringVar(f1)
        myoptlist1.set("Options")
        b1 = OptionMenu(f1, myoptlist1, *myitems1, command=self.option1_changed)
        b1.config(bg=belcolors[0], fg=belcolors[1], relief=FLAT)
        b1["menu"].config(bg=belcolors[0], fg=belcolors[1])
        b1.grid(column=0, row=0, sticky="nsew")
        b2 = Button(f1, text="Main", command=self.main, relief=FLAT)
        b2.config(bg=belcolors[0], fg=belcolors[1], activebackground=belcolors[1], activeforeground=belcolors[0])
        b2.grid(column=1, row=0, sticky="nsew")
        b3 = Button(f1, text="Theory", command=self.mytheory, relief=FLAT)
        b3.config(bg=belcolors[0], fg=belcolors[1], activebackground=belcolors[1], activeforeground=belcolors[0])
        b3.grid(column=2, row=0, sticky="nsew")
        b4 = Button(f1, text="Start", relief=FLAT)
        b4.config(bg=belcolors[0], fg=belcolors[1], activebackground=belcolors[1], activeforeground=belcolors[0])
        b4.grid(column=3, row=0, sticky="nsew")
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)
        self.text_box = tkst.ScrolledText(self.parent, height = 50, width=50, bg=belcolors[0], fg=belcolors[1])
        self.text_box.pack(fill=BOTH, expand=1)
        self.text_box.see(END)
        sys.stdout = StdoutRedirector(self.text_box)
        sys.stderr = StderrRedirector(self.text_box)

def mylearn(root5):
    f3 = Frame(root5)
    f3.config(background=belcolors[0])
    f3.pack(fill=BOTH, expand=1)
    left = tkst.ScrolledText(master=f3, wrap='word', width=50, height=50, bg=belcolors[0])
    left.pack(fill=BOTH, expand=True)
    left.insert(INSERT, mytxt4, 'name')
    left.insert(INSERT, "\n\n")
    hyperlink = HyperlinkManager(left)
    left.insert(INSERT, "Hello, ")
    left.insert(INSERT, "Stack Overflow",
                hyperlink.add(partial(webbrowser.open, "http://stackoverflow.com")))
    left.insert(INSERT, "!\n\n")
    left.insert(INSERT, "And here's ")
    left.insert(INSERT, "a search engine",
                hyperlink.add(partial(webbrowser.open, "http://duckduckgo.com")))
    left.insert(INSERT, ".")
    left.tag_config('name', foreground=belcolors[1])

# create the HyperlinkManager
class HyperlinkManager:
    def __init__(self, text):
        self.text = text
        self.text.tag_config("hyper", foreground="blue", underline=1)
        self.text.tag_bind("hyper", "<Enter>", self._enter)
        self.text.tag_bind("hyper", "<Leave>", self._leave)
        self.text.tag_bind("hyper", "<Button-1>", self._click)
        self.reset()
    def reset(self):
        self.links = {}
    def add(self, action):
        tag = "hyper-%d" % len(self.links)
        self.links[tag] = action
        return "hyper", tag
    def _enter(self, event):
        self.text.config(cursor="hand2")
    def _leave(self, event):
        self.text.config(cursor="")
    def _click(self, event):
        for tag in self.text.tag_names(CURRENT):
            if tag[:6] == "hyper-":
                self.links[tag]()
                return

# create panes
def mypane1():
    root5=Toplevel()
    # info for windows placement on the screen
    w = 820  # width for the Tk root
    h = 550  # height for the Tk root
    # get screen width and height
    ws = root5.winfo_screenwidth()  # width of the screen
    hs = root5.winfo_screenheight()  # height of the screen
    # calculate x and y coordinates for the Tk root window
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    root5.overrideredirect(False)
    # create the window
    root5.title('test')
    root5.geometry('%dx%d+%d+%d' % (w, h, x, y))
    m1 = PanedWindow(root5)
    m1.config(background=belcolors[0])
    m1.pack(fill=BOTH, expand=1)
    m2 = PanedWindow(m1, orient=VERTICAL)
    m3 = PanedWindow(m1, orient=VERTICAL)
    m1.add(m2, stretch="always")
    m1.add(m3, stretch="always")
    top = Label(m2)
    m2.add(top, stretch="always")
    bottom = Label(m2)
    m2.add(bottom, stretch="always")
    m2.config(background=belcolors[0], cursor='hand2 white white')
    top2 = Label(m3)
    m3.add(top2, stretch="always")
    m3.config(background=belcolors[0], cursor='hand2 white white')
    start2 = mygui(top2)
    start3 = mylearn(bottom)
    start4 = mycode(top)
    root5.config(background=belcolors[0], cursor='hand2 white white')
    app5 = FullScreenApp(root5)
    root5.mainloop()

#################################################################################################################

mytxt1="""In computer science, data validation is the process of
        ensuring data have undergone data cleansing to ensure they
        have data quality, that is, that they are both correct and
        useful."""

mytxt2="""Data cleansing or data cleaning is the process of detecting
and correcting (or removing) corrupt or inaccurate records from a record set,
table, or database and refers to identifying incomplete, incorrect, inaccurate
or irrelevant parts of the data and then replacing, modifying, or deleting the
dirty or coarse data."""

mytxt3="""Data extraction is the act or process of retrieving data out of
(usually unstructured or poorly structured) data sources for further data
processing or data storage (data migration)."""

mytxt4= """Data cleansing or data cleaning is the process of detecting
and correcting (or removing) corrupt or inaccurate records from a record set,
table, or database and refers to identifying incomplete, incorrect, inaccurate
or irrelevant parts of the data and then replacing, modifying, or deleting the
dirty or coarse data.Data cleansing or data cleaning is the process of detecting
and correcting (or remData cleansing or data cleaning is the process of detecting
and correcting (or removing) corrupt or inaccurate records from a record set,
table, or database and refers to identifying incomplete, incorrect, inaccurate
or irrelevant parts of the data and then replacing, modifying, or deleting the
dirty or coarse data.Data cleansing or data cleaning is the process of detecting
and correcting (or removing) corrupt or inaccurate records from a record set,
table, or database and refers to identifying incomplete, incorrect, inaccurate
or irrelevant parts of the data and then replacing, modifying, or deleting the
dirty or coarse data.Data cleansing or data cleaning is the process of detecting
and correcting (or removing) corrupt or inaccurate records from a record set,
table, or database and refers to identifying incomplete, incorrect, inaccurate
or irrelevant parts of the data and then replacing, modifying, or deleting the
dirty or coarse data.Data cleansing or data cleaning is the process of detecting
and correcting (or removing) corrupt or inaccurate records from a record set,
table, or database and refers to identifying incomplete, incorrect, inaccurate
or irrelevant parts of the data and then replacing, modifying, or deleting the
dirty or coarse data.oving) corrupt or inaccurate records from a record set,
table, or database and refers to identifying incomplete, incorrect, inaccurate
or irrelevant parts of the data and then replacing, modifying, or deleting the
dirty or coarse data.Data cleansing or data cleaning is the process of detecting
and correcting (or removing) corrupt or inaccurate records from a record set,
table, or database and refers to identifying incomplete, incorrect, inaccurate
or irrelevant parts of the data and then replacing, modifying, or deleting the
dirty or coarse data.3.1 Simple Linear Regression
Simple linear regression lives up to its name: it is a very straightforward simple linear"""

def pop1():
    root5 = Toplevel()
    label1 = Label(root5, text=mytxt1, height=0, width=100)
    label1.pack()

def pop2():
    root5 = Toplevel()
    label1 = Label(root5, text=mytxt2, height=0, width=100)
    label1.pack()

def pop3():
    root5 = Toplevel()
    label1 = Label(root5, text=mytxt3, height=0, width=100)
    label1.pack()

#------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------

# multiple analyses for each button
def mymean(x):
    return np.mean(x)

# Function to calculate missing values by column#
def missing_values_table():
    # Total missing values
    mis_val = mydata.isnull().sum()
    # Percentage of missing values
    mis_val_percent = 100 * mydata.isnull().sum() / len(mydata)
    # Make a table with the results
    mis_val_table = pd.concat([mis_val, mis_val_percent], axis=1)
    # Rename the columns
    mis_val_table_ren_columns = mis_val_table.rename(
        columns={0: 'Missing Values', 1: '% of Total Values'})
    # Sort the table by percentage of missing descending
    mis_val_table_ren_columns = mis_val_table_ren_columns[
        mis_val_table_ren_columns.iloc[:, 1] != 0].sort_values(
        '% of Total Values', ascending=False).round(1)
    # Print some summary information
    print("Your selected dataframe has " + str(mydata.shape[1]) + " columns.\n"
                                                              "There are " + str(
        mis_val_table_ren_columns.shape[0]) +
          " columns that have missing values.")
    # Return the dataframe with missing information
    return mis_val_table_ren_columns


def mylogreg():
    data = mydata.dropna()
    data['y'] = data.loc[:, 'y'].replace('yes', 1)
    data['y'] = data.loc[:, 'y'].replace('no', 0)
    print(data.shape)
    print(data.columns)
    print(data.head())
    # Let us group “basic.4y”, “basic.9y” and “basic.6y” together and call them “basic”.
    data['education'] = np.where(data['education'] == 'basic.9y', 'Basic', data['education'])
    data['education'] = np.where(data['education'] == 'basic.6y', 'Basic', data['education'])
    data['education'] = np.where(data['education'] == 'basic.4y', 'Basic', data['education'])
    # Create dummy variables
    cat_vars = ['job', 'marital', 'education', 'default', 'housing', 'loan', 'contact', 'month', 'day_of_week',
                'poutcome']
    for var in cat_vars:
        cat_list = 'var' + '_' + var
        cat_list = pd.get_dummies(data[var], prefix=var, drop_first=True)
        data1 = data.join(cat_list)
        data = data1
    cat_vars = ['job', 'marital', 'education', 'default', 'housing', 'loan', 'contact', 'month', 'day_of_week',
                'poutcome']
    data_vars = data.columns.values.tolist()
    to_keep = [i for i in data_vars if i not in cat_vars]
    data_final = data[to_keep]
    # We are going to implement SMOTE in Python
    X = data_final.loc[:, data_final.columns != 'y']
    y = data_final.loc[:, data_final.columns == 'y']
    os = SMOTE(random_state=0)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
    columns = X_train.columns
    os_data_X, os_data_y = os.fit_sample(X_train, y_train.values.ravel())
    os_data_X = pd.DataFrame(data=os_data_X, columns=columns)
    os_data_y = pd.DataFrame(data=os_data_y, columns=['y'])
    # we can Check the numbers of our data
    print("length of oversampled data is ", len(os_data_X))
    print("Number of no subscription in oversampled data", len(os_data_y[os_data_y['y'] == 0]))
    print("Number of subscription", len(os_data_y[os_data_y['y'] == 1]))
    print("Proportion of no subscription data in oversampled data is ",
          len(os_data_y[os_data_y['y'] == 0]) / len(os_data_X))
    print("Proportion of subscription data in oversampled data is ",
          len(os_data_y[os_data_y['y'] == 1]) / len(os_data_X))
    """Now we have a perfect balanced data! You may have noticed that I over-sampled only on the training data, because by
    oversampling only on the training data, none of the information in the test data is being used to create synthetic
    observations, therefore, no information will bleed from test data into the model training."""
    # The p-values for most of the variables are smaller than 0.05, except four variables, therefore, we will remove them.
    cols = ['euribor3m', 'job_blue-collar', 'job_housemaid', 'marital_unknown', 'education_illiterate',
            'month_aug', 'month_dec', 'month_jul', 'month_jun', 'month_mar',
            'month_may', 'month_nov', 'month_oct', "poutcome_success"]
    X = os_data_X[cols]
    y = os_data_y['y']
    logit_model = sm.Logit(y, X)
    result = logit_model.fit()
    print(result.summary2())
    # Logistic Regression Model Fitting
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
    logreg = LogisticRegression(solver='lbfgs')
    logreg.fit(X_train, y_train)
    # Predicting the test set results and calculating the accuracy
    y_pred = logreg.predict(X_test)
    print('Accuracy of logistic regression classifier on test set: {:.2f}'.format(logreg.score(X_test, y_test)))
    # Confusion Matrix
    myconfusion_matrix = confusion_matrix(y_test, y_pred)
    print(myconfusion_matrix)
    # Compute precision, recall, F-measure and support
    print(classification_report(y_test, y_pred))
    # ROC Curve
    logit_roc_auc = roc_auc_score(y_test, logreg.predict(X_test))
    fpr, tpr, thresholds = roc_curve(y_test, logreg.predict_proba(X_test)[:, 1])
    plt.figure()
    plt.plot(fpr, tpr, label='Logistic Regression (area = %0.2f)' % logit_roc_auc)
    plt.plot([0, 1], [0, 1], 'r--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic')
    plt.legend(loc="lower right")
    plt.savefig('Log_ROC')
    plt.show()
#---------------------------------------------------------------------------------------------------
"""
# proceed button
def proc_but():
    root2 = Toplevel()
    root2.iconbitmap(root2, resource_path(r'myicon.ico'))
    # info for windows placement on the screen
    w = 820
    h = 550
    # get screen width and heightk
    ws = root2.winfo_screenwidth()  # width of the screen
    hs = root2.winfo_screenheight()  # height of the screen
    # calculate x and y coordinates for the Tk root window
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    root2.overrideredirect(False)
    # create the window
    root2.title("Technical View")
    root2.configure(background="dim gray")
    root2.geometry('%dx%d+%d+%d' % (ws, hs, x, y))
    root2.columnconfigure(0, weight=1)  # Which column should expand with window
    root2.rowconfigure(0, weight=1)  # Which row should expand with window
    app2 = FullScreenApp(root2)
    items = [{'text': 'Regressions', 'x': 60, 'y': 100},
             {'text': 'LDA', 'x': 60, 'y': 200},
             {'text': 'LDA', 'x': 60, 'y': 300},
             {'text': 'KNN', 'x': 60, 'y': 400},
             {'text': 'Decision Trees', 'x': 60, 'y': 400},
             {'text': 'SVM', 'x': 60, 'y': 400},
             {'text': 'Naive Bayes', 'x': 60, 'y': 400},
             {'text': 'Random Forest', 'x': 60, 'y': 400},
             {'text': 'NLP', 'x': 60, 'y': 400},
             {'text': 'Kmeans', 'x': 60, 'y': 400},
             {'text': 'DBSCAN', 'x': 60, 'y': 400},
             {'text': 'PCA', 'x': 60, 'y': 400},
             {'text': 'Home', 'x': 60, 'y': 400}]
    photo2 = PhotoImage(file=resource_path(r"stars2.gif"))
    canvas = Canvas(root2, bg='khaki')  # To see where canvas is
    canvas.create_image(230, 240, image=photo2)
    canvas.grid(sticky=NSEW)
    for rngitem, item in enumerate(items):
        if rngitem == 0:
            widget = HoverButton(root2, text=item['text'], height=3, width=15, bg="peach puff", activebackground="LightGoldenrod1", command=combine_funcs(thismysound, root2.destroy, mypane1))
        # Place widget on canvas with: create_window
            canvas.create_window(item['x'], item['y'], anchor=NW,
                                 height=35, width=90, window=widget)
            widget.place(relwidth=0.1, relheight=0.065, relx=0.05, rely=0.05)
        elif rngitem == 1:
            widget = HoverButton(root2, text=item['text'], height=3, width=15, bg="peach puff", activebackground="LightGoldenrod1", command=thismysound)
        # Place widget on canvas with: create_window
            canvas.create_window(item['x'], item['y'], anchor=NW,
                                 height=35, width=90, window=widget)
            widget.place(relwidth=0.1, relheight=0.065, relx=0.3, rely=0.05)
        elif rngitem == 2:
            widget = HoverButton(root2, text=item['text'], height=3, width=15, bg="peach puff",
                                 activebackground="LightGoldenrod1", command=thismysound)
            # Place widget on canvas with: create_window
            canvas.create_window(item['x'], item['y'], anchor=NW,
                                 height=35, width=90, window=widget)
            widget.place(relwidth=0.1, relheight=0.065, relx=0.55, rely=0.05)
        elif rngitem == 3:
            widget = HoverButton(root2, text=item['text'], height=3, width=15, bg="peach puff",
                                 activebackground="LightGoldenrod1", command=combine_funcs(root2.destroy, thismysound2), relief=RAISED)
            # Place widget on canvas with: create_window
            canvas.create_window(item['x'], item['y'], anchor=NW,
                                 height=35, width=90, window=widget)
            widget.place(relwidth=0.1, relheight=0.065, relx=0.8, rely=0.05)
        elif rngitem == 4:
            widget = HoverButton(root2, text=item['text'], height=3, width=15, bg="peach puff",
                                 activebackground="LightGoldenrod1", command=combine_funcs(root2.destroy, thismysound2), relief=RAISED)
            # Place widget on canvas with: create_window
            canvas.create_window(item['x'], item['y'], anchor=NW,
                                 height=35, width=90, window=widget)
            widget.place(relwidth=0.1, relheight=0.065, relx=0.05, rely=0.3)
        elif rngitem == 5:
            widget = HoverButton(root2, text=item['text'], height=3, width=15, bg="peach puff",
                                 activebackground="LightGoldenrod1", command=combine_funcs(thismysound, root2.destroy, mypane1), relief=RAISED)
            # Place widget on canvas with: create_window
            canvas.create_window(item['x'], item['y'], anchor=NW,
                                 height=35, width=90, window=widget)
            widget.place(relwidth=0.1, relheight=0.065, relx=0.3, rely=0.3)
        elif rngitem == 6:
            widget = HoverButton(root2, text=item['text'], height=3, width=15, bg="peach puff",
                                 activebackground="LightGoldenrod1", command=combine_funcs(root2.destroy, thismysound2), relief=RAISED)
            # Place widget on canvas with: create_window
            canvas.create_window(item['x'], item['y'], anchor=NW,
                                 height=35, width=90, window=widget)
            widget.place(relwidth=0.1, relheight=0.065, relx=0.55, rely=0.3)
        elif rngitem == 7:
            widget = HoverButton(root2, text=item['text'], height=3, width=15, bg="peach puff",
                                 activebackground="LightGoldenrod1", command=combine_funcs(root2.destroy, thismysound2), relief=RAISED)
            # Place widget on canvas with: create_window
            canvas.create_window(item['x'], item['y'], anchor=NW,
                                 height=35, width=90, window=widget)
            widget.place(relwidth=0.1, relheight=0.065, relx=0.8, rely=0.3)
        elif rngitem == 8:
            widget = HoverButton(root2, text=item['text'], height=3, width=15, bg="peach puff",
                                 activebackground="LightGoldenrod1", command=combine_funcs(root2.destroy, thismysound2), relief=RAISED)
            # Place widget on canvas with: create_window
            canvas.create_window(item['x'], item['y'], anchor=NW,
                                 height=35, width=90, window=widget)
            widget.place(relwidth=0.1, relheight=0.065, relx=0.05, rely=0.55)
        elif rngitem == 9:
            widget = HoverButton(root2, text=item['text'], height=3, width=15, bg="peach puff",
                                 activebackground="LightGoldenrod1", command=combine_funcs(root2.destroy, thismysound2), relief=RAISED)
            # Place widget on canvas with: create_window
            canvas.create_window(item['x'], item['y'], anchor=NW,
                                 height=35, width=90, window=widget)
            widget.place(relwidth=0.1, relheight=0.065, relx=0.3, rely=0.55)
        elif rngitem == 10:
            widget = HoverButton(root2, text=item['text'], height=3, width=15, bg="peach puff",
                                 activebackground="LightGoldenrod1", command=combine_funcs(root2.destroy, thismysound2), relief=RAISED)
            # Place widget on canvas with: create_window
            canvas.create_window(item['x'], item['y'], anchor=NW,
                                 height=35, width=90, window=widget)
            widget.place(relwidth=0.1, relheight=0.065, relx=0.55, rely=0.55)
        elif rngitem == 11:
            widget = HoverButton(root2, text=item['text'], height=3, width=15, bg="peach puff",
                                 activebackground="LightGoldenrod1", command=combine_funcs(root2.destroy, thismysound2), relief=RAISED)
            # Place widget on canvas with: create_window
            canvas.create_window(item['x'], item['y'], anchor=NW,
                                 height=35, width=90, window=widget)
            widget.place(relwidth=0.1, relheight=0.065, relx=0.8, rely=0.55)
        elif rngitem == 12:
            widget = HoverButton(root2, text=item['text'], height=3, width=15, bg="peach puff",
                                 activebackground="LightGoldenrod1", command=combine_funcs(root.deiconify, root2.destroy), relief=RAISED)
            # Place widget on canvas with: create_window
            canvas.create_window(item['x'], item['y'], anchor=NW,
                                 height=35, width=90, window=widget)
            widget.place(relwidth=0.1, relheight=0.065, relx=0.8, rely=0.8)
        else:
            pass
    root2.mainloop()
"""

def mywin1():
    try:
        if mydata is None:
            pass
        else:
            win1 = Toplevel()
            win1.attributes("-topmost", True)
            win1.overrideredirect(1)
            # info for windows placement on the screen
            w = 800  # width for the Tk root
            h = 400  # height for the Tk root
            # get screen width and height
            ws = root.winfo_screenwidth()  # width of the screen
            hs = root.winfo_screenheight()  # height of the screen
            # calculate x and y coordinates for the Tk root window
            x = (ws / 2) - (w / 3)
            y = (hs / 2) - (h / 4)
            win1.geometry('%dx%d+%d+%d' % (w, h, x, y))
            win1.iconbitmap(resource_path(r'myicon.ico'))
            # add background
            win1.columnconfigure(0, weight=1)  # Which column should expand with window
            win1.rowconfigure(0, weight=1)  # Which row should expand with window
            win1.configure(bg="white")
            data = mydata.iloc[0:20, 0:mydata.shape[1]]
            frame = Frame(win1)
            frame.pack()
            mytuple = tuple(i for i in range(len(data.iloc[0, :])))
            tree = ttk.Treeview(frame, columns=mytuple, height=16, show="headings")
            scrolly = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
            scrolly.pack(side='right', fill='y')
            scrollx = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
            scrollx.pack(side='bottom', fill='x')
            tree.configure(yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
            tree.tag_configure('monospace', font='courier')
            tree.pack(side='left')
            for i, j in enumerate(data):
                tree.heading(i, text=data.columns[i])
                tree.column(column=i, width=100, minwidth=20)
            data2 = data.values.tolist()
            for val in data2:
                myval = [val[0]]
                for i in range(len(data2[0])):
                    myval.append(val[i])
                del myval[0]
                tree.insert('', 'end', values=myval)
            def selectItem(a):
                curItem = tree.focus()
                print(tree.item(curItem, "value"))
            tree.bind('<ButtonRelease-1>', selectItem)
            b1 = Button(win1, text="Export",
                        command=data.to_excel(mypath + '/' + 'My_export_file.xlsx', sheet_name="sheet1", index=False))
            b1.pack()
            b2 = Button(win1, text="Exit", command=win1.destroy)
            b2.pack()
            win1.mainloop()
    except Exception:
        pass

def savethecsv():
    global mycsv2, mycsv3, mycsv4, mycsv5, mycsvlist
    mycsv2 = int(mywidget11.get())
    mycsv3 = [int(i) for i in mywidget12.get().split(',') if mywidget12.get()]
    mycsv4 = int(mywidget13.get())
    mycsv5 = [str(i) for i in mywidget14.get().split(',')]

def savethexl():
    global myxl2, myxl3, myxl4, myxl5
    myxl2 = int(mywidget21.get())
    myxl3 = [int(i) for i in mywidget22.get().split(',')]
    myxl4 = int(mywidget23.get())
    myxl5 = [str(i) for i in mywidget24.get().split(',')]

def callback_function1(event):
    global rootrad1, rootrad2
    if widgetcomb1.get()=="csv":
        rootrad1 = Toplevel()
        # info for windows placement on the screen
        w = 547
        h = 367
        ws = root.winfo_screenwidth()  # width of the screen
        hs = root.winfo_screenheight()  # height of the screen
        # calculate x and y coordinates for the Tk root window
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        rootrad1.overrideredirect(0)
        # create the window
        rootrad1.title("data import")
        rootrad1.configure(background="Dark Slate Gray")
        rootrad1.geometry('%dx%d+%d+%d' % (w, h, x, y))
        rootrad1.iconbitmap(resource_path(r'myicon.ico'))  # add background
        itemsrad1 = [{'text': 'Input Data', 'x': 50, 'y': 360},
                     {'text': 'Input Data', 'x': 50, 'y': 480},
                     {'text': 'Input Data', 'x': 50, 'y': 480},
                     {'text': 'Input Data', 'x': 50, 'y': 480},
                     {'text': 'Input Data', 'x': 50, 'y': 480},
                     {'text': 'Input Data', 'x': 50, 'y': 480}]
        itemsrad2 = [{'text': 'Separator', 'x': 50, 'y': 360},
                     {'text': 'Low memory', 'x': 50, 'y': 360},
                     {'text': 'Header', 'x': 50, 'y': 360},
                     {'text': 'UseCols', 'x': 50, 'y': 360},
                     {'text': 'No of rows', 'x': 50, 'y': 360},
                     {'text': 'NA values', 'x': 50, 'y': 360}]
        itemsrad3 = [{'text': 'Proceed', 'x': 50, 'y': 360},
                     {'text': 'Cancel', 'x': 50, 'y': 360}]
        for rngitem, item in enumerate(itemsrad1):
            global mywidget11, mywidget12, mywidget13, mywidget14, mycsv1, mycsv6
            if rngitem == 0:
                i = 0
                MODES = [("Comma", ","), ("Semicolon", ';'), ("Tab", '  ')]
                mycsv1 = StringVar()
                mycsv1.set("Comma")
                for text, mode in MODES:
                    widget = Radiobutton(rootrad1, text=text, variable=mycsv1, value=mode)
                    widget.pack(side=LEFT, anchor=W)
                    widget.place(relwidth=0.14, relheight=0.05, relx=0.05, rely=0.22 + i)
                    i += 0.1
                    widget.deselect()
            elif rngitem == 1:
                i = 0
                MODES = [("True", 'True'), ("False", 'False')]
                mycsv6 = StringVar()
                mycsv6.set(True)
                for text, mode in MODES:
                    widget = Radiobutton(rootrad1, text=text, variable=mycsv6, value=mode)
                    widget.pack(side=LEFT, anchor=W)
                    widget.place(relwidth=0.14, relheight=0.05, relx=0.2, rely=0.22 + i)
                    i += 0.1
                    widget.deselect()
            elif rngitem == 2:
                widget = Entry(rootrad1, width=12, bg="white")
                widget.pack(side=LEFT, anchor=W)
                widget.place(relwidth=0.12, relheight=0.05, relx=0.4, rely=0.22)
                mywidget11 = widget
            elif rngitem == 3:
                widget = Entry(rootrad1, width=12, bg="white")
                widget.pack(side=LEFT, anchor=W)
                widget.place(relwidth=0.12, relheight=0.05, relx=0.55, rely=0.22)
                mywidget12 = widget
            elif rngitem == 4:
                widget = Entry(rootrad1, width=12, bg="white")
                widget.pack(side=LEFT, anchor=W)
                widget.place(relwidth=0.12, relheight=0.05, relx=0.4, rely=0.37)
                mywidget13 = widget
            elif rngitem == 5:
                widget = Entry(rootrad1, width=12, bg="white")
                widget.pack(side=LEFT, anchor=W)
                widget.place(relwidth=0.12, relheight=0.05, relx=0.55, rely=0.37)
                mywidget14 = widget
            else:
                pass
        for rngitem, item in enumerate(itemsrad2):
            if rngitem == 0:
                widget = Label(rootrad1, text=item['text'], bg='Dark Slate Gray')
                widget.place(relwidth=0.13, relheight=0.06, relx=0.055, rely=0.15)
            elif rngitem == 1:
                widget = Label(rootrad1, text=item['text'], bg='Dark Slate Gray')
                widget.place(relwidth=0.13, relheight=0.06, relx=0.205, rely=0.15)
            elif rngitem == 2:
                widget = Label(rootrad1, text=item['text'], bg='Dark Slate Gray')
                widget.place(relwidth=0.13, relheight=0.06, relx=0.405, rely=0.15)
            elif rngitem == 3:
                widget = Label(rootrad1, text=item['text'], bg='Dark Slate Gray')
                widget.place(relwidth=0.13, relheight=0.06, relx=0.555, rely=0.15)
            elif rngitem == 4:
                widget = Label(rootrad1, text=item['text'], bg='Dark Slate Gray')
                widget.place(relwidth=0.13, relheight=0.06, relx=0.405, rely=0.3)
            elif rngitem == 5:
                widget = Label(rootrad1, text=item['text'], bg='Dark Slate Gray')
                widget.place(relwidth=0.13, relheight=0.06, relx=0.555, rely=0.3)
            else:
                pass
        for rngitem, item in enumerate(itemsrad3):
            if rngitem == 0:
                widget = HoverButton(rootrad1, text=item['text'], height=3, width=15, bg="thistle",
                                     activebackground="LightGoldenrod1",
                                     relief=FLAT, command=combine_funcs(savethecsv,rootrad1.destroy))
                widget.place(relwidth=0.13, relheight=0.06, relx=0.055, rely=0.05)
            elif rngitem == 1:
                widget = HoverButton(rootrad1, text=item['text'], height=3, width=15, bg="thistle",
                                     activebackground="LightGoldenrod1",
                                     relief=FLAT, command=rootrad1.destroy)
                widget.place(relwidth=0.13, relheight=0.06, relx=0.205, rely=0.05)
            else:
                pass
        rootrad1.mainloop()
    elif widgetcomb1.get() == "xls" or widgetcomb1.get() == "xlsx" or widgetcomb1.get() == "xlsm":
        rootrad2 = Toplevel()
        # info for windows placement on the screen
        w = 547
        h = 367
        ws = root.winfo_screenwidth()  # width of the screen
        hs = root.winfo_screenheight()  # height of the screen
        # calculate x and y coordinates for the Tk root window
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        rootrad2.overrideredirect(0)
        # create the window
        rootrad2.title("data import")
        rootrad2.configure(background="Dark Slate Gray")
        rootrad2.geometry('%dx%d+%d+%d' % (w, h, x, y))
        rootrad2.iconbitmap(resource_path(r'myicon.ico'))  # add background
        itemsrad1 = [{'text': 'Input Data', 'x': 50, 'y': 360},
                     {'text': 'Input Data', 'x': 50, 'y': 480},
                     {'text': 'Input Data', 'x': 50, 'y': 480},
                     {'text': 'Input Data', 'x': 50, 'y': 480},
                     {'text': 'Input Data', 'x': 50, 'y': 480},
                     {'text': 'Input Data', 'x': 50, 'y': 480}]
        itemsrad2 = [{'text': 'Separator', 'x': 50, 'y': 360},
                     {'text': 'Convert to Float', 'x': 50, 'y': 360},
                     {'text': 'Header', 'x': 50, 'y': 360},
                     {'text': 'UseCols', 'x': 50, 'y': 360},
                     {'text': 'No of rows', 'x': 50, 'y': 360},
                     {'text': 'NA values', 'x': 50, 'y': 360}]
        itemsrad3 = [{'text': 'Proceed', 'x': 50, 'y': 360},
                     {'text': 'Cancel', 'x': 50, 'y': 360}]
        for rngitem, item in enumerate(itemsrad1):
            global mywidget21, mywidget22, mywidget23, mywidget24, myxl1, myxl6
            if rngitem == 0:
                i = 0
                MODES = [("Comma", ","), ("Semicolon", ';'), ("Tab", '  ')]
                myxl1 = StringVar()
                myxl1.set("Comma")
                for text, mode in MODES:
                    widget = Radiobutton(rootrad2, text=text, variable=myxl1, value=mode)
                    widget.pack(side=LEFT, anchor=W)
                    widget.place(relwidth=0.14, relheight=0.05, relx=0.05, rely=0.22 + i)
                    i += 0.1
                    widget.deselect()
            elif rngitem == 1:
                i = 0
                MODES = [("True", 'True'), ("False", 'False')]
                myxl6 = StringVar()
                myxl6.set(True)
                for text, mode in MODES:
                    widget = Radiobutton(rootrad2, text=text, variable=myxl6, value=mode)
                    widget.pack(side=LEFT, anchor=W)
                    widget.place(relwidth=0.14, relheight=0.05, relx=0.2, rely=0.22 + i)
                    i += 0.1
                    widget.deselect()
            elif rngitem == 2:
                widget = Entry(rootrad2, width=12, bg="white")
                widget.pack(side=LEFT, anchor=W)
                widget.place(relwidth=0.12, relheight=0.05, relx=0.4, rely=0.22)
                mywidget21 = widget
            elif rngitem == 3:
                widget = Entry(rootrad2, width=12, bg="white")
                widget.pack(side=LEFT, anchor=W)
                widget.place(relwidth=0.12, relheight=0.05, relx=0.55, rely=0.22)
                mywidget22 = widget
            elif rngitem == 4:
                widget = Entry(rootrad2, width=12, bg="white")
                widget.pack(side=LEFT, anchor=W)
                widget.place(relwidth=0.12, relheight=0.05, relx=0.4, rely=0.37)
                mywidget23 = widget
            elif rngitem == 5:
                widget = Entry(rootrad2, width=12, bg="white")
                widget.pack(side=LEFT, anchor=W)
                widget.place(relwidth=0.12, relheight=0.05, relx=0.55, rely=0.37)
                mywidget24 = widget
            else:
                pass

        for rngitem, item in enumerate(itemsrad2):
            if rngitem == 0:
                widget = Label(rootrad2, text=item['text'], bg='Dark Slate Gray')
                widget.place(relwidth=0.13, relheight=0.06, relx=0.055, rely=0.15)
            elif rngitem == 1:
                widget = Label(rootrad2, text=item['text'], bg='Dark Slate Gray')
                widget.place(relwidth=0.13, relheight=0.06, relx=0.205, rely=0.15)
            elif rngitem == 2:
                widget = Label(rootrad2, text=item['text'], bg='Dark Slate Gray')
                widget.place(relwidth=0.13, relheight=0.06, relx=0.405, rely=0.15)
            elif rngitem == 3:
                widget = Label(rootrad2, text=item['text'], bg='Dark Slate Gray')
                widget.place(relwidth=0.13, relheight=0.06, relx=0.555, rely=0.15)
            elif rngitem == 4:
                widget = Label(rootrad2, text=item['text'], bg='Dark Slate Gray')
                widget.place(relwidth=0.13, relheight=0.06, relx=0.405, rely=0.3)
            elif rngitem == 5:
                widget = Label(rootrad2, text=item['text'], bg='Dark Slate Gray')
                widget.place(relwidth=0.13, relheight=0.06, relx=0.555, rely=0.3)
            else:
                pass
        for rngitem, item in enumerate(itemsrad3):
            if rngitem == 0:
                widget = HoverButton(rootrad2, text=item['text'], height=3, width=15, bg="thistle",
                                     activebackground="LightGoldenrod1",
                                     relief=FLAT, command=combine_funcs(savethexl, rootrad2.destroy))
                widget.place(relwidth=0.13, relheight=0.06, relx=0.055, rely=0.05)
            elif rngitem == 1:
                widget = HoverButton(rootrad2, text=item['text'], height=3, width=15, bg="thistle",
                                     activebackground="LightGoldenrod1",
                                     relief=FLAT, command=rootrad2.destroy)
                widget.place(relwidth=0.13, relheight=0.06, relx=0.205, rely=0.05)
            else:
                pass
        rootrad2.mainloop()
    else:
        pass

def try_login(username, password):
    global window, textentry, textentry2, root, canvas
    with open("passd.txt") as f:
        new = f.readlines()
        username = new[0].rstrip()
        password = new[1].rstrip()
    if textentry.get() == username and textentry2.get() == password:
        try:
            window.destroy()
        except:
            pass
        root = Toplevel()
        # info for windows placement on the screen
        w = 820
        h = 550
        ws = root.winfo_screenwidth()  # width of the screen
        hs = root.winfo_screenheight()  # height of the screen
        # calculate x and y coordinates for the Tk root window
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        root.overrideredirect(0)
        # create the window
        root.title("Loading Data")
        root.configure(background="Dark Slate Gray")
        root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        root.iconbitmap(resource_path(r'myicon.ico'))  # add background
        root.bind("<Return>", lambda x: try_login(username, password))
        # create the window
        root.columnconfigure(0, weight=1)  # Which column should expand with window
        root.rowconfigure(0, weight=1)  # Which row should expand with window
        app = FullScreenApp(root)
        canvas = Canvas(root, bg='purple4')  # To see where canvas is
        canvas.create_image(230, 240, image=PhotoImage(resource_path(r"darback.gif")))
        canvas.pack(fill=BOTH, expand=YES)
        e = ResizePic(canvas)
        e.pack(fill=BOTH, expand=YES)
        items = [{'text': 'Home Page', 'x': 150, 'y': 100},
                 {'text': 'Proceed', 'x': 260, 'y': 100},
                 {'text': 'Browse', 'x': 50, 'y': 230},
                 {'text': 'Data Frame Structure', 'x': 50, 'y': 230},
                 {'text': 'Data View', 'x': 50, 'y': 230},
                 {'text': 'Exit', 'x': 150, 'y': 100}]
        items2 = [{'text':'Choose file to upload', 'x': 50, 'y': 140},
                  {'text': 'Select File Type:', 'x': 50, 'y': 200}]
        items3 = [{'text': 'Input Data', 'x': 370, 'y': 100},
                  {'text': 'Input Data', 'x': 480, 'y': 100},
                  {'text': 'Input Data', 'x': 590, 'y': 100},
                  {'text': 'Input Data', 'x': 590, 'y': 100}]
        items4 = [{'text': 'Input Data', 'x': 50, 'y': 170}]
        myitems1 = ["Data Exploration", "Intro", "Intermediate", "Advanced"]
        myitems2 = ["Feature Engineering", "bla", "bla", "bla"]
        myitems = ["blank","amelia","berlin","sylvania"]
        for rngitem, item in enumerate(items2):
            if rngitem == 0:
                widget = Label(root, text=item['text'])
                widget.place(relwidth=0.1, relheight=0.05, relx=0.02, rely=0.25)
            elif rngitem == 1:
                widget = Label(root, text=item['text'])
                widget.place(relwidth=0.1, relheight=0.05, relx=0.02, rely=0.35)
            else:
                pass
        for rngitem, item in enumerate(items):
            if rngitem == 0:
                widget = HoverButton(root, text=item['text'], height=3, width=15, bg="thistle",
                                     activebackground="LightGoldenrod1",
                                     relief=FLAT)
                widget.place(relwidth=0.1, relheight=0.065, relx=0.015, rely=0.15)
            elif rngitem == 1:
                widget = HoverButton(root, text=item['text'], height=3, width=15, bg="thistle",
                                     activebackground="LightGoldenrod1",
                                     command=combine_funcs(root.withdraw, mypane1), relief=FLAT)
                widget.place(relwidth=0.1, relheight=0.065, relx=0.115, rely=0.15)
            elif rngitem == 2:
                widget = HoverButton(root, text=item['text'], height=3, width=15, bg="thistle",
                                     activebackground="LightGoldenrod1",
                                     command=browse_button, relief=FLAT)
                widget.place(relwidth=0.1, relheight=0.05, relx=0.02, rely=0.30)
            elif rngitem == 3:
                widget = HoverButton(root, text=item['text'], height=3, width=15, bg="thistle",
                                     activebackground="LightGoldenrod1",
                                     command=mywin1, relief=FLAT)
                widget.place(relwidth=0.125, relheight=0.05, relx=0.35, rely=0.25)
            elif rngitem == 4:
                widget = HoverButton(root, text=item['text'], height=3, width=15, bg="thistle",
                                     activebackground="LightGoldenrod1",
                                     relief=FLAT)
                widget.place(relwidth=0.125, relheight=0.05, relx=0.465, rely=0.25)
            elif rngitem == 5:
                widget = HoverButton(root, text=item['text'], height=3, width=15, bg="thistle",
                                     activebackground="LightGoldenrod1",
                                     command=root.destroy, relief=FLAT)
                widget.place(relwidth=0.1, relheight=0.065, relx=0.615, rely=0.15)
            else:
                pass
        for rngitem, item in enumerate(items3):
            if rngitem == 0:
                global myoptlist
                myoptlist = StringVar(root)
                myoptlist.set(myitems[0])
                widget = OptionMenu(root, myoptlist, *myitems, command=option_changed)
                widget.config(indicatoron=0, compound='right', highlightthickness=0, bg="thistle", relief=FLAT)
                widget.place(relwidth=0.1, relheight=0.065, relx=0.215, rely=0.15)
            elif rngitem == 1:
                global myoptlist1
                myoptlist1 = StringVar(root)
                myoptlist1.set(myitems1[0])
                widget = OptionMenu(root, myoptlist1, *myitems1, command=levels_changed)
                widget.config(indicatoron=0, compound='right', highlightthickness=0, bg="thistle", relief=FLAT)
                widget.place(relwidth=0.1, relheight=0.065, relx=0.315, rely=0.15)
            elif rngitem == 2:
                global myoptlist2
                myoptlist2 = StringVar(root)
                myoptlist2.set(myitems2[0])
                widget = OptionMenu(root, myoptlist2, *myitems2, command=option_changed)
                widget.config(indicatoron=0, compound='right', highlightthickness=0, bg="thistle", relief=FLAT)
                widget.place(relwidth=0.1, relheight=0.065, relx=0.415, rely=0.15)
            elif rngitem == 3:
                myoptlist = StringVar(root)
                myoptlist.set(myitems[0])
                widget = OptionMenu(root, myoptlist, *myitems, command=option_changed)
                widget.config(indicatoron=0, compound='right', highlightthickness=0, bg="thistle", relief=FLAT)
                widget.place(relwidth=0.1, relheight=0.065, relx=0.515, rely=0.15)
            else:
                pass
        for rngitem, item in enumerate(items4):
            if rngitem == 0:
                global widgetcomb1
                widgetcomb1 = ttk.Combobox(root, state='readonly')
                widgetcomb1['values'] = ["csv", "txt", "xlsx", "xlsm", "xls"]
                widgetcomb1.pack(side=TOP, anchor=W)
                widgetcomb1.place(relwidth=0.1, relheight=0.03, relx=0.02, rely=0.40)
                root.bind('<<ComboboxSelected>>', callback_function1)
            else:
                pass
    else:
        messagebox.showinfo("-- ERROR --", "Please enter valid infomation!", icon="warning")

# Change Pass/User
def themaindef():
    global window, textentry, textentry2
    if window:
        window.destroy()
        window = Toplevel()
        window.overrideredirect(False)
        # info for windows placement on the screen
        w = 820
        h = 550
        ws = window.winfo_screenwidth()  # width of the screen
        hs = window.winfo_screenheight()  # height of the screen
        # calculate x and y coordinates for the Tk root window
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        window.title("RDA ML Tool")
        window.configure(background="pink")
        window.geometry('%dx%d+%d+%d' % (w, h, x, y))
        window.iconbitmap(resource_path(r'myicon.ico'))
        # add background
        window.bind("<Return>", lambda X: try_login(username, password))
        # create the window
        window.columnconfigure(0, weight=1)  # Which column should expand with window
        window.rowconfigure(0, weight=1)  # Which row should expand with window
        appw = FullScreenApp(window)
        items = [{'x': 300, 'y': 100},
                 {'x': 300, 'y': 120}]
        items2 = [{'text': 'Login', 'x': 260, 'y': 160},
                  {'text': 'Quit', 'x': 340, 'y': 160},
                  {'text': 'Change\n Credentials', 'x': 420, 'y': 160}]
        items3 = [{'text': 'Username', 'x': 380, 'y': 100},
                  {'text': 'Password', 'x': 380, 'y': 120}]
        photo4 = PhotoImage(file=resource_path(r"mymoon.gif"))
        canvas = Canvas(window, bg="khaki")  # To see where canvas is
        canvas.create_image(0, 0, image=photo4, anchor="nw")
        canvas.pack(fill=BOTH, expand=1)
        for rngitem, item in enumerate(items):
            if rngitem == 0:
                widget = Entry(window, show="*")
                # Place widget on canvas with: create_window
                canvas.create_window(item['x'], item['y'], anchor=NW,
                                     height=15, width=70, window=widget)
                textentry = widget
                textentry.focus_set()
            elif rngitem == 1:
                widget = Entry(window, show="*")
                # Place widget on canvas with: create_window
                canvas.create_window(item['x'], item['y'], anchor=NW,
                                     height=15, width=70, window=widget)
                textentry2 = widget
            else:
                pass
        for rngitem, item in enumerate(items3):
            if rngitem == 0:
                widget = Label(window, text=item['text'])
                # Place widget on canvas with: create_window
                canvas.create_window(item['x'], item['y'], anchor=NW,
                                     height=15, width=70, window=widget)
            elif rngitem == 1:
                widget = Label(window, text=item['text'])
                # Place widget on canvas with: create_window
                canvas.create_window(item['x'], item['y'], anchor=NW,
                                     height=15, width=70, window=widget)
            else:
                pass
        for rngitem, item in enumerate(items2):
            if rngitem == 0:
                widget = HoverButton(window, text=item['text'], height=4, width=40, bg="lightblue",
                                     command=combine_funcs(thismysound, lambda: try_login(username, password)))
                # Place widget on canvas with: create_window
                canvas.create_window(item['x'], item['y'], anchor=NW,
                                     height=30, width=70, window=widget)
            elif rngitem == 1:
                widget = HoverButton(window, text=item['text'], height=4, width=40, bg="lightblue",
                                     command=combine_funcs(thismysound,window.destroy))
                # Place widget on canvas with: create_window
                canvas.create_window(item['x'], item['y'], anchor=NW,
                                     height=30, width=70, window=widget)
            elif rngitem == 2:
                widget = HoverButton(window, text=item['text'], height=4, width=40, bg="lightblue",
                                     command=combine_funcs(thismysound,change_login))
                # Place widget on canvas with: create_window
                canvas.create_window(item['x'], item['y'], anchor=NW,
                                     height=30, width=70, window=widget)
            else:
                pass
        window.mainloop()
    else:
        window = Toplevel()
        window.overrideredirect(False)
        # info for windows placement on the screen
        w = 820  # width for the Tk root
        h = 550  # height for the Tk root
        # get screen width and height
        ws = window.winfo_screenwidth()  # width of the screen
        hs = window.winfo_screenheight()  # height of the screen
        # calculate x and y coordinates for the Tk root window
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        window.title("RDA ML Tool")
        window.configure(background="pink")
        window.geometry('%dx%d+%d+%d' % (w, h, x, y))
        window.iconbitmap(resource_path(r'myicon.ico'))
        # add background
        window.bind("<Return>", lambda x: try_login(username, password))
        # create the window
        window.columnconfigure(0, weight=1)  # Which column should expand with window
        window.rowconfigure(0, weight=1)  # Which row should expand with window
        appw = FullScreenApp(window)

        items = [{'x': 300, 'y': 100},
                 {'x': 300, 'y': 120}]
        items2 = [{'text': 'Login', 'x': 260, 'y': 160},
                  {'text': 'Quit', 'x': 340, 'y': 160},
                  {'text': 'Change\n Credentials', 'x': 420, 'y': 160}]
        items3 = [{'text': 'Username', 'x': 380, 'y': 100},
                  {'text': 'Password', 'x': 380, 'y': 120}]
        photo4 = PhotoImage(file=resource_path(r"mymoon.gif"))
        canvas = Canvas(window, bg="khaki")  # To see where canvas is
        canvas.create_image(0, 0, image=photo4, anchor="nw")
        canvas.pack(fill=BOTH, expand=1)
        for rngitem, item in enumerate(items):
            if rngitem == 0:
                widget = Entry(window, show="*")
                # Place widget on canvas with: create_window
                canvas.create_window(item['x'], item['y'], anchor=NW,
                                     height=15, width=70, window=widget)
                textentry = widget
                textentry.focus_set()
            elif rngitem == 1:
                widget = Entry(window, show="*")
                # Place widget on canvas with: create_window
                canvas.create_window(item['x'], item['y'], anchor=NW,
                                     height=15, width=70, window=widget)
                textentry2 = widget
            else:
                pass

        for rngitem, item in enumerate(items3):
            if rngitem == 0:
                widget = Label(window, text=item['text'])
                # Place widget on canvas with: create_window
                canvas.create_window(item['x'], item['y'], anchor=NW,
                                     height=15, width=70, window=widget)
            elif rngitem == 1:
                widget = Label(window, text=item['text'])
                # Place widget on canvas with: create_window
                canvas.create_window(item['x'], item['y'], anchor=NW,
                                     height=15, width=70, window=widget)
            else:
                pass

        for rngitem, item in enumerate(items2):
            if rngitem == 0:
                widget = HoverButton(window, text=item['text'], height=4, width=40, bg="lightblue",
                                     command=combine_funcs(thismysound, lambda: try_login(username, password)))
                # Place widget on canvas with: create_window
                canvas.create_window(item['x'], item['y'], anchor=NW,
                                     height=30, width=70, window=widget)
            elif rngitem == 1:
                widget = HoverButton(window, text=item['text'], height=4, width=40, bg="lightblue",
                                     command=combine_funcs(thismysound, window.destroy))
                # Place widget on canvas with: create_window
                canvas.create_window(item['x'], item['y'], anchor=NW,
                                     height=30, width=70, window=widget)
            elif rngitem == 2:
                widget = HoverButton(window, text=item['text'], height=4, width=40, bg="lightblue",
                                     command=combine_funcs(thismysound,change_login))
                # Place widget on canvas with: create_window
                canvas.create_window(item['x'], item['y'], anchor=NW,
                                     height=30, width=70, window=widget)
            else:
                pass
        window.mainloop()

#---------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------
# Change Pass/User
def change_login():
    global e1, e2, e3, e4, e5, e6, root6
    root6 = Toplevel()
    # info for windows placement on the screen
    root6.overrideredirect(False)
    w = 820
    h = 550
    ws = root6.winfo_screenwidth()  # width of the screen
    hs = root6.winfo_screenheight()  # height of the screen
    # calculate x and y coordinates for the Tk root window
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    # info for windows placement on the screen
    root6.title("Updating Details")
    root6.configure(background=belcolors[0])
    root6.geometry('%dx%d+%d+%d' % (w, h, x, y))
    root6.iconbitmap(resource_path(r'myicon.ico'))
    root6.bind("<Return>", lambda x: login_in())
    # create the window
    root6.columnconfigure(0, weight=1)  # Which column should expand with window
    root6.rowconfigure(0, weight=1)  # Which row should expand with window
    app6 = FullScreenApp(root6)
    items = [{'x': 400, 'y': 100},
             {'x': 400, 'y': 120},
             {'x': 400, 'y': 140},
             {'x': 400, 'y': 160},
             {'x': 400, 'y': 180},
             {'x': 400, 'y': 200}]
    items2 = [{'text': 'Existing User', 'x': 320, 'y': 100},
             {'text': 'Existing Pass', 'x': 320, 'y': 120},
             {'text': 'New User', 'x': 320, 'y': 140},
             {'text': 'New Pass', 'x': 320, 'y': 160},
             {'text': 'Confirm User', 'x': 320, 'y': 180},
             {'text': 'Confirm Pass', 'x': 320, 'y': 200}]
    items3 = [{'text': 'Save', 'x': 320, 'y': 220},
              {'text': 'Back', 'x': 420, 'y': 220}]
    photo3 = PhotoImage(file=resource_path(r"stars.gif"))
    canvas = Canvas(root6, bg="khaki")  # To see where canvas is
    canvas.create_image(0, 0, image=photo3, anchor="nw")
    canvas.pack(fill=BOTH, expand=1)
    for rngitem, item in enumerate(items):
        if rngitem==0:
            widget = Entry(root6, show="*")
        # Place widget on canvas with: create_window
            canvas.create_window(item['x'], item['y'], anchor=NW,
                                 height=15, width=70, window=widget)
            e1=widget
        elif rngitem==1:
            widget = Entry(root6, show="*")
            # Place widget on canvas with: create_window
            canvas.create_window(item['x'], item['y'], anchor=NW,
                                 height=15, width=70, window=widget)
            e2=widget
        elif rngitem==2:
            widget = Entry(root6, show="*")
            # Place widget on canvas with: create_window
            canvas.create_window(item['x'], item['y'], anchor=NW,
                                 height=15, width=70, window=widget)
            e3=widget
        elif rngitem==3:
            widget = Entry(root6, show="*")
            # Place widget on canvas with: create_window
            canvas.create_window(item['x'], item['y'], anchor=NW,
                                 height=15, width=70, window=widget)
            e4 = widget
        elif rngitem==4:
            widget = Entry(root6, show="*")
            # Place widget on canvas with: create_window
            canvas.create_window(item['x'], item['y'], anchor=NW,
                                 height=15, width=70, window=widget)
            e5 = widget
        elif rngitem==5:
            widget = Entry(root6, show="*")
            # Place widget on canvas with: create_window
            canvas.create_window(item['x'], item['y'], anchor=NW,
                                 height=15, width=70, window=widget)
            e6 = widget
        else:
            pass

    for rngitem, item in enumerate(items2):
        if rngitem == 0:
            widget = Label(root6, text=item['text'])
            # Place widget on canvas with: create_window
            canvas.create_window(item['x'], item['y'], anchor=NW,
                                 height=15, width=70, window=widget)
        elif rngitem == 1:
            widget = Label(root6, text=item['text'])
            # Place widget on canvas with: create_window
            canvas.create_window(item['x'], item['y'], anchor=NW,
                                 height=15, width=70, window=widget)
        elif rngitem == 2:
            widget = Label(root6, text=item['text'])
            # Place widget on canvas with: create_window
            canvas.create_window(item['x'], item['y'], anchor=NW,
                                 height=15, width=70, window=widget)
        elif rngitem == 3:
            widget = Label(root6, text=item['text'])
            # Place widget on canvas with: create_window
            canvas.create_window(item['x'], item['y'], anchor=NW,
                                 height=15, width=70, window=widget)
        elif rngitem == 4:
            widget = Label(root6, text=item['text'])
            # Place widget on canvas with: create_window
            canvas.create_window(item['x'], item['y'], anchor=NW,
                                 height=15, width=70, window=widget)
        elif rngitem == 5:
            widget = Label(root6, text=item['text'])
            # Place widget on canvas with: create_window
            canvas.create_window(item['x'], item['y'], anchor=NW,
                                 height=15, width=70, window=widget)
        else:
            pass

    for rngitem, item in enumerate(items3):
        if rngitem == 0:
            widget = HoverButton(root6, text=item['text'],height=3, width=15, bg="lightblue", command=combine_funcs(thismysound, login_in, root6.destroy))
            # Place widget on canvas with: create_window
            canvas.create_window(item['x'], item['y'], anchor=NW,
                                 height=15, width=70, window=widget)
        elif rngitem == 1:
            widget = HoverButton(root6, text=item['text'], height=3, width=15, bg="lightblue",
                                 command=combine_funcs(thismysound, root6.destroy))
            # Place widget on canvas with: create_window
            canvas.create_window(item['x'], item['y'], anchor=NW,
                                 height=15, width=70, window=widget)
        else:
            pass
        root6.mainloop()

# password
if not os.path.isfile("passd.txt"):
    now = open("passd.txt", "w+")
    now.write("dar\n")
    now.write("bla")
    now.close()

def login_in():
    with open("passd.txt") as f:
        new = f.readlines()
        username = new[0].rstrip()
        password = new[1].rstrip()
    if e1.get() == username and e2.get() == password and e3.get()==e5.get() and e4.get()==e6.get():
        data = e3.get() + "\n" + e4.get()  # removed space after \n
        with open("passd.txt", "w") as f:
            f.writelines(data)
        root6.destroy()
    else:
        root6.destroy()
        messagebox.showerror("error", "login Failed")

#---------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
window = Toplevel()
# info for windows placement on the screen
w = 820  # width for the Tk root
h = 550  # height for the Tk root
# get screen width and height
ws = window.winfo_screenwidth()  # width of the screen
hs = window.winfo_screenheight()  # height of the screen
# calculate x and y coordinates for the Tk root window
x = (ws / 2) - (w / 2)
y = (hs / 2) - (h / 2)
window.title("RDA ML Tool")
window.configure(background="pink")
window.geometry('%dx%d+%d+%d' % (w, h, x, y))
window.iconbitmap(resource_path(r'myicon.ico'))
window.bind("<Return>", lambda x: try_login(username, password))
# add background
window.columnconfigure(0, weight=1)  # Which column should expand with window
window.rowconfigure(0, weight=1)  # Which row should expand with window
appw = FullScreenApp(window)
items = [{'x':300, 'y': 100},
         {'x': 300, 'y': 120}]
items2 = [{'text': 'Username', 'x': 380, 'y': 100},
         {'text': 'Password', 'x': 380, 'y': 120}]
items3 = [{'text': 'Login', 'x': 260, 'y': 160},
          {'text': 'Quit', 'x': 340, 'y': 160},
          {'text': 'Change\n User/Pass', 'x': 420, 'y': 160}]
photo3 = PhotoImage(file=resource_path(r"stars2.gif"))
canvas = Canvas(window, bg="khaki")  # To see where canvas is
canvas.create_image(0, 0, image=photo3, anchor="nw")
canvas.pack(fill=BOTH, expand=1)
for rngitem, item in enumerate(items2):
    if rngitem==0:
        widget = Label(window, text=item['text'], bg="pink", fg="white", font="none 8 bold")
    # Place widget on canvas with: create_window
        canvas.create_window(item['x'], item['y'], anchor=NW,
                             height=15, width=70, window=widget)
    elif rngitem==1:
        widget = Label(window, text=item['text'], bg="pink", fg="white", font="none 8 bold")
        # Place widget on canvas with: create_window
        canvas.create_window(item['x'], item['y'], anchor=NW,
                             height=15, width=70, window=widget)
    else:
        pass

for rngitem, item in enumerate(items):
    if rngitem==0:
        widget = Entry(window, width=12, bg="white", show="*")
        # Place widget on canvas with: create_window
        canvas.create_window(item['x'], item['y'], anchor=NW,
                             height=15, width=70, window=widget)
        textentry = widget
        textentry.focus_set()
    elif rngitem==1:
        widget = Entry(window, width=12, bg="white", show="*")
        # Place widget on canvas with: create_window
        canvas.create_window(item['x'], item['y'], anchor=NW,
                             height=15, width=70, window=widget)
        textentry2 = widget
    else:
        pass

for rngitem, item in enumerate(items3):
    if rngitem==0:
        widget = HoverButton(window, text=item['text'],height=4, width=40, bg="lightblue", command= combine_funcs(thismysound, lambda: try_login(username, password)))
        # Place widget on canvas with: create_window
        canvas.create_window(item['x'], item['y'], anchor=NW,
                             height=30, width=70, window=widget)
    elif rngitem==1:
        widget = HoverButton(window, text=item['text'],height=4, width=40, bg="lightblue", command=combine_funcs(thismysound, window.destroy))
        # Place widget on caanvas with: create_window
        canvas.create_window(item['x'], item['y'], anchor=NW,
                             height=30, width=70, window=widget)
    elif rngitem==2:
        widget = HoverButton(window, text=item['text'],height=4, width=40, bg="lightblue", command=combine_funcs(thismysound, change_login))
        # Place widget on canvas with: create_window
        canvas.create_window(item['x'], item['y'], anchor=NW,
                             height=30, width=70, window=widget)
    else:
        pass
window.mainloop()