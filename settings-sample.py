# Path for log. Make sure the files (if present, otherwise the containing directory) are writable by the user that will be running the daemon.
logPath = '/var/log/carillon/carillon.log'
logDebug = False
# Note, you can monitor the log in real time with tail -f [logPath]

# MIDI info
midiPort = 20 #Find with aplaymidi -l
midiHWPort = 'hw:1' #Find with amidi -l
midiPath = "/path/to/midifiles"
# See README.md for details on how to provide MIDI files to be added to the chime program.

# Silent hours: do not send any MIDI between these hours (exclusive). For no silent hours, use False.
silentHours = (22,7)
# The first minute (:00) of the first silent hour is allowed to sound, so any pre-hour chimes aren't left w/o strikes.
# The range can cross a midnight (e.g. 22,7) or not (e.g. 0,7 or 1,7).
# For more fine-grained control over silent times, duplicate midi files and set them to trigger at specific times.

strikingDelay = 3 #Seconds between hourly strokes