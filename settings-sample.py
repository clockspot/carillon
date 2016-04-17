# Meter calibration points, display value vs DC value. Use meterCalibrate.py to find points for your meter.
# This also defines the range of your meter scale. (If it starts at zero, you can omit (0,0), it will be assumed.)
meterCal = [(59,94)] #This default defines a 60-second scale, more or less, on a 3VDC meter (since Pi GPIO is 3.3V).

# MIDI data
midiPort = 20 # ALSA port. I found it via aplaymidi -l (and luckily own an Edirol UM-1 which is natively supported).
midiPath = "./midi/westminster"
# This default will only work if carillon is run from its own directory. Absolute path recommended.
# See README.md for details on how to provide MIDI files to be added to the chime program.