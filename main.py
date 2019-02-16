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


def createChromaticScale():
	#y_slow = librosa.effects.time_stretch(y, 0.5)
	#librosa.output.write_wav('src/chromatic/60_slow.wav',y_slow,sr,norm=False);

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


def loadNotes(all_notes):
	for y in range(80):
		
		note = y +20
		print(' inserting '+str(note)+' to the array')
		filename = "src/chromatic/" + str(note) + ".wav"
		new_note = AudioSegment.from_wav(filename)
		all_notes.insert(note, new_note)
			





def main():

	createChromaticScale()

		#actual midi parsing and song composition


	all_notes = [None]*100

	loadNotes(all_notes)


	mid = MidiFile('src/midi/song.mid')
	print (mid.type)

	song_canvas = AudioSegment.silent(8*60*1000)

	current_time = 0
	for i, track in enumerate(mid.tracks):
		current_time = 0
		test_list = []
		('Track {}: {}'.format(i, track.name))
		index = 0
		for msg in track:
			print(msg)
			if msg.is_meta:
				current_time += round(mido.tick2second(msg.time , mid.ticks_per_beat, mido.bpm2tempo(210))*1000,3)
			
			elif msg.type == 'note_on' :
				if msg.velocity == 0:
					current_time += round(mido.tick2second(msg.time , mid.ticks_per_beat, mido.bpm2tempo(210))*1000	,3)
					
					#test_list[index - 1]["length"] = 
				elif msg.time == 0:
			
					test_list.append({'note':str(msg.note), 'time':current_time, 'length':1})
					
				else:
					
					#500000 microsecs = 120 bpm
					
					current_time += round(mido.tick2second(msg.time , mid.ticks_per_beat, mido.bpm2tempo(210))*1000,3)
			
					test_list.append({'note':msg.note, 'time':current_time, 'length':1})
			index = index +1
					
			if len(test_list) >= 50:
				for x in test_list:
				#print(' grabbing '+str(x.get('note'))+' from the array')
				
				#print(' grabbed  from the array')
					print(' placing note at t =  '+str(x.get('time')))
					
					
					song_canvas = song_canvas.overlay(all_notes[int(x.get('note'))], position=x.get('time'))
					#print(' placed note')
				test_list = []
				
	
	

	
			
		for x in test_list:
				#print(' grabbing '+str(x.get('note'))+' from the array')
				
				#print(' grabbed  from the array')
				print(' placing note at t =  '+str(x.get('time')))
				
				
				song_canvas = song_canvas.overlay(all_notes[int(x.get('note'))], position=x.get('time'))
				#print(' placed note')
				
		
	song_canvas.export('src/final/final_version.wav', format="wav")
			
			

main()
