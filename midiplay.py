#!/usr/bin/env python
print("Play MIDI file directly. Ctrl+C to stop. README for more info.");

import settings

#External modules
import sys
import subprocess
from subprocess import call #synchronous
#from subprocess import Popen #asynchronous

midiFile = sys.argv[len(sys.argv)-1] #take last argument
if midiFile.find('.mid') == -1:
    print ("Please specify MIDI file as argument to this script.")
    raise SystemExit
    
midiProcess = False

def midiStop():
    #No need to stop midiProcess, we're doing it synchronously so it will stop first
    call(['amidi','-p',settings.midiHWPort,'-S','f07e7f0901f7'])

try:
    if(midiProcess == False or midiProcess.poll() is not None):
        print ("Playing "+midiFile+" ...")
        midiProcess = call(['aplaymidi','-p',str(settings.midiPort),midiFile])
        print ("Thank you come again.")
except KeyboardInterrupt:
    print("\r\nBye!")
# except:
#     print("Error")
finally:
    midiStop()
#end try/except/finally