# carillon
Use your Raspberry Pi to play MIDI files on schedule. Companion to [master-clock](https://github.com/clockspot/master-clock).

## Why?
I got a harebrained scheme to build an indoor carillon in two loosely-coupled parts:

* **the Clock,** a Raspberry Pi living inside and controlling a 1960s Gents slave clock (see companion project [master-clock](https://github.com/clockspot/master-clock)), synced to NTP (via `ntpd`), and outputting MIDI (via `amidi` and `aplaymidi`) on schedule; and
* **the Bells**, a small glockenspiel rigged with solenoids wired up to [a purpose-made MIDI decoder card from Orgautomatech](http://www.orgautomatech.com/), receiving MIDI from the Clock.

Because the only link between the Clock and Bells is MIDI, the Clock can control other MIDI instruments, and the Bells can be played with other MIDI controllers.

## How to use
* **Install packages** if not present: `python`, `python-daemon`
* **Make settings file** `settings.py` as a copy of `settings-sample.py`, and modify to suit. Other instructions within (e.g. file permissions).
* **Run the script,** e.g. `./carillon.py`, directly or at startup. It will detach from the shell and run as a daemon. No start/stop service controls just yet; for now, stop with `stop.sh` or e.g. `pkill -f carillon.py`.

## Files herein
* `carillon.py` - Where the magic happens.
* `settings-sample.py` - Duplicate to `settings.py` and edit accordingly.
* `midi/` - Some common (and not so common) chime programs (see below).
* `midiplay.py` - Play MIDI files directly for testing; pass file path as argument.
* `stop.sh` - Lazy way of stopping the daemon.

## Chime programs
To be included in the program, MIDI files in the MIDI path (per settings.py) should be formatted as `[time][-description].mid` where `time` is `[[N]d][[N]h][[N]m][[N]s]`. If `[N]` is omitted it means "every". Use 24-hour notation. If `description` includes the word "strike" (case sensitive), it will be repeated per the current hour (12-hour clock). If multiple .mid files are triggered at once, only the highest-priority one plays: priority is given to larger units of time, and specific (rather than repeating) times, which allows for easy overriding. Chimes do not interrupt other chimes, but strikes do.

#### Examples
* **s-song.mid** - Plays every second
* **30s-song.mid** - Plays at 30s every minute
* **m-song.mid** - Plays every minute (at 0s)
* **15m-song.mid** - Plays at 15m every hour (at 0s)
* **59m45s-song.mid** - Plays at 59m 45s every hour
* **2d11h59m45s-song.mid** - Plays 15s before noon every Tuesday
* **h-strike.mid** - Plays every hour (at 0m 0s) and repeats per current hour
* **nh-song.mid** - Won't play
* **-song.mid** - Won't play
* **Extension other than .mid** - Won't play
* **why-me.mid** - Will probably crash the script

Validation on these filenames is currently a bit loose. If you have mids that fit the pattern but invalidly, the script may crash. The safest place for .mids you don't want played is in a different folder (such as a subfolder, it'll skip that).

#### Included chime programs
Most of these follow a pattern of three quarters, plus a fourth quarter that plays a few seconds before the hour, plus the hour strokes, beginning at the very top of the hour, [Big-Ben-style](https://www.youtube.com/watch?v=tHMVdhEp-Tw). All are arranged by me, with reference to [Clock Chime Tunes Reference](http://www.clockguy.com/SiteRelated/SiteReferencePages/ClockChimeTunes.html) and [*Tolling Time*](http://www.mtosmt.org/issues/mto.00.6.4/mto.00.6.4.harrison.html?q=mto/issues/mto.00.6.4/mto.00.6.4.harrison.html), both of which offer considerably more historical and theoretical detail.
* **Canterbury Cathedral** - 3–4 notes/quarter, [based on the 8th Gregorian tone](https://books.google.com/books?id=MR9GAQAAMAAJ&pg=PA14&lpg=PA14&dq=canterbury+cathedral+quarter+hour+chime&source=bl&ots=aN0UtyMD39&sig=ot3oeovs5TKWbAQBfKYJk_JcnjI&hl=en&sa=X&ved=0ahUKEwjXlKXX8pTMAhVB7SYKHQ9eB4MQ6AEILDAD#v=onepage&q&f=false). [Example](https://www.youtube.com/watch?v=CrLb1XL65Bk) and [further deets](http://www.kenthistoryforum.co.uk/index.php?topic=4805.msg113620#msg113620).
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

## Best-laid plans
* Take advantage of crontab? Depends if it triggers precisely enough, can handle overlaps, etc
* Program to do actual [change ringing](https://en.wikipedia.org/wiki/Change_ringing)?
* Admin via web console?

## Credit where due!
* [Harpsichord driven by Orgautomatech decoders](https://www.youtube.com/watch?v=UbwfAc0AKhk)
* [Clock Chime Tunes Reference](http://www.clockguy.com/SiteRelated/SiteReferencePages/ClockChimeTunes.html) and [*Tolling Time*](http://www.mtosmt.org/issues/mto.00.6.4/mto.00.6.4.harrison.html?q=mto/issues/mto.00.6.4/mto.00.6.4.harrison.html)
* Various other credits within