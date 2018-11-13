from __future__ import print_function
import os
from Tkinter import *
from mutagen.id3 import ID3
import pygame
import tkFileDialog
import subprocess
from pyAudioAnalysis import *
import audioBasicIO
import importlib
import audioFeatureExtraction as afe
import audioAnalysis as aa

from subprocess import Popen, PIPE


songlist = []
songnames = []
host = object()
songindex = 0
currentsong = ""
currentsonglabel = Label()
workingdir = ""






def resetup():
	global songindex 
	songindex = 0
	listbox.delete(0,'end')
	for songs in songlist:
		listbox.insert(-1,songs)
	

def runningdirectorychooser(event):
	songdirectory = tkFileDialog.askdirectory()
	#os.chdir(songdirectory)

	for song in os.listdir(songdirectory):
		if song.endswith(".mp3"):
			truedir = os.path.realpath(song)
			audio = ID3(truedir)
			#songnames.append(audio['TIT2'].text[0])
			songlist.append(song)
			print(song)
	updatecurrentsong()
	resetup()

def directorychooser():
	global workingdir
	songdirectory = tkFileDialog.askdirectory()
	workingdir = songdirectory
	audioBasicIO.convertDirMP3ToWav(songdirectory, 44100, 1, useMp3TagsAsName=False)
	#text = subprocess.check_output(['python','./pyAudioAnalysis/pyAudioAnalysis/audioAnalysis.py', 'dirMp3toWav', '-i', './Musiclist/', '-r 44100', '-c', '1'])
	#python ./pyAudioAnalysis/pyAudioAnalysis/audioAnalysis.py dirMp3toWav -i ./Musiclist/ -r 44100 -c 1
	"""with Popen(['python','./pyAudioAnalysis/pyAudioAnalysis/audioAnalysis.py', 'dirMp3toWav', '-i', './Musiclist/', '-r 44100', '-c', '1'], stdin=PIPE, stdout=PIPE, 
         universal_newlines=True) as p:
	   for line in p.stdout: 
	      if line.endswith("[y/N]"):
	            answer = "y"
	        else:
	            continue # skip it

	        print(answer,file=p.stdin)
	    p.stdin.flush()"""
	print(songdirectory)
	os.chdir(songdirectory)
	for song in os.listdir(songdirectory):
		if song.endswith(".mp3"):
			truedir = os.path.realpath(song)
			audio = ID3(truedir)
			#songnames.append(audio['TIT2'].text[0])
			songlist.append(song)
			print(song)
	updatecurrentsong()
	

def updatecurrentsong():
	global songindex
	global songname
	global currentsong
	currentsong = songlist[songindex]
	print("currentsong:" + currentsong)

#def songchromagram():
	



def listentosong(event):
	global songindex
	pygame.mixer.init()
	pygame.mixer.music.load(songlist[songindex])
	pygame.mixer.music.play()

def nextsong(event): 
	global songindex
	songindex = (songindex + 1) % len(songlist)
	updatecurrentsong()

def previoussong(event):
	global songindex
	songindex = (songindex + 1) % len(songlist)
	updatecurrentsong()

def chromagraphsong(event):
	selectedsong = tkFileDialog.askopenfilename()
	aa.fileChromagramWrapper(selectedsong) 

def beatgraph(event):
	selectedsong = tkFileDialog.askopenfilename()
	aa.beatExtractionWrapper(selectedsong, True)
	

def featurevisualization(event):
	aa.featureVisualizationDirWrapper(workingdir)

def stopsong(event):
	pygame.mixer.music.stop()

def raise_frame(frame):
    frame.tkraise()

root = Tk()

f1 = Frame(root)
f2 = Frame(root)
f3 = Frame(root)
f4 = Frame(root)

for frame in (f1, f2, f3, f4):
    frame.grid(row=0, column=0, sticky='news')

Button(f1, text='Go to frame 2', command=lambda:raise_frame(f2)).pack()
Label(f1, text='FRAME 1').pack()

Label(f2, text='FRAME 2').pack()
Button(f2, text='Go to frame 3', command=lambda:raise_frame(f3)).pack()

Label(f3, text='FRAME 3').pack(side='left')
Button(f3, text='Go to frame 4', command=lambda:raise_frame(f4)).pack(side='left')

Label(f4, text='FRAME 4').pack()
Button(f4, text='Goto to frame 1', command=lambda:raise_frame(f1)).pack()

	
#f1 things
var1 = StringVar()
var1.set(currentsong)

currentsonglabel = Label(f1,textvariable=var1, width=35)
currentsonglabel.pack()
		
listbox = Listbox(f1)


for songs in songlist:
	listbox.insert(-1,songs)

listbox.pack()

nextbutton = Button(f1,text = "Next Song")
nextbutton.pack()

play = Button(f1, text = "Play Song")
play.pack()

choosedir = Button(f1, text = "Choose Dir")
choosedir.pack()

stop = Button(f1, text = "Stop Song")
stop.pack()
		
previousbutton = Button(f1, text = "Previous Song")
previousbutton.pack()

chroma = Button(f2, text = "chromagraphsong")
chroma.pack()

beat = Button(f2, text = "BeatExtraction")
beat.pack()

dirGraph = Button(f2, text = "Graph all songs")
dirGraph.pack()

nextbutton.bind("<Button-1>",nextsong)
play.bind("<Button-1>",listentosong)
choosedir.bind("<Button-1>",runningdirectorychooser)
stop.bind("<Button-1>",stopsong)
previousbutton.bind("<Button-1>",previoussong)
compare.bind("<Button-1>",compare)
chroma.bind("<Button-1>",chromagraphsong)
beat.bind("<Button-1>",beatgraph)
dirGraph.bind("<Button-1>",featurevisualization)

def UpdateCurrentSong(f1):
	currentsonglabel.configure(text = currentsong)

directorychooser()
raise_frame(f1)	

root.mainloop() 



