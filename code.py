import time
import pwmio
import board
import random
import neopixel
import digitalio
from adafruit_debouncer import Debouncer
from adafruit_ticks import ticks_ms, ticks_add, ticks_less

pixels = neopixel.NeoPixel(board.A3, 5*5, brightness=.07, auto_write=False)
pixels.fill(0)
pixels.show()

piezo = pwmio.PWMOut(board.A2, duty_cycle=0, frequency=440, variable_frequency=True)
TONE_FREQ = [ 262,  # C4
              294,  # D4
              330,  # E4
              349,  # F4
              392,  # G4
              440,  # A4
              494,  # B4
              523,
              1047,
              2093 ] 
for i in range(1):
    for f in TONE_FREQ:
        piezo.frequency = f
        piezo.duty_cycle = 65535 // 2  # On 50%
        time.sleep(0.05)  # On for 1/4 second
        piezo.duty_cycle = 0  # Off
        time.sleep(0.0125)  # Pause between notes
    time.sleep(0.05)

hue = 1
RED = 0x100000
GREEN = 0x001000
BLUE = 0x000010
YELLOW = 0x101000
PURPLE = 0x100010
CLEAR = 0x000000

REEL = [RED,GREEN,YELLOW,BLUE,PURPLE,YELLOW,RED,GREEN,BLUE,RED,YELLOW,RED,RED]

pin = digitalio.DigitalInOut(board.A1)
pin.direction = digitalio.Direction.INPUT
pin.pull = digitalio.Pull.UP
switch = Debouncer(pin)

# Inverted matrix where pixel[0] is bottom right
# for i in range(5):
#     for j in range(5):
#         pixels[20-(5*i-j)] =  #TOP LEFT ACROSS
#         pixels[20-(5*j-i)] =  #TOP LEFT DOWN
#         pixels[5*i+j] = #BOTTOM LEFT ACROSS
#         pixels[5*j+i] = #BOTTOM LEFT UP
#         pixels[24-(i+j*5)] = #TOP RIGHT DOWN
#         pixels[24-(5*i+j)] = #TOP RIGHT ACROSS

for i in range(5):
    for j in range(5):
        pixels[20-(5*j-i)] = GREEN
        pixels.show()
        time.sleep(.01)

time.sleep(1)
for i in range(5): 
    for j in range(5):
        pixels[24-(5*i+j)] = CLEAR    
        pixels.show()
        time.sleep(.01)
def win():
    for x in range(8):
        pixels.brightness = 0.5
        pixels.show()
        # time.sleep(.1)
        piezo.frequency = 1980
        piezo.duty_cycle = 65535 // 2
        time.sleep(0.15)  
        # piezo.duty_cycle = 0  # Off
        # time.sleep(0.001)
        piezo.frequency = 2637
        time.sleep(0.35)
        pixels.brightness = 0.2
        pixels.show()
        piezo.duty_cycle = 0  # Off
        time.sleep(.01)

while True:
    switch.update()
    if switch.rose:
        print("Just released")
        results = []
        for i in range(12):
            for i in range(5):
                for j in range(5):
                    pixels[20-(5*j-i)] = pixels[1-(5*j-i)]
                    piezo.frequency = TONE_FREQ[-i]
                    piezo.duty_cycle = 65535 // 8
                    time.sleep(0.001)
                    piezo.duty_cycle = 0
                    time.sleep(0.001)
                    pixels.show()
                time.sleep(.00)

        for i in range(5): #COLUMNS
            offset = random.randint(0,len(REEL))
            for j in range(5): #ROWS
                item = REEL[j-offset]
                if (j == 2):
                    results.append(hex(item))
                    pixels[20-(5*j-i)] = int(hex(item*10))
                    piezo.frequency = 987
                    piezo.duty_cycle = 65535 // 4
                    time.sleep(0.15)
                    piezo.duty_cycle = 0
                    time.sleep(0.01)
                    if i == 4:
                        piezo.frequency = 2637
                        piezo.duty_cycle = 65535 // 2
                        time.sleep(0.5)
                    else:
                        piezo.frequency = 1318
                        piezo.duty_cycle = 65535 // 4
                        time.sleep(0.125)
                    piezo.duty_cycle = 0
                    time.sleep(0.0125)
                else:
                    pixels[20-(5*j-i)] = int(hex(item))
                pixels.show()
                time.sleep(.1)

        if len(set(results))<=2: # 2 = Four of a kind OR 'Fullhouse'. 1 = Five of a kind
            win()
        print(results, len(set(results)))