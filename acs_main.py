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
import mfcc.py as mfcc
from subprocess import Popen, PIPE


songlist = []
songnames = []
host = object()
songindex = 0
currentsong = ""
currentsonglabel = Label()
workingdir = ""

class App(Tk):
	var = None
	def __init__(self,*args,**kwargs):
		Tk.__init__(self, *args, **kwargs)
		self.var1 = StringVar()
		container = Frame(self)
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		self.frames = {}
		for F in (Root, ACSFrame):
			frame = F(container,self)
			self.frames[F] = frame 
			frame.grid(row=0,column=0,sticky="nsew")
		global currentsong
		print(currentsong)
		self.var1.set(currentsong)

		self.show_frame(Root)

	def show_frame(self, context):
		frame = self.frames[context]
		currentframe = frame
		frame.tkraise()

class Root(Frame):

	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		label = Label(self, text = 'Music Player')
		label.pack()
		var1 = controller.var1

		global currentsong
		global songindex
		global songlist	 

		currentsonglabel = Label(self,textvariable=var1, width=35)
		currentsonglabel.pack()
		
		listbox = Listbox(self)
		listbox.pack()

		for songs in songlist:
			listbox.insert(-1,songs)

		nextbutton = Button(self,text = "Next Song")
		nextbutton.pack()

		play = Button(self, text = "Play Song")
		play.pack()

		choosedir = Button(self, text = "Choose Dir")
		choosedir.pack()
		
		compare = Button(self, text = "Compare", command=lambda:controller.show_frame(ACSFrame))
		compare.pack()

		stop = Button(self, text = "Stop Song")
		stop.pack()
		
		previousbutton = Button(self, text = "Previous Song")
		previousbutton.pack()


		nextbutton.bind("<Button-1>",nextsong)
		play.bind("<Button-1>",listentosong)
		choosedir.bind("<Button-1>",runningdirectorychooser)
		stop.bind("<Button-1>",stopsong)
		previousbutton.bind("<Button-1>",previoussong)
		compare.bind("<Button-1>",compare)

	def UpdateCurrentSong(self):
		currentsonglabel.configure(text = currentsong)

class ACSFrame(Frame):

	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		var1 = controller.var1
		label = Label(self, text = 'Comparator Operations')
		label.pack()

		songlabel = Label(self,textvariable=var1, width=35)
		songlabel.pack()
		Home = Button(self, text = "Home", command=lambda:controller.show_frame(Root))
		Home.pack()


		chroma = Button(self, text = "chromagraphsong")
		chroma.pack()

		beat = Button(self, text = "BeatExtraction")
		beat.pack()

		dirGraph = Button(self, text = "Graph all songs")
		dirGraph.pack()
		chroma.bind("<Button-1>",chromagraphsong)
		beat.bind("<Button-1>",beatgraph)
		dirGraph.bind("<Button-1>",featurevisualization)		

def resetup():
	global songindex 
	songindex = 0
	listbox.delete(0,'end')
	for songs in songlist:
		listbox.insert(-1,songs)

def updatecurrentsong():
	global songindex
	global songname
	global currentsong
	currentsong = songlist[songindex]
	print("currentsong:" + currentsong)

def directorychooser():
	global workingdir
	songdirectory = tkFileDialog.askdirectory()
	workingdir = songdirectory
	audioBasicIO.convertDirMP3ToWav(songdirectory, 44100, 2, useMp3TagsAsName=False)
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



directorychooser()
app = App()
app.mainloop() 



