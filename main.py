import sys
import time
import warnings
from pprint import pprint
from random import choice, randint

import librosa.display
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy
import rtmidi
import soundcard
from rtmidi.midiconstants import NOTE_OFF, NOTE_ON

warnings.filterwarnings("ignore")


def turn_on_all(color):
    for button in range(0, 127):
        midiout.send_message([144, button, color])


def turn_off(device):
    # turn all buttosn off
    for button in range(0, 127):
        device.send_message([128, button, 0])
        device.send_message([176, button, 0])


def turn_on(device, button, color):
    device.send_message([NOTE_ON, button, color])


def two_channel_viz(col, left, right, color):
    rows_left = 0
    rows_right = 0
    slices = [x for x in numpy.arange(0, 1.1, 0.25)]
    try:
        for index, slic in enumerate(slices):
            if slices[index] <= left < slices[index + 1]:
                rows_left = index + 1
                break
        for index, slic in enumerate(slices):
            if slices[index] <= right < slices[index + 1]:
                rows_right = index + 1
                break
        col_right = 36 + col
        for row in range(rows_right):
            midiout.send_message([144, col_right + row * 8, color])
        col_left = 92 + col
        for row in range(rows_left):
            midiout.send_message([144, col_left - row * 8, color])
    except:
        pass


def turn_on_col(col, intensity, color):
    cols = 0
    multiplicator = 3
    slices = [x for x in numpy.arange(0, 1.1 * multiplicator, 0.125)]
    for index, slic in enumerate(slices):
        if slices[index] <= intensity * multiplicator < slices[index + 1]:
            cols = index + 1
            break
    col = 36 + col
    if cols >= 9:
        print("{} exceeding one?".format(intensity))
    for row in range(cols):
        midiout.send_message([144, col + row * 8, color])


def turn_on_col_reverse(col, intensity, color):
    cols = 0
    slices = [x for x in numpy.arange(0, 1.1, 0.125)]
    for index, slic in enumerate(slices):
        if slices[index] <= intensity < slices[index + 1]:
            cols = index + 1
            break
    col = 92 + col
    if cols >= 9:
        print("{} exceeding one?".format(intensity))
    for row in range(cols):
        midiout.send_message([144, col - row * 8, color])


def matrix(device, sleep=0.02):
    for button in range(36, 100):
        color = randint(0, 128)
        device.send_message([144, button, color])
        time.sleep(sleep)
        device.send_message([128, button, 0])
    for col in range(8):
        for button in range(36, 100, 8):
            color = randint(0, 128)
            device.send_message([144, button + col, color])
            time.sleep(sleep)
            device.send_message([128, button + col, 0])


def randy():
    return randint(0, 128)


def free_for_all(device, sleep=0.05):
    note = randy()
    device.send_message([NOTE_ON, note, randy()])
    # device.send_message([176, randy(), randy()])
    time.sleep(sleep)
    device.send_message([NOTE_OFF, note, 0])
    # device.send_message([176, randy(), 0])


def scale(device, sleep=0.05):
    notes = [36, 38, 40, 41, 43, 45, 47, 48, 50, 52, 53, 55, 57, 59, 60]
    for note in notes:
        device.send_message([144, note, 127])
        time.sleep(sleep)
        device.send_message([128, note, 0])
    for note in reversed(notes):
        device.send_message([144, note, 127])
        time.sleep(sleep)
        device.send_message([128, note, 0])


def blink_diagonally(device, sleep):
    diagonals = [
        [
            [36],
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
            [99],
        ],
        [
            [43],
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
            [92],
        ],
    ]

    color = randint(0, 128)
    direction = randint(0, 2)
    diagonal = choice(diagonals)
    if direction == 0:
        for line in diagonal:
            for led in line:
                turn_on(device, led, color)
            time.sleep(sleep)
            turn_off(device)
        for line in reversed(diagonal):
            for led in line:
                turn_on(device, led, color)
            time.sleep(sleep)
            turn_off(device)
    else:
        for line in reversed(diagonal):
            for led in line:
                turn_on(device, led, color)
            time.sleep(sleep)
            turn_off(device)
        for line in diagonal:
            for led in line:
                turn_on(device, led, color)
            time.sleep(sleep)
            turn_off(device)


def spiral_out(device, sleep):
    led = 36
    color = randint(0, 128)
    # for x in range(7, 0, -1):
    for i in range(7):
        turn_on(device, led, color)
        led += 1
        time.sleep(sleep)
        turn_off(device)
    for i in range(7):
        turn_on(device, led, color)
        led += 8
        time.sleep(sleep)
        turn_off(device)
    for i in range(7):
        turn_on(device, led, color)
        led -= 1
        time.sleep(sleep)
        turn_off(device)
    for i in range(6):
        turn_on(device, led, color)
        led -= 8
        time.sleep(sleep)
        turn_off(device)
    for i in range(6):
        turn_on(device, led, color)
        led += 1
        time.sleep(sleep)
        turn_off(device)
    for i in range(5):
        turn_on(device, led, color)
        led += 8
        time.sleep(sleep)
        turn_off(device)
    for i in range(5):
        turn_on(device, led, color)
        led -= 1
        time.sleep(sleep)
        turn_off(device)
    for i in range(4):
        turn_on(device, led, color)
        led -= 8
        time.sleep(sleep)
        turn_off(device)
    for i in range(4):
        turn_on(device, led, color)
        led += 1
        time.sleep(sleep)
        turn_off(device)
    for i in range(3):
        turn_on(device, led, color)
        led += 8
        time.sleep(sleep)
        turn_off(device)
    for i in range(3):
        turn_on(device, led, color)
        led -= 1
        time.sleep(sleep)
        turn_off(device)
    for i in range(2):
        turn_on(device, led, color)
        led -= 8
        time.sleep(sleep)
        turn_off(device)
    turn_on(device, led, color)
    time.sleep(sleep)
    turn_off(device)
    for i in range(3):
        turn_on(device, 71, color)
        turn_on(device, 72, color)
        turn_on(device, 63, color)
        turn_on(device, 64, color)
        time.sleep(sleep)
        turn_off(device)
        time.sleep(sleep)


def spiral_out_full(device, sleep):
    turn_off(device)
    led = 36
    color = randint(0, 128)
    # for x in range(7, 0, -1):
    for i in range(7):
        turn_on(device, led, color)
        led += 1
        time.sleep(sleep)
    for i in range(7):
        turn_on(device, led, color)
        led += 8
        time.sleep(sleep)
    for i in range(7):
        turn_on(device, led, color)
        led -= 1
        time.sleep(sleep)
    for i in range(6):
        turn_on(device, led, color)
        led -= 8
        time.sleep(sleep)
    for i in range(6):
        turn_on(device, led, color)
        led += 1
        time.sleep(sleep)
    for i in range(5):
        turn_on(device, led, color)
        led += 8
        time.sleep(sleep)
    for i in range(5):
        turn_on(device, led, color)
        led -= 1
        time.sleep(sleep)
    for i in range(4):
        turn_on(device, led, color)
        led -= 8
        time.sleep(sleep)
    for i in range(4):
        turn_on(device, led, color)
        led += 1
        time.sleep(sleep)
    for i in range(3):
        turn_on(device, led, color)
        led += 8
        time.sleep(sleep)
    for i in range(3):
        turn_on(device, led, color)
        led -= 1
        time.sleep(sleep)
    for i in range(2):
        turn_on(device, led, color)
        led -= 8
        time.sleep(sleep)
    turn_on(device, led, color)
    time.sleep(sleep)
    for i in range(3):
        turn_on(device, 71, color)
        turn_on(device, 72, color)
        turn_on(device, 63, color)
        turn_on(device, 64, color)
        time.sleep(sleep * 10)
        turn_off(device)
        time.sleep(sleep * 10)


def show(device, sleep):
    while True:
        blink_diagonally(device, sleep)
        spiral_out(device, sleep)
        spiral_out_full(device, sleep)
        blink_diagonally(device, sleep)


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


def to_fix():
    speaker = soundcard.default_speaker()
    microphones = soundcard.all_microphones(include_loopback=True)
    microphone = microphones[-3]

    # for microphone in microphones:
    #     print(microphone)
    # return

    turn_off(device)
    prev = 0
    color = randint(0, 127)
    print("{} is the color.".format(color))
    samples = 11200
    milisec = 56
    eighth = int(milisec / 8)
    # with speaker.player(samplerate=samples, channels=2) as mic:
    with microphone.recorder(samplerate=samples, channels=2) as mic:
        while True:
            # free_for_all()
            turn_off(device)
            audio = mic.record(numframes=milisec)
            curr = numpy.average(audio)
            # if prev < curr:
            # 	turn_off(device)
            prev = curr
            count = 0
            # for slic in range(0, len(audio), eighth):
            # 	two_channel_viz(count, numpy.average(audio[slic:slic+eighth][0]), numpy.average(audio[slic:slic+eighth][1]), color)
            # 	count += 1

            # for slic in range(0, len(audio), eighth):
            # 	turn_on_col_reverse(count, numpy.average(audio[slic:slic+14]), color)
            # 	count += 1

            for slic in range(0, len(audio), eighth):
                turn_on_col(count, numpy.average(audio[slic : slic + 14]), color)
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
            # 		turn_off(device)

    turn_off(device)


def midi_device(midi_device_name: str):
    midiout = rtmidi.MidiOut()
    available_ports = midiout.get_ports()
    print(available_ports)

    for port in available_ports:
        if midi_device_name in port and "MIDIOUT" not in port:
            return midiout.open_port(int(port[-1]))


sleep = 0.02


if __name__ == "__main__":
    # spiral_out_full(0.05)
    # to_fix()

    # ableton_push = midi_device("Ableton Push 2")
    loop_midi = midi_device("loopMIDI")

    turn_off(loop_midi)

    while True:
        # free_for_all()
        # show(loop_midi, 0.5)
        # matrix(loop_midi, 0.5)

        scale(loop_midi, 1)
