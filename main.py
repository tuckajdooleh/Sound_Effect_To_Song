from pydub import AudioSegment
from pydub.playback import play
import librosa
import midi
from mido import MidiFile
import mido
import time

mid = MidiFile('src/SkinnyLove.mid')

song = AudioSegment.from_wav('src/gabe-bark.wav')

song.export('src/final.wav', format="wav")
play(song)


previous_audio = song
#if its 0 then take current not and merge the 2 notes, if its not zero, then add previous note to song
#then add silence
#for msg in MidiFile('src/SkinnyLove.mid').play():
for msg in MidiFile('src/SkinnyLove.mid'):
	print(msg)
	if msg.type == 'note_on' :
		if msg.time == 0:
			#use msg.note, derive note name from 60 = c, then select actual note, and overlay with previous sound
			filename = "src/chromatic/" + str(msg.note%12) + ".wav"
			new_note = AudioSegment.from_wav(filename)
			previous_audio = previous_audio.overlay(new_note)
		else:
			rest_time = AudioSegment.silent(duration=msg.time * 1000)
			#if time is given in seconds
			song += previous_audio
			song += rest_time
		
			filename = "src/chromatic/" + str(msg.note % 12) + ".wav"
			new_note = AudioSegment.from_wav(filename)
			previous_audio = new_note
		
	#need to treat velocity 0 as nothing, but still add up its time...
song.export('src/final.wav', format="wav")
play(song)
	# create 1 sec of silence audio segment
  #duration in milliseconds
'''
#load in C version of the sound
y, sr = librosa.load('src/gabe-bark.wav', sr=16000) # y is a numpy array of the wav file, sr = sample rate
#place that version in Chromatic as C
#then do the entire chromatic scale
librosa.output.write_wav('src/chromatic/c.wav',y,sr,norm=False);
print ('c');
y_shifted = librosa.effects.pitch_shift(y, sr, n_steps=1) # shifted by 1 half step
librosa.output.write_wav('src/chromatic/c#.wav',y_shifted,sr,norm=False);
print ('c#');
y_shifted = librosa.effects.pitch_shift(y, sr, n_steps=2) # shifted by 1 half step
librosa.output.write_wav('src/chromatic/d.wav',y_shifted,sr,norm=False);
print ('d');
y_shifted = librosa.effects.pitch_shift(y, sr, n_steps=3) # shifted by 1 half step
librosa.output.write_wav('src/chromatic/d#.wav',y_shifted,sr,norm=False);
print ('d#');
y_shifted = librosa.effects.pitch_shift(y, sr, n_steps=4) # shifted by 1 half step
librosa.output.write_wav('src/chromatic/e.wav',y_shifted,sr,norm=False);
print ('e');
y_shifted = librosa.effects.pitch_shift(y, sr, n_steps=5) # shifted by 1 half step
librosa.output.write_wav('src/chromatic/f.wav',y_shifted,sr,norm=False);
print ('f');
y_shifted = librosa.effects.pitch_shift(y, sr, n_steps=6) # shifted by 1 half step
librosa.output.write_wav('src/chromatic/f#.wav',y_shifted,sr,norm=False);
print ('f#');
y_shifted = librosa.effects.pitch_shift(y, sr, n_steps=7) # shifted by 1 half step
librosa.output.write_wav('src/chromatic/g.wav',y_shifted,sr,norm=False);
print ('g');
y_shifted = librosa.effects.pitch_shift(y, sr, n_steps=8) # shifted by 1 half step
librosa.output.write_wav('src/chromatic/g#.wav',y_shifted,sr,norm=False);
print ('g#');
y_shifted = librosa.effects.pitch_shift(y, sr, n_steps=9) # shifted by 1 half step
librosa.output.write_wav('src/chromatic/a.wav',y_shifted,sr,norm=False);
print ('a');
y_shifted = librosa.effects.pitch_shift(y, sr, n_steps=10) # shifted by 1 half step
librosa.output.write_wav('src/chromatic/a#.wav',y_shifted,sr,norm=False);
print ('a#');
y_shifted = librosa.effects.pitch_shift(y, sr, n_steps=11) # shifted by 1 half step
librosa.output.write_wav('src/chromatic/b.wav',y_shifted,sr,norm=False);
print ('b');
'''
#pattern = midi.read_midifile("src/SkinnyLove.mid")
#print(pattern);

'''
sound = AudioSegment.from_file('src/gabe-bark.wav', format="wav")

# shift the pitch up by half an octave (speed will increase proportionally)
octaves = 0.5

new_sample_rate = int(sound.frame_rate * (2.0 ** octaves))

# keep the same samples but tell the computer they ought to be played at the 
# new, higher sample rate. This file sounds like a chipmunk but has a weird sample rate.
hipitch_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})

# now we just convert it to a common sample rate (44.1k - standard audio CD) to 
# make sure it works in regular audio players. Other than potentially losing audio quality (if
# you set it too low - 44.1k is plenty) this should now noticeable change how the audio sounds.
hipitch_sound = hipitch_sound.set_frame_rate(44100)

#Play pitch changed sound
play(hipitch_sound)

#export / save pitch changed sound
#hipitch_sound.export("src/newlul.wav", format="wav")
'''








'''

#stitch together
sound1 = AudioSegment.from_wav("/path/to/file1.wav")
sound2 = AudioSegment.from_wav("/path/to/file2.wav")

combined_sounds = sound1 + sound2
combined_sounds.export("/output/path.wav", format="wav")


#overlay
sound1 = AudioSegment.from_file("/path/to/my_sound.wav")
sound2 = AudioSegment.from_file("/path/to/another_sound.wav")

combined = sound1.overlay(sound2)

combined.export("/path/to/combined.wav", format='wav')

#fit sound effect to be length of 1 beat, also have a sound effect of nothing
#then just use these 2 things with the midi
#also need to pitch bend note to make all the notes we need


'''
