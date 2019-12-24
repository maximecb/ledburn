#!/usr/bin/env python3

import argparse
import numpy as np
import sounddevice as sd

import argparse
import math
import shutil

import numpy as np
import sounddevice as sd

usage_line = ' press <enter> to quit, +<enter> or -<enter> to change scaling '

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

try:
    columns, _ = shutil.get_terminal_size()
except AttributeError:
    columns = 80

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
#parser = argparse.ArgumentParser(
#    description=__doc__ + '\n\nSupported keys:' + usage_line,
#    formatter_class=argparse.RawDescriptionHelpFormatter,
#    parents=[parser])
parser.add_argument(
    '-b', '--block-duration', type=float, metavar='DURATION', default=50,
    help='block size (default %(default)s milliseconds)')
parser.add_argument(
    '-c', '--columns', type=int, default=columns,
    help='width of spectrogram')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-g', '--gain', type=float, default=10,
    help='initial gain factor (default %(default)s)')
parser.add_argument(
    '-r', '--range', type=float, nargs=2,
    metavar=('LOW', 'HIGH'), default=[100, 2000],
    help='frequency range (default %(default)s Hz)')
args = parser.parse_args(remaining)
low, high = args.range
if high <= low:
    parser.error('HIGH must be greater than LOW')

# Create a nice output gradient using ANSI escape sequences.
# Stolen from https://gist.github.com/maurisvh/df919538bcef391bc89f
colors = 30, 34, 35, 91, 93, 97
chars = ' :%#\t#%:'
gradient = []
for bg, fg in zip(colors, colors[1:]):
    for char in chars:
        if char == '\t':
            bg, fg = fg, bg
        else:
            gradient.append('\x1b[{};{}m{}'.format(fg, bg + 10, char))


moving_avg = 0
moving_var = 1

def calc_moving_avg(old, new, gamma=0.995):
    return gamma * old + (1 - gamma) * new 

def update_moving_stats(old_avg, old_var, data):
    avg = calc_moving_avg(old_avg, data)
    var = calc_moving_avg(old_var, data ** 2)
    return avg, var
    


def callback(indata, frames, time, status):
    global moving_avg
    global moving_var
    #if status:
    #     text = ' ' + str(status) + ' '
    #     print('\x1b[34;40m', text.center(args.columns, '#'),
    #          '\x1b[0m', sep='')
    if any(indata):
        max_bin = 7
        avg, std = moving_avg, moving_var**0.5
        magnitude = np.abs(np.fft.rfft(indata[:, 0], n=fftsize))

        energy = sum(magnitude[:max_bin] * (1.0 /(1 + np.arange(max_bin))))
        moving_avg, moving_var = update_moving_stats(moving_avg, moving_var, energy)

        threshold = (energy - avg )/(std) - 0.5
 
        #magnitude *= args.gain / fftsize
        #line = (gradient[int(np.clip(x, 0, 1) * (len(gradient) - 1))]
        #        for x in magnitude[low_bin:low_bin + args.columns])
        if threshold > 0:
           print("///////////////////////////////////////////////////////\r", end="")
        else:
           print("                                                       \r", end="")
    else:
        print('no input')





try:
    samplerate = sd.query_devices(args.device, 'input')['default_samplerate']

    delta_f = (high - low) / (args.columns - 1)
    fftsize = math.ceil(samplerate / delta_f)
    low_bin = math.floor(low / delta_f)

    with sd.InputStream(device=args.device, channels=1, callback=callback,
                        blocksize=int(samplerate * args.block_duration / 1000),
                        samplerate=samplerate):
        while True:
            response = input()
            if response in ('', 'q', 'Q'):
                break
            for ch in response:
                if ch == '+':
                    args.gain *= 2
                elif ch == '-':
                    args.gain /= 2
                else:
                    print('\x1b[31;40m', usage_line.center(args.columns, '#'),
                          '\x1b[0m\r', sep='')
                    break

except KeyboardInterrupt:
    parser.exit('Interrupted by user')
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))