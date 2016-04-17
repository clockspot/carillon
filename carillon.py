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

print("Carillon starting.");

#External modules
import RPi.GPIO as GPIO
import os
#from os import path
#from os import listdir
import sys
import time
#from time import asctime, localtime
#from time import localtime
import subprocess
from subprocess import call #synchronous
from subprocess import Popen #asynchronous
from datetime import datetime

#External settings
import settings

# http://stackoverflow.com/a/4943474
def getScriptPath():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

#Hardware stuff - Broadcom pin definitions
clockPin = 20 #trigger external circuit to advance slave clock #TODO correction mechanisms
meterPin = 18 #pwm to control moving-coil galvanometer (3VDC) as seconds display

#MIDI stuff
midiStopFile = getScriptPath() + "/alloff.mid" 
midiProcess = False
midiProgram = []

def buildProgram():
    midiFiles = os.listdir(settings.midiPath)
    midiProgram = []
    for i in range(0,len(midiFiles)):
        #Parse files in settings.midiPath (settings.py). Per description there:
            # To be included in the program, MIDI files in settings.midiPath should be formatted as [time][-description].mid
            # where [time] is [[N]h][[N]m][[N]s]. If [N] is omitted it means "every"
            # If description includes the word "stroke" (case sensitive), it will be repeated per current hour
        #Each program item will be a 5-tuple comprising hour, minute, second, stroke flag, and midi file name.
        
        fTest = midiFiles[i].split('.')
        if(fTest[len(fTest)-1]=='mid'): #it's a midi file, proceed
            #we only want to test the time part. If there's a hyphen, discard all after that for now.
            fTest = fTest[0].split('-')[0]
            #if it's empty, or includes an 'n', skip this file
            if(len(fTest.split('n')) > 1 or fTest==''): continue
            #Extract time values
            fH = fTest.split('h')
            fM = fH[len(fH)-1].split('m')
            fS = fM[len(fM)-1].split('s')
            if len(fH)>1: fH = fH[0] #a hit on explicit hours
            else: fH=-1
            if len(fM)>1: fM = fM[0] #minutes
            else: fM=-1
            if len(fS)>1: fS = fS[0] #seconds
            else: fS=-1
            #At this point, '' = every, larger -1 = every, smaller -1 = 0
            #Sanitize to no strings, -1 = every, explicit 0s
            if(fH!=-1):
                if(fH==''): fH=-1
                else: fH=int(fH) #neither -1 nor an empty string - a real value - cast to int
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

def convertValueToDC(valNew):
    dcNew = 0
    #Which calibration range does valNew fall into?
    for i in range(0, len(settings.meterCal)):
        #If it falls in this one, or in/past the last one:
        if(valNew < settings.meterCal[i][0] or i == len(settings.meterCal)-1):
            valMax = settings.meterCal[i][0]
            valMin = 0
            dcMax = settings.meterCal[i][1]
            dcMin = 0
            #if valNew < first calibration point (indicated by i==0), lower bound is assumed calibration point of (0,0)
            if i > 0: #if valNew > first calibration point, set lower bound to previous calibration point
                valMin = settings.meterCal[i-1][0]
                dcMin = settings.meterCal[i-1][1]
            #Map new value. Not sure if I've reduced this as far as it can go mathwise.
            #print ("i="+str(i)+", valNew="+str(valNew)+", valMax="+str(valMax)+", valMin="+str(valMin)+", dcMax="+str(dcMax)+", dcMin="+str(dcMin))
            return float(dcMax-dcMin)*(float(valNew-valMin)/(valMax-valMin)) + dcMin
        #end found calibration range
    #end for each calibration range
#end def convertValueToDC

def updateMeter(valNew):
    #We will probably set it to valNew, but there may be some statuses to display instead.
    #if(no network connection): setMeter(10)
    if(clockProcess != False and clockProcess.poll() is None): setMeter(30) #to indicate clock is moving
    #elif(no network connection): setMeter(10)
    #elif(bad ntp): setMeter(20)
    else: setMeter(valNew)
#end def updateMeter

dcLast = 0
meterLag = 0.18 #seconds between ballistics steps
def setMeter(valNew):
    #pwm must already have been started
    global dcLast #otherwise the fact that we set dcLast inside this function would make python complain
    dcNew = convertValueToDC(valNew) #find new dc
    if dcNew > 100: dcNew = 100 #apply range limits
    if dcNew < 0: dcNew = 0
    #set meter, using ballistics if dcChg is great enough
    dcChg = dcNew-dcLast    
    if(abs(dcChg) > 10): #apply ballistics
        #easing out equations by Robert Penner - gizma.com/easing
        steps = 4
        for t in range(1, steps+1):
            #quadratic t^2
            t /= float(steps)
            nowDC = float(-dcChg) * t * (t-2) + dcLast
            pwm.ChangeDutyCycle( nowDC )
            if(t<steps):
                time.sleep(meterLag)
    else: #just go to there
        pwm.ChangeDutyCycle(dcNew)
    dcLast = dcNew
#end def setMeter

def midiStop():
    global midiProcess
    if(midiProcess != False and midiProcess.poll() is None):
        midiProcess.terminate() #not kill you, sir, never kill you!...
    midiProcess = Popen(['aplaymidi','-p',str(settings.midiPort),midiStopFile])
    # time.sleep(0.05)
    # midiProcess.terminate()
#end def midiStop

def to12Hr(hr):
    if hr == 0: return 12
    elif hr > 12: return hr-12
    else: return hr
#end def to12Hr

clockProcess = False
#TODO add clockCalibrate.py, clockLast.txt (in .gitignore), and clockAdvance.py
def updateClock():
    global clockProcess
    if(clockProcess != False and clockProcess.poll() is None):
        midiProcess.terminate() #not kill you, sir, never kill you!
    midiProcess = Popen(['aplaymidi','-p',str(settings.midiPort),midiStopFile])
    #call clockAdvance - it should advance the clock immediately, then check to see if it needs to go further per clockLast.txt
    #this can even be done at 29/59 
    # GPIO.output(clockPin, GPIO.HIGH)
    # time.sleep(0.3)
    # GPIO.output(clockPin, GPIO.LOW)
#end def updateClock

#Let's go!

#Pin setup
GPIO.setmode(GPIO.BCM)
#outputs
GPIO.setup(clockPin, GPIO.OUT)
GPIO.setup(meterPin, GPIO.OUT)
pwm = GPIO.PWM(meterPin, 50)
pwm.start(0)

#MIDI and timing setup
buildProgram()
midiStop() #initializes midiProcess to a process
updateClock()

print("Carillon running. Press Ctrl+C to stop.");

lastSecond = -1
nowTime = datetime.now()
strikingFile = False #when striking, holds midi filename
strikingSecs = 0
strikingDelay = 3
strikingCount = 0
try:
    while 1:
        #important to snapshot current time, so test and assignment use same time value
        nowTime = datetime.now()
        if lastSecond != nowTime.second:
            #take care of MIDI first to minimize delay in starting to play
            #list comprehension is amazing. I owe http://stackoverflow.com/a/2917388 a beer or two
            if(strikingFile == False): #if we're not striking, look for a chime or strike file for this moment                
                midiMatches = [i for i, v in enumerate(midiProgram) if ((v[0]==nowTime.hour or v[0]==-1) and (v[1]==nowTime.minute or v[1]==-1) and (v[2]==nowTime.second or v[2]==-1))]
                if(len(midiMatches)>0):
                    #print("Found midi matches! "+str(midiMatches)+"  Best match: "+str(midiProgram[midiMatches[0]]))
                    if(midiProgram[midiMatches[0]][3] == True): #all aboard the strike train #horologyjoke #ahaha
                        strikingFile = midiProgram[midiMatches[0]][4];
                    else: #just a regular chime
                        if(midiProcess.poll() is not None): #don't stop a chime already in progress
                            midiProcess = Popen(['aplaymidi','-p',str(settings.midiPort),settings.midiPath+'/'+midiProgram[midiMatches[0]][4]])
                    #end strike vs chime test
                #end if we found a midi match
            #end if not striking
            
            if(strikingFile != False): #are we on the strike train?
                if countSeconds == strokeDelay*strokesDone: #is it time for a stroke?
                    midiStop() #stop chime or stroke already sounding, if any
                    midiProcess = Popen(['aplaymidi','-p',str(settings.midiPort),settings.midiPath+'/'+strikingFile])
                    strikingCount += 1
                    strikingSecs += 1
                    if(strikingCount == to12Hr(nowTime.hour)): #the strike train has reached the station. mind the gap.
                        strikingFile = False
                        strikingCount = 0
                        strikingSecs = 0
                    #end if done with striking
                #end if it's time for a strike
            #end if striking
            
            #A few things we'd like to do at less frequent intervals
            if(nowTime.second==0 or nowTime.second==30):
                updateClock()
            
            #Finally, update the meter - the last thing where real time is important
            updateMeter(nowTime.second)

            #Now some non-realtime stuff
            if(nowTime.second==1):
                buildProgram() #check for updates
            
            #TODO check for ntp status on minute changes?
            #ntpq -c rv | grep "reftime" with result e.g.
            #reftime=dabcecde.167297c4  Sat, Apr 16 2016 11:54:54.087,
            #reftime=00000000.00000000  Sat, Apr 16 2016 11:54:54.087,
            
            lastSecond = nowTime.second
        #end if new second
        time.sleep(0.05)
    #end while            
except KeyboardInterrupt:
    print("\r\nBye!")
# except:
#     print("Error")
finally:
    if dcLast > 20: #kill the meter softly
        setMeter(0)
    midiStop()
    GPIO.output(clockPin, GPIO.LOW)
    pwm.stop()
    GPIO.cleanup()
#end try/except/finally