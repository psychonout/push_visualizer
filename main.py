import time, rtmidi, sys, soundcard, numpy, librosa.display
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from pprint import pprint
from random import randint, choice

def turnOnAll(color):
	for button in range(0, 127):
		midiout.send_message([144, button, color])
		


def turnOff():
	#turn all buttosn off
	for button in range(0, 127):
		midiout.send_message([128, button, 0])
		midiout.send_message([128, button, 0])

def turnOn(button, color):
	midiout.send_message([144, button, color])		

def twoChannelViz(col, left, right, color):
	rows_left = 0
	rows_right = 0
	slices = [x for x in numpy.arange(0, 1.1, 0.25)]
	try:
		for index, slic in enumerate(slices):
			if slices[index] <= left < slices[index+1]:
				rows_left = index + 1
				break
		for index, slic in enumerate(slices):
			if slices[index] <= right < slices[index+1]:
				rows_right = index + 1 
				break
		col_right = 36 + col
		for row in range(rows_right):
			midiout.send_message([144, col_right + row*8, color])
		col_left = 92 + col
		for row in range(rows_left):
			midiout.send_message([144, col_left - row*8, color])
	except:
		pass


def turnOnCol(col, intensity, color):
	cols = 0
	multiplicator = 3
	slices = [x for x in numpy.arange(0, 1.1 * multiplicator, 0.125)]
	for index, slic in enumerate(slices):
		if slices[index] <= intensity * multiplicator < slices[index+1]:
			cols = index + 1
			break
	col = 36 + col
	if cols >= 9:
		print("{} exceeding one?".format(intensity))
	for row in range(cols):
		midiout.send_message([144, col+row*8, color])

def turnOnColRev(col, intensity, color):
	cols = 0
	slices = [x for x in numpy.arange(0, 1.1, 0.125)]
	for index, slic in enumerate(slices):
		if slices[index] <= intensity < slices[index+1]:
			cols = index + 1
			break
	col = 92 + col
	if cols >= 9:
		print("{} exceeding one?".format(intensity))
	for row in range(cols):
		midiout.send_message([144, col-row*8, color])

def matrix():
	sleep = 0.02
	for button in range(36, 100):
		color = randint(0, 128)
		midiout.send_message([144, button, color])
		time.sleep(sleep)
		midiout.send_message([128, button, 0])
	for col in range(8):
		for button in range(36, 100, 8):
			color = randint(0, 128)
			midiout.send_message([144, button+col, color])
			time.sleep(sleep)
			midiout.send_message([128, button+col, 0])

def freeForAll():
	sleep = 0.05
	button = randint(0, 128)
	color = randint(0, 128)
	midiout.send_message([144, button, color])
	midiout.send_message([176, button, color])
	time.sleep(sleep)
	midiout.send_message([128, button, 0])
	midiout.send_message([176, button, 0])

def blinkDiagonally(sleep):
	diagonals = [[[36], 
			[37, 44], 
			[38, 45, 52], 
			[39, 46, 53, 60], 
			[40, 47, 54, 61, 68], 
			[41, 48, 55, 62, 69, 76], 
			[42, 49, 56, 63, 70, 77, 84], 
			[43, 50, 57, 64, 71, 78, 85, 92],
			[51, 58, 65, 72, 79, 86, 93],
			[59, 66, 73, 80, 87, 94],
			[67, 74, 81, 88, 95],
			[75, 82, 89, 96],
			[83, 90, 97],
			[91, 98],
			[99]],
			[[43], 
			[42, 51], 
			[41, 50, 59], 
			[40, 49, 58, 67], 
			[39, 48, 57, 66, 75], 
			[38, 47, 56, 65, 74, 83], 
			[37, 46, 55, 64, 73, 82, 91], 
			[36, 45, 54, 63, 72, 81, 90, 99],
			[44, 53, 62, 71, 80, 89, 98],
			[52, 61, 70, 79, 88, 97],
			[60, 69, 78, 87, 96],
			[68, 77, 86, 95],
			[76, 85, 94],
			[84, 93],
			[92]]]

	color = randint(0, 128)
	direction = randint(0, 2)
	diagonal = choice(diagonals)
	if direction == 0:
		for line in diagonal:
			for led in line:
				turnOn(led, color)
			time.sleep(sleep)
			turnOff()
		for line in reversed(diagonal):
			for led in line:
				turnOn(led, color)
			time.sleep(sleep)
			turnOff()
	else:
		for line in reversed(diagonal):
			for led in line:
				turnOn(led, color)
			time.sleep(sleep)
			turnOff()
		for line in diagonal:
			for led in line:
				turnOn(led, color)
			time.sleep(sleep)
			turnOff()

def spiralOut(sleep):
	led = 36
	color = randint(0, 128)
	# for x in range(7, 0, -1):
	for i in range(7):
		turnOn(led, color)
		led += 1
		time.sleep(sleep)
		turnOff()
	for i in range(7):
		turnOn(led, color)
		led += 8
		time.sleep(sleep)
		turnOff()
	for i in range(7):
		turnOn(led, color)
		led -= 1
		time.sleep(sleep)
		turnOff()
	for i in range(6):
		turnOn(led, color)
		led -= 8
		time.sleep(sleep)
		turnOff()
	for i in range(6):
		turnOn(led, color)
		led += 1
		time.sleep(sleep)
		turnOff()
	for i in range(5):
		turnOn(led, color)
		led += 8
		time.sleep(sleep)
		turnOff()
	for i in range(5):
		turnOn(led, color)
		led -= 1
		time.sleep(sleep)
		turnOff()
	for i in range(4):
		turnOn(led, color)
		led -= 8
		time.sleep(sleep)
		turnOff()
	for i in range(4):
		turnOn(led, color)
		led += 1
		time.sleep(sleep)
		turnOff()
	for i in range(3):
		turnOn(led, color)
		led += 8
		time.sleep(sleep)
		turnOff()
	for i in range(3):
		turnOn(led, color)
		led -= 1
		time.sleep(sleep)
		turnOff()
	for i in range(2):
		turnOn(led, color)
		led -= 8
		time.sleep(sleep)
		turnOff()
	turnOn(led, color)
	time.sleep(sleep)
	turnOff()
	for i in range(3):
		turnOn(71, color)
		turnOn(72, color)
		turnOn(63, color)
		turnOn(64, color)
		time.sleep(sleep)
		turnOff()
		time.sleep(sleep)

def spiralOutFull(sleep):
	turnOff()
	led = 36
	color = randint(0, 128)
	# for x in range(7, 0, -1):
	for i in range(7):
		turnOn(led, color)
		led += 1
		time.sleep(sleep)	
	for i in range(7):
		turnOn(led, color)
		led += 8
		time.sleep(sleep)
	for i in range(7):
		turnOn(led, color)
		led -= 1
		time.sleep(sleep)
	for i in range(6):
		turnOn(led, color)
		led -= 8
		time.sleep(sleep)
	for i in range(6):
		turnOn(led, color)
		led += 1
		time.sleep(sleep)
	for i in range(5):
		turnOn(led, color)
		led += 8
		time.sleep(sleep)
	for i in range(5):
		turnOn(led, color)
		led -= 1
		time.sleep(sleep)
	for i in range(4):
		turnOn(led, color)
		led -= 8
		time.sleep(sleep)
	for i in range(4):
		turnOn(led, color)
		led += 1
		time.sleep(sleep)
	for i in range(3):
		turnOn(led, color)
		led += 8
		time.sleep(sleep)
	for i in range(3):
		turnOn(led, color)
		led -= 1
		time.sleep(sleep)
	for i in range(2):
		turnOn(led, color)
		led -= 8
		time.sleep(sleep)
	turnOn(led, color)
	time.sleep(sleep)
	for i in range(3):
		turnOn(71, color)
		turnOn(72, color)
		turnOn(63, color)
		turnOn(64, color)
		time.sleep(sleep*10)
		turnOff()
		time.sleep(sleep*10)

def show():
	while True:
		blinkDiagonally(sleep)
		spiralOut(sleep)
		spiralOutFull(sleep)
		blinkDiagonally(sleep)

"""
92 93 94 95 96 97 98 99
84 85 86 87 88 89 90 91
76 77 78 79 80 81 82 83
68 69 70 71 72 73 74 75
60 61 62 63 64 65 66 67
52 53 54 55 56 57 58 59
44 45 46 47 48 49 50 51
36 37 38 39 40 41 42 43
"""

speaker = soundcard.get_speaker("Steinberg")
microphone = soundcard.get_microphone("Steinberg", include_loopback=True)
   
midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()
for port in available_ports:
	if "Ableton Push 2" in port and "MIDIOUT" not in port:
		device = int(port[-1])
midiout.open_port(device)
sleep = 0.02
turnOff()
prev = 0
color = randint(0, 127)
print("{} is the color.".format(color))
samples = 11200
milisec = 56
eighth = int(milisec / 8)
with microphone.recorder(samplerate=samples, channels=2) as mic:
	while True:
		#freeForAll()
		turnOff()
		audio = mic.record(numframes=milisec)
		curr = numpy.average(audio)
		# if prev < curr:
		# 	turnOff()
		prev = curr
		count = 0
		# for slic in range(0, len(audio), eighth):
		# 	twoChannelViz(count, numpy.average(audio[slic:slic+eighth][0]), numpy.average(audio[slic:slic+eighth][1]), color)
		# 	count += 1

		# for slic in range(0, len(audio), eighth):
		# 	turnOnColRev(count, numpy.average(audio[slic:slic+14]), color)
		# 	count += 1

		for slic in range(0, len(audio), eighth):
			turnOnCol(count, numpy.average(audio[slic:slic+14]), color)
			count += 1
		# speaker.play(audio/numpy.max(audio), samplerate=samples)
		# plt.plot(audio)
		# plt.show()
		# avg = numpy.average(audio)
		# for key in reds:
		# 	if avg > key:
		# 		color = reds[key]
		# 		for button in range(36, 100):
		# 			midiout.send_message([144, button, color])
		# 		turnOff()

turnOff()