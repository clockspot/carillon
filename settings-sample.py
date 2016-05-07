# MIDI info
midiPort = 20 #Use aplaymidi -l to find yours. (Luckily I own an Edirol UM-1 which is natively supported.)
midiHWPort = 'hw:1' #Use amidi -l to find yours
midiPath = "./midi/westminster"
# This default will only work if carillon is run from its own directory. Absolute path recommended.
# See README.md for details on how to provide MIDI files to be added to the chime program.

silentHours = (22,7) #Do not send any MIDI after X (inclusive) or before X (exclusive)
#For more fine-grained control over silent times, duplicate midi files and set them to trigger at specific times.