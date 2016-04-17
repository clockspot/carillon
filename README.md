# carillon
The Indoor Carillon Project: script for a Raspberry Pi to drive a slave clock and a MIDI instrument on schedule, synced to NTP. This is very much in progress.

## What the what?
I've got a harebrained scheme to build an indoor carillon in two loosely-coupled parts:

### The Clock
The brains of the operation. A Raspberry Pi will make its home inside a lovely 1960s Gents slave clock formerly in the employ of the UK Post Office. It will connect to wifi, sync to NTP (by virtue of ntpd), use GPIO pins to drive a small circuit to advance the clock and a 3VDC meter (via PWM) to display seconds / status, provide simple admistration of chime programs via MIDI files, and most importantly, output that MIDI on schedule. All this absurdity will be coordinated by the project you hold in your virtual hands.

**For later:** provide detailed administration via SSH or hopefully a webpage (which may also support MIDI via HTML5)

### The Bells
A small 30-note glockenspiel, to be rigged with small solenoids wired up to [a MIDI decoder card from Orgautomatech](http://www.orgautomatech.com/), which receives input from the Clock. This card is favored because it supports wiring solenoids directly ([example](https://www.youtube.com/watch?v=UbwfAc0AKhk)).

Because the only link between the Clock and Bells is MIDI, the Clock can control other MIDI instruments, and the Bells can be played with other MIDI controllers.

## Files herein
* **carillon.py** - Where the magic happens.
* **settings-sample.py** - Duplicate/rename this to **settings.py** and edit accordingly.
* **meterCalibrate.py** - Use this to calibrate your 3VDC meter.
* **clockCalibrate.py** - *Coming soon.* Use this to tell the Pi what time your slave clock reads (in case it runs, but is wrong).
* **clockAdvance.py** - *Coming soon.* carillon calls this asynchronously to advance the clock to the current time.
* **alloff.mid** - carillon uses this periodically to kill all MIDI notes, in case `aplaymidi` terminates early and leaves notes on. Don't want solenoids to burn out!
* **midi/** - Some common (and not so common) chime programs (see below).

## Chime programs
To be included in the program, MIDI files in the MIDI path (per settings.py) should be formatted as `[time][-description].mid` where `time` is `[[N]h][[N]m][[N]s]`. If `[N]` is omitted it means "every". Use 24-hour notation. If `description` includes the word "strike" (case sensitive), it will be repeated per the current hour (12-hour clock). If multiple .mid files are triggered at once, only the highest-priority one plays: priority is given to larger units of time, and specific (rather than repeating) times, which allows for easy overriding. Chimes do not interrupt other chimes, but strikes do.

#### Examples
* **s-song.mid** - Plays every second
* **30s-song.mid** - Plays at 30s every minute
* **m-song.mid** - Plays every minute (at 0s)
* **15m-song.mid** - Plays at 15m every hour (at 0s)
* **59m45s-song.mid** - Plays at 59m 45s every hour
* **h-strike.mid** - Plays every hour (at 0m 0s) and repeats per current hour
* **nh-song.mid** - Won't play
* **-song.mid** - Won't play
* **Extension other than .mid** - Won't play
* **why-me.mid** - Will probably crash the script

Validation on these filenames is currently a bit loose. If you have mids that fit the pattern but invalidly, the script may crash. The safest place for .mids you don't want played is in a different folder (such as a subfolder, it'll skip that).

#### Included programs
Most of the included programs follow a pattern of three quarters, plus a fourth quarter that plays a few seconds before the hour, plus the hour strokes, beginning at the very top of the hour, [Big-Ben-style](https://www.youtube.com/watch?v=bmZ2bpJKXUI). All are arranged by me in Logic, with reference to [Clock Chime Tunes Reference](http://www.clockguy.com/SiteRelated/SiteReferencePages/ClockChimeTunes.html) and [*Tolling Time*](http://www.mtosmt.org/issues/mto.00.6.4/mto.00.6.4.harrison.html?q=mto/issues/mto.00.6.4/mto.00.6.4.harrison.html), both of which offer considerably more historical and theoretical detail.
* **Canterbury Cathedral** - 3/4 notes added per quarter, [based on the 8th Gregorian tone](https://books.google.com/books?id=MR9GAQAAMAAJ&pg=PA14&lpg=PA14&dq=canterbury+cathedral+quarter+hour+chime&source=bl&ots=aN0UtyMD39&sig=ot3oeovs5TKWbAQBfKYJk_JcnjI&hl=en&sa=X&ved=0ahUKEwjXlKXX8pTMAhVB7SYKHQ9eB4MQ6AEILDAD#v=onepage&q&f=false) and [quite beautiful](https://www.youtube.com/watch?v=CrLb1XL65Bk). [Further deets](http://www.kenthistoryforum.co.uk/index.php?topic=4805.msg113620#msg113620).
* **Canterbury Herschede** - 6 notes/quarter. Inspired by the Cathedral, allegedly.
* **Guildford** - A rather musical one.
* **Magdalen** - Only 2 notes/quarter.
* **Parsifal** - 4 notes/quarter; inverts on itself. Inspired by Wagner's opera.
* **Saint-Saens That'll Do Pig** - You may recognize this hamfisted arrangement from *Babe* (1995) or "If I Had Words" (1978), but it's originally from [Saint-Saëns' Symphony No. 3](https://www.youtube.com/watch?v=ZWCZq33BrOo). [Further deets](http://www.classicfm.com/composers/saint-saens/guides/organ-symphony-jane-jones/).
* **St. Michael** - 8 notes/quarter. As heard at St. Michael's in Charleston, SC. Reminds me of [change ringing.](https://en.wikipedia.org/wiki/Change_ringing)
* **Trinity** - 6 notes/quarter, but the pitches cover a whole octave. After the Trinity Church in NYC.
* **Westminster** - 4 notes/quarter. The one everyone knows, from Cambridge University via the Palace of Westminster.
* **Whittington** - 8 notes/quarter. There's apparently several versions of this. No matter, they all sound like [change ringing.](https://en.wikipedia.org/wiki/Change_ringing)
* **Winchester** - 6 notes/quarter.

**For later:** program this thing to do actual [change ringing](https://en.wikipedia.org/wiki/Change_ringing)?

## Credit where due!
* [Harpsichord driven by Orgautomatech decoders](https://www.youtube.com/watch?v=UbwfAc0AKhk)
* [Make an Atom Synchronised Clock from a 1950s Slave Clock on Instructables](http://www.instructables.com/id/Make-an-Atom-Synchronised-Clock-from-a-1950s-Slav/)
* [Clock Chime Tunes Reference](http://www.clockguy.com/SiteRelated/SiteReferencePages/ClockChimeTunes.html) and [*Tolling Time*](http://www.mtosmt.org/issues/mto.00.6.4/mto.00.6.4.harrison.html?q=mto/issues/mto.00.6.4/mto.00.6.4.harrison.html)
* Various other credits as sprinkled throughout