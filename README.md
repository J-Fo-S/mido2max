### Mido2Max

This is a quick code experiment to iteratively send midi to Max in real-time via [Mido](https://github.com/mido/mido). The midi is sent by OSC, which might seem odd but it's easy and it works. Alternatively you can simply play the midi in Python by itself, but this code has only been tested on Windows 10. The original idea was to generate midi through [music21](https://web.mit.edu/music21/) or some other library and send to Max, all in real-time. At the moment, the generative code has not been developed, and this code simply iterates through a static midi file.

#### Requirements

`pip install -r requirements.txt`

#### About / How-to-Use

`python mido_play_sendOSC_min.py` runs the Mido2Max code and `python mido_play_min.py` runs the python-only code. Both programs use computer clock, and you can read here about [timing](https://mido.readthedocs.io/en/stable/files/midi.html). In this code, there are two time parameters that you can modify to affect the timing of the midi playback. One is the duration of each individual note, and the other is the system clock. You have access to these as arguments. `python mido_play_sendOSC_min.py --clock_scale 1.0 --dur_scale 1.0` is the default setting, which will play back the midi file faithfully according to each individual midi note time value (as opposed to a global tempo). If you would like to change the "tempo", then you can change the `dur_scale` value. For example `--dur_scale 0.5` will double the tempo. `clock_scale` will affect the timing of the individual midi notes by scaling the computer clock. It's really just there for fun: `python mido_play_sendOSC_min.py --clock_scale 0.1 --dur_scale 0.1` kinda sounds like Thelonius Monk if he were reduced to a lowly python program. Finally, to run your own file, use the argument `--filename [your_midi_file].mid`. The default is One Note Samba. 



