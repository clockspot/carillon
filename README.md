# carillon
The Indoor Carillon Project: script for a Raspberry Pi to drive a slave clock and a MIDI instrument on schedule, synced to NTP.

This is very much in progress. At this point I am still gathering the hardware.

## What the what?
I've got a harebrained scheme to build an indoor carillon in two loosely-coupled parts:

### The Clock
The brains of the operation. A Raspberry Pi will make its home inside a lovely 1960s Gents slave clock formerly in the employ of the UK Post Office. It will connect to wifi, sync to NTP, use GPIO pins to drive a small circuit to advance the clock and a 3VDC gauge (via PWM) to display seconds / status, provide administration via SSH or hopefully a webpage (which may also support MIDI via HTML5), and most importantly, output MIDI on predetermined schedules. All this absurdity will be coordinated by the project you hold in your virtual hands.

### The Bells
A small 30-note glockenspiel, to be rigged with small solenoids wired up to a MIDI decoder card from Orgautomatech, which receives input from the Clock. This card is favored because it supports wiring solenoids directly.

## Brought to you by
http://www.orgautomatech.com/ – The intended MIDI decoder card.
https://www.youtube.com/watch?v=UbwfAc0AKhk – A harpsichord driven by the above
http://www.instructables.com/id/Make-an-Atom-Synchronised-Clock-from-a-1950s-Slav/