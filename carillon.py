#!/usr/bin/env python

# John Memmeling and John Van Eyck
# Hold state at Bruges. In sore shame
# I scanned the works that keep their name.
# The Carillon, which then did strike
# Mine ears, was heard of theirs alike:
# It set me closer unto them.
# - The Carillon, Dante Gabriel Rossetti

# Two roads diverged in a yellow wood,
# and sorry I could not travel both,
# and be one traveler, long I stood
# and looked down one as far as I could
# and wrote a carillon in Python.
# - Me

#External settings
import settings

#External modules
import os #includes path, listdir
import sys
import time #includes asctime, localtime
import subprocess
from subprocess import call #synchronous
from subprocess import Popen #asynchronous
from datetime import datetime

def getScriptPath():
    #http://stackoverflow.com/a/4943474
    return os.path.dirname(os.path.realpath(sys.argv[0]))

# TODO: consider extra output to trigger an auxiliary bell system / striker?

#MIDI stuff
midiProcess = False
midiProgram = []

def buildProgram():
    global midiProgram
    midiFiles = os.listdir(settings.midiPath)
    midiProgram = []
    for i in range(0,len(midiFiles)):
        #Parse files in settings.midiPath (settings.py). Per description there:
            # To be included in the program, MIDI files in settings.midiPath should be formatted as [time][-description].mid
            # where [time] is [[N]d][[N]h][[N]m][[N]s]. If [N] is omitted it means "every"
            # If description includes the word "stroke" (case sensitive), it will be repeated per current hour
        #Each program item will be a 6-tuple comprising weekday, hour, minute, second, stroke flag, and midi file name.
        
        fTest = midiFiles[i].split('.')
        if(fTest[len(fTest)-1]=='mid'): #it's a midi file, proceed
            #we only want to test the time part. If there's a hyphen, discard all after that for now.
            fTest = fTest[0].split('-')[0]
            #if it's empty, or includes an 'n', skip this file
            if(len(fTest.split('n')) > 1 or fTest==''): continue
            #Extract time values
            fD = fTest.split('d')
            fH = fD[len(fD)-1].split('h')
            fM = fH[len(fH)-1].split('m')
            fS = fM[len(fM)-1].split('s')
            if len(fD)>1: fD = fD[0] #a hit on explicit day of the week
            else: fD=-1
            if len(fH)>1: fH = fH[0] #a hit on explicit hours
            else: fH=-1
            if len(fM)>1: fM = fM[0] #minutes
            else: fM=-1
            if len(fS)>1: fS = fS[0] #seconds
            else: fS=-1
            #At this point, '' = every, larger -1 = every, smaller -1 = 0
            #Sanitize to no strings, -1 = every, explicit 0s
            if(fD!=-1):
                if(fD==''): fD=-1
                else: fD=int(fD) #neither -1 nor an empty string - a real value - cast to int
                if(fH==-1): fH=0 #zero smaller values, if unspecified
                if(fM==-1): fM=0
                if(fS==-1): fS=0
            if(fH!=-1):
                if(fH==''): fH=-1
                else: fH=int(fH)
                if(fM==-1): fM=0
                if(fS==-1): fS=0
            if(fM!=-1):
                if(fM==''): fM=-1
                else: fM=int(fM)
                if(fS==-1): fS=0
            if(fS!=-1):
                if(fS==''): fS=-1
                else: fS=int(fS)
            #Is this a stroke?
            fStr = False
            if(midiFiles[i].find('stroke') != -1 or midiFiles[i].find('strike') != -1): fStr = True
            midiProgram.append( (fH,fM,fS,fStr,midiFiles[i]) )
        #end if it's a midi file
    #end for each file
    #sort the list by second, then minute, then hour descending
    #Highest priority (top of the list) should be later, non-repeating (since repeat is -1), higher unit
    midiProgram.sort(key=lambda x: (x[0],x[1],x[2]), reverse=True)
    
    #Print results
    print("Program built from "+settings.midiPath+" with "+str(len(midiProgram))+" item(s)")
    #for i in range(0,len(midiProgram)): print(midiProgram[i])
#end def buildProgram

def midiStop():
    global midiProcess
    if(midiProcess != False and midiProcess.poll() is None):
        midiProcess.terminate()
        #http://askubuntu.com/a/565566/531496
        call(['amidi','-p',settings.midiHWPort,'-S','f07e7f0901f7'])
    # midiProcess = Popen(['aplaymidi','-p',str(settings.midiPort),midiStopFile])
    # time.sleep(0.05)
    # midiProcess.terminate()
#end def midiStop

#Let's go!
try:
    print("Carillon running. Press Ctrl+C to stop.");

    buildProgram()

    strikingFile = False #when striking, holds midi filename
    strikingSecs = -1
    strikingDelay = 3
    strikingCount = 0

    lastSecond = -1
    while 1:
        #important to snapshot current time, so test and assignment use same time value
        nowTime = datetime.now()
        if lastSecond != nowTime.second:
            if nowTime.hour < settings.silentHours[0] and nowTime.hour >= settings.silentHours[1]:
                #take care of MIDI first to minimize delay in starting to play
                #list comprehension is amazing. I owe http://stackoverflow.com/a/2917388 a beer or two
                if(strikingFile == False): #if we're not striking, look for a chime or strike file for this moment
                    midiMatches = [i for i, v in enumerate(midiProgram) if ((v[0]==nowTime.hour or v[0]==-1) and (v[1]==nowTime.minute or v[1]==-1) and (v[2]==nowTime.second or v[2]==-1))]
                    #print(nowTime)
                    #print(midiProgram)
                    #print(midiMatches)
                    if(len(midiMatches)>0):
                        print("At "+str(nowTime.hour)+":"+str(nowTime.minute)+":"+str(nowTime.second)+", found "+str(len(midiMatches))+" midi matches! Best match: "+str(midiProgram[midiMatches[0]]))
                        if(midiProgram[midiMatches[0]][3] == True): #all aboard the strike train #horologyjoke #ahaha
                            strikingFile = midiProgram[midiMatches[0]][4];
                        else: #just a regular chime
                            if(midiProcess == False or midiProcess.poll() is not None): #don't stop a chime already in progress
                                midiProcess = Popen(['aplaymidi','-p',str(settings.midiPort),settings.midiPath+'/'+midiProgram[midiMatches[0]][4]])
                        #end strike vs chime test
                    #end if we found a midi match
                #end if not striking
            
                if(strikingFile != False): #are we on the strike train?
                    strikingSecs += 1
                    if strikingSecs == strikingDelay*strikingCount: #is it time for a stroke?
                        midiStop() #stop chime or stroke already sounding, if any
                        midiProcess = Popen(['aplaymidi','-p',str(settings.midiPort),settings.midiPath+'/'+strikingFile])
                        strikingCount += 1
                        if(strikingCount == ((nowTime.hour-1)%12)+1): #the strike train has reached the station. mind the gap. (this fancy math converts 24h to 12h)
                            strikingFile = False
                            strikingCount = 0
                            strikingSecs = -1
                        #end if done with striking
                    #end if it's time for a strike
                #end if striking
            #end if within striking time (not silent hours)
            
            #A few things we'd like to do at less frequent intervals
            if(nowTime.second==1):
                buildProgram() #check for updates
            
            lastSecond = nowTime.second
        #end if new second
        time.sleep(0.05)
    #end while            
#except AttributeError: #Easier to ask forgiveness than permission (EAFP) - http://stackoverflow.com/a/610923
    #print("\r\nAttributeError. Please ensure your settings.py includes all items from settings-sample.py.")
except KeyboardInterrupt:
    print("\r\nBye!")
#except:
    #print("Error")
finally:
    midiStop()
#end try/except/finally