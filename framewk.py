import soundfloat as sound
import scipy.io.wavfile as wav
import pyaudio
import numpy as np
import pickle
#import matplotlib.pyplot as plt


def encframewk(fileName,channels,outName):
	""" Function that reads a track in fileName with 16 bit per sample and stores it in a binary file with 16 bit per sample"""
	
	RATE, wavData = wav.read(fileName)	
	t1 = 2
	t2 = 5
	
	
	p = pyaudio.PyAudio()
	
	# open audio stream

	stream = p.open(format=pyaudio.paInt16, # paFloat32, # paInt16,
					channels=channels,
					rate=RATE,
					output=True)

	nShiftSamples = t1 * RATE
	nSamples = t2*RATE # seconds*Hz
	fragment = wavData[nShiftSamples:nShiftSamples+nSamples,:]
	
	#save data as binary file	
	pickle.dump(fragment, open(outName, "wb"), 1)
	#play fragment	
	sound = (fragment.astype(np.int16).tostring())
	stream.write(sound)

    # close stream and terminate audio object
	stream.stop_stream()
	stream.close()
	p.terminate()
	return

def decframewk(inFile,outFile,RATE):
	""" Function thats read a .bin file and saves it back as a .wav file"""

	pkl_file = open(inFile, 'rb')
	data = pickle.load(pkl_file)
	wav.write(outFile,RATE,data)


# test area

wavName = 'Track48.wav'
RATE = 48000 # Hz
CH= 2
binName = 'encoded.bin'
outName = 'decoded.wav'

encframewk(wavName,CH,binName)
decframewk(binName,outName,RATE)








