# carillon
The Indoor Carillon Project: script for a Raspberry Pi to drive a slave clock and a MIDI instrument on schedule, synced to NTP. This is very much in progress.

## What the what?
I've got a harebrained scheme to build an indoor carillon in two loosely-coupled parts:

### The Clock
The brains of the operation. A Raspberry Pi will make its home inside a lovely 1960s Gents slave clock formerly in the employ of the UK Post Office. It will connect to wifi, sync to NTP (by virtue of ntpd), use GPIO pins to drive a small circuit to advance the clock and a 3VDC meter (via PWM) to display seconds / status, provide simple admistration of chime programs via MIDI files, and most importantly, output that MIDI on schedule. All this absurdity will be coordinated by the project you hold in your virtual hands.

**For later:** provide administration via SSH or hopefully a webpage (which may also support MIDI via HTML5)

### The Bells
A small 30-note glockenspiel, to be rigged with small solenoids wired up to [a MIDI decoder card from Orgautomatech](http://www.orgautomatech.com/), which receives input from the Clock. This card is favored because it supports wiring solenoids directly ([example](https://www.youtube.com/watch?v=UbwfAc0AKhk)).

## Files herein
* **carillon.py** - Where the magic happens.
* **settings-sample.py** - Duplicate/rename this to **settings.py** and edit accordingly.
* **meterCalibrate.py** - Use this to calibrate your 3VDC meter.
* **clockCalibrate.py** - *Coming soon.* Use this to tell the Pi what time your slave clock reads (in case it runs, but is wrong).
* **clockAdvance.py** - *Coming soon.* carillon calls this asynchronously to advance the clock to the current time.
* **alloff.mid** - carillon uses this periodically to kill all MIDI notes, in case `aplaymidi` terminates early and leaves notes on. Don't want solenoids to burn out!
* **midi/** - Some common (and not so common) chime programs (see below).

## Chime programs
To be included in the program, MIDI files in the MIDI path (per sample.py) should be formatted as
    [time][-description].mid
where `time` is `[[N]h][[N]m][[N]s]`. If `[N]` is omitted it means "every". Use 24-hour notation. If `description` includes the word "strike" (case sensitive), it will be repeated per the current hour (12-hour clock).

#### Examples:
(Can you tell I'm going a little nuts learning Markdown?)
| Filename                  | Plays how often                   |
|---------------------------|-----------------------------------|
| s-song.mid                | every second                      |
| 30s-song.mid              | at 30s every minute               |
| m-song.mid                | every minute (at 0s)              |
| 15m-song.mid              | at 15m every hour (at 0s)         |
| 59m45s-song.mid           | at 59m 45s every hour             |
| h-song.mid                | every hour (at 0m 0s)             |
| nh-song.mid               | won't play                        |
| -song.mid                 | won't play                        |
| Extension other than .mid | won't play                        |
| why-me.mid                | Will probably crash the script    |
Validation is currently a bit loose. If you have mids that fit the pattern but invalidly, the script may crash. The safest place for .mids you don't want played is in a different folder (such as a subfolder, it'll skip that).

#### Suggested program:
Most of the provided programs follow this pattern.
| Filename          | What                                                                              |
|-------------------|-----------------------------------------------------------------------------------|
| 15m-song.mid      | First quarter chimes                                                              |
| 30m-song.mid      | Second quarter chimes                                                             |
| 45m-song.mid      | Third quarter chimes                                                              |
| 59m40s-song.mid   | Fourth quarter chimes, 20 seconds before top of hour (Big Ben style)              |
| h-stroke.mid      | Hourly strokes, starting at top of hour, repeating per current hour               |

## Ideaphoria!
* [Harpsichord driven by Orgautomatech decoders](https://www.youtube.com/watch?v=UbwfAc0AKhk)
* [Make an Atom Synchronised Clock from a 1950s Slave Clock on Instructables](http://www.instructables.com/id/Make-an-Atom-Synchronised-Clock-from-a-1950s-Slav/)
* [Clock Chime Tunes Reference](http://www.clockguy.com/SiteRelated/SiteReferencePages/ClockChimeTunes.html)
* Various other credits as sprinkled throughout