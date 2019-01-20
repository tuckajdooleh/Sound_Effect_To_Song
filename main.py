from pydub import AudioSegment
from pydub.playback import play
import librosa
#import midi
from mido import MidiFile
import mido
#import time
import os.path
from pathlib import Path
import wave
import numpy as np

#load in C version of the sound 1600
y, sr = librosa.load('src/sound_effect/sound_in_c4.wav', sr=16000) # y is a numpy array of the wav file, sr = sample rate
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

#mid = MidiFile('src/SkinnyLove.mid')

#song = AudioSegment.from_wav('src/gabe-bark.wav')
song = AudioSegment.silent(duration=(1000))



previous_audio = song
#if its 0 then take current not and merge the 2 notes, if its not zero, then add previous note to song
#then add silence
#for msg in MidiFile('src/SkinnyLove.mid').play():
resttime = 0
combineNotes = []
mid = MidiFile('src/midi/song.mid')
print (mid.type)
numberoftracks = 0
for i, track in enumerate(mid.tracks):
	print('Track {}: {}'.format(i, track.name))
#for msg in MidiFile('src/midi/song.mid'):
	for msg in track:
		if not msg.is_meta:
			print(msg)
			if msg.type == 'note_on' :
				if msg.velocity == 0:
					resttime += msg.time	
				elif msg.time == 0:
					#use msg.note, derive note name from 60 = c, then select actual note, and overlay with previous sound

					filename = "src/chromatic/" + str(msg.note) + ".wav"
					new_note = AudioSegment.from_wav(filename)
					#combineNotes.append(new_note)
					#getridofnextline
					previous_audio = previous_audio.overlay(new_note)
				else:
					#rest_time = AudioSegment.silent(duration=(msg.time *100) +resttime*100)
					rest_time = AudioSegment.silent(duration=(mido.tick2second(msg.time , mid.ticks_per_beat, 500000)*100 + mido.tick2second(resttime, mid.ticks_per_beat, 500000)*100))
					#mido.tick2second(ticks, mid.ticks_per_beat, 500000)
					#500000 microsecs = 120 bpm
					#if time is given in seconds
					#how
					
		#			if len(combineNotes) > 0 :
		#				combined = combineNotes[0]
		#			if len(combineNotes) > 1 :
		#				for i in range(len(combineNotes)-1):
						
		#					combined = combined.overlay(combineNotes[i+1])
					
					
			#		def set_to_target_level(sound, target_level):
			#		difference = target_level - sound.dBFS
			#		return sound.apply_gain(difference)

			#	sound1_adjusted = set_to_target_level(sound1, -12.0)
			#	sound2_adjusted = set_to_target_level(sound2, -12.0)

			#	combined = sound1_adjusted.overlay(sound2_adjusted)
					
					
		#			if len(combineNotes) > 0 :
					song += previous_audio
					#how
					song += rest_time
				
					filename = "src/chromatic/" + str(msg.note) + ".wav"
					new_note = AudioSegment.from_wav(filename)
					previous_audio = new_note
					resttime = 0
					combineNotes=[]
					combined = 0
		#need to treat velocity 0 as nothing, but still add up its time...
	song.export('src/final/part' + str(i) +'.wav', format="wav")
	numberoftracks = i
	
if numberoftracks == 1:
	filename = 'src/final/part0.wav'
	part1 = AudioSegment.from_wav(filename)
	filename = 'src/final/part1.wav'
	part2 = AudioSegment.from_wav(filename)
	song = part1.overlay(part2)

song.export('src/final/final.wav', format="wav")
play(song)

'''
t1 = 120+20
t2 = 60+47
t1 = t1 * 1000 #Works in milliseconds
t2 = t2 * 1000
filename = 'src/final/part0.wav'
part1 = AudioSegment.from_wav(filename)
filename = 'src/final/part1.wav'
part2 = AudioSegment.from_wav(filename)
newpart2= part2[:t2]


song = part1.overlay(newpart2)

song.export('src/final/final.wav', format="wav")
'''