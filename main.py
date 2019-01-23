from pydub import AudioSegment
from pydub.playback import play
import librosa
from mido import MidiFile
import mido
import time
import os.path
from pathlib import Path
import wave
import numpy as np
import math

x = input('create chromatic scale?')

if x == 'yes':

	#load in C version of the sound 1600
	y, sr = librosa.load('src/sound_effect/sound_in_c4.wav', sr=32000) # y is a numpy array of the wav file, sr = sample rate
	#place that version in Chromatic as C
	#then do the entire chromatic scale
	librosa.output.write_wav('src/chromatic/60.wav',y,sr,norm=False);
	print ('c4-60');

	for i in range(40):
		name = 'src/chromatic/' + str(61+i)+ '.wav'
		namefile = Path('home/tucker/Desktop/Sound_Effect_To_Song/src/chromatic/60.wav')
		if ~(namefile.is_file() ):
			y_shifted = librosa.effects.pitch_shift(y, sr, n_steps=1+i) # shifted by 1 half step
			librosa.output.write_wav(name,y_shifted,sr,norm=False);
			print (str(61+i));

	#shifting down

	for i in range(34):
		name = 'src/chromatic/' + str(59-i)+ '.wav'
		namefile = Path("src/chromatic/" + str(59-i)+ ".wav")
		if ~(namefile.is_file() ):
			y_shifted = librosa.effects.pitch_shift(y, sr, n_steps=-1-i) # shifted by 1 half step
			librosa.output.write_wav(name,y_shifted,sr,norm=False);
			print (str(59-i));

	#actual midi parsing and song composition

mid = MidiFile('src/midi/song.mid')
print (mid.type)
numberoftracks = 0
song_canvas = AudioSegment.silent(4*60*1000)

current_time = 0
for i, track in enumerate(mid.tracks):
	current_time = 0
	test_list = []
	current_part = AudioSegment.silent(4*60*1000)
	('Track {}: {}'.format(i, track.name))
	for msg in track:
		print(msg)
		if not msg.is_meta:
			
			if msg.type == 'note_on' :
				if msg.velocity == 0:
					current_time += mido.tick2second(msg.time , mid.ticks_per_beat, 500000)*1000	
				elif msg.time == 0:
				
					#filename = "src/chromatic/" + str(msg.note) + ".wav"
					#new_note = AudioSegment.from_wav(filename)
					
					test_list.append({'note':str(msg.note), 'time':current_time})
					#current_part = current_part.overlay(new_note, position=current_time)
				else:
					
					#500000 microsecs = 120 bpm
					
					current_time += mido.tick2second(msg.time , mid.ticks_per_beat, 500000)*1000
					#filename = "src/chromatic/" + str(msg.note) + ".wav"
					#new_note = AudioSegment.from_wav(filename)
					test_list.append({'note':msg.note, 'time':current_time})
					#current_part = current_part.overlay(new_note, position=current_time)
	
	
	

	all_notes = [None]*100

	for y in range(80):
			
			note = y +20
			print(' inserting '+str(note)+' to the array')
			filename = "src/chromatic/" + str(note) + ".wav"
			new_note = AudioSegment.from_wav(filename)
			all_notes.insert(note, new_note)
			
			
	for x in test_list:
			print(' grabbing '+str(x.get('note'))+' from the array')
			placeholder = all_notes[int(x.get('note'))]
			print(' grabbed  from the array')
			print(' placing note at t =  '+str(x.get('time')))
			
			
			current_part = current_part.overlay(all_notes[int(x.get('note'))], position=x.get('time'))
			print(' placed note')
			
	current_part.export('src/final/part'+ str(i)+'.wav', format="wav")

		

song_canvas = AudioSegment.silent(4*60*1000)
filename = "src/final/part0.wav"
new_note = AudioSegment.from_wav(filename)

song_canvas = song_canvas.overlay(new_note)
filename = "src/final/part1.wav"
new_note = AudioSegment.from_wav(filename)
new_note = new_note - 3
song_canvas = song_canvas.overlay(new_note)
song_canvas.export('src/final/overlayed.wav', format="wav")
#song_canvas.export('src/final/part' + str(i) +'.wav', format="wav")
#numberoftracks = i