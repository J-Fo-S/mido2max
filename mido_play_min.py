# adapted from: https://github.com/mido/mido/blob/main/examples/midifiles/play_midi_file.py
# see: https://mido.readthedocs.io/en/stable/
"""
Play MIDI file on output port.

"""
import time
import mido
import argparse
from mido import MidiFile

def time_rate(rate):
        return time.time()*rate
    
# quick generator to access and modify midi
# tempo is irrelevant if playing back via clock
# dur_scale increases/decreases tempo. clock_scale is just for fun - can 'realign' note timings
def play_mod(midifile, now=time.time, clock_scale=1., dur_scale=1.):  
    start_time = now(clock_scale)
    input_time = 0.0
    for msg in midifile:
        if not msg.is_meta:
            input_time += msg.time*dur_scale
            playback_time = now(clock_scale) - start_time
            duration_to_next_event = input_time - playback_time
            if duration_to_next_event > 0.0:
                time.sleep(duration_to_next_event)
            yield msg

# Run
parser = argparse.ArgumentParser()
parser.add_argument('--filename', type=str, default='onenotesamba3.mid')
parser.add_argument('--clock_scale', type=float, default=1.0, help='scale the system clock - 1.0 is default')
parser.add_argument('--dur_scale', type=float, default=1.0, help='scale the midi note durations - 1.0 is default')
args = parser.parse_args()
filename = args.filename
midifile = MidiFile(filename)
with mido.open_output(mido.get_output_names()[0]) as output:
    try:
        t0 = time.time()
        for msg in play_mod(midifile, now=time_rate, clock_scale=args.clock_scale, dur_scale=args.dur_scale):
            output.send(msg)
        print('play time: {:.2f} s (expected {:.2f})'.format(
            time.time() - t0, midifile.length))
        quit()

    except KeyboardInterrupt:
        print()
        output.reset()