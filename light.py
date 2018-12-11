from __future__ import division
import RPi.GPIO as GPIO
import time
import csv
import os

probing_seconds = 0.01
wh_per_blink = 1000/2500

GPIO.setmode(GPIO.BCM)
GPIO.setup(16,GPIO.IN)

total_num_of_pulses = 0

readings_dir = 'readings'
if not os.path.exists(readings_dir):
    os.makedirs(readings_dir)

def getPulse():
    is_in_pulse = False
    global total_num_of_pulses

    while True:
        diode_is_active = not GPIO.input(16)
	if(not is_in_pulse and diode_is_active):
	    is_in_pulse = True
            total_num_of_pulses += 1
            continue
        if(is_in_pulse and not diode_is_active):
            break
        time.sleep(probing_seconds)

while True:
    curr_time = time.time()
    getPulse()
    new_time = time.time()

    if(new_time // 60 != curr_time // 60):
        target_day_file = readings_dir + '/day_' + time.strftime('%Y%m%d', time.localtime(curr_time)) + '.csv'
        with open(target_day_file, 'a') as f:
            writer = csv.writer(f)
            writer.writerow([time.strftime('%Y-%m-%d %H:%M:00', time.localtime(curr_time)), total_num_of_pulses])

    diff_time = new_time - curr_time
    curr_pwr_kwats = 3600 / diff_time * wh_per_blink
    total_consumption_kwh = total_num_of_pulses * wh_per_blink / 1000

    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(new_time)))
    print('Curr Power          = {curr_pwr_kwats}'.format(**locals()))
    print('Pulses              = {total_num_of_pulses}'.format(**locals()))
    print('Total consumption   = {total_consumption_kwh}'.format(**locals()))
    print
