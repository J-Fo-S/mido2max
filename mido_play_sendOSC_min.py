# adapted from: https://github.com/mido/mido/blob/main/examples/midifiles/play_midi_file.py
# see: https://mido.readthedocs.io/en/stable/

"""
Send midi over osc

"""
import time
import mido
import argparse
from mido import MidiFile
from pythonosc import udp_client

class OSCSender:

    def __init__(self,ip="127.0.0.1",port=11004):
        self.sender = udp_client.SimpleUDPClient(ip,port)

    def sendMessage(self,address,args):
        self.sender.send_message(address,args)
    
    def sendDict(self,dict):
        for k,v in dict.items():
            self.sendMessage(k,v)

    def time_rate(self, rate):
            return time.time()*rate
        
    # quick generator to access and modify midi
    # tempo is irrelevant if playing back via clock
    # # dur_scale increases/decreases tempo. clock_scale is just for fun - can 'realign' note timings
    def play_mod(self, midifile, now=time.time, clock_scale=1., dur_scale=1.):  
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
osc_send = OSCSender()
try:
    t0 = time.time()
    for msg in osc_send.play_mod(midifile, now=osc_send.time_rate, clock_scale=args.clock_scale, dur_scale=args.dur_scale):
        #osc_send.sendDict(msg.dict())
        if msg.type == 'note_on' or  msg.type == 'note_off':
            osc_send.sendMessage('note', msg.note)
            osc_send.sendMessage('velocity', msg.velocity)
            osc_send.sendMessage('time', msg.time)
        
    print('play time: {:.2f} s (expected {:.2f})'.format(
        time.time() - t0, midifile.length))
    quit()
except KeyboardInterrupt:
    quit()