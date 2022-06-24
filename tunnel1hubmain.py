import RPi.GPIO as GPIO
import time
import pygame

# SETUP
input_pins = {13: False,  # Sensor/Screen 1
              19: False,  # Sensor/Screen 2
              26: False,  # Sensor/Screen 3
              16: False,  # Sensor/Screen 4
              20: False,  # Sensor/Screen 5
              21: False  # Sensor/Screen 6
              }

outcomes = {0: {"type": "GPIO", "pin": 23},  # Lights
            1: {"type": "GPIO", "pin": 24},  # Air Blast
            2: {"type": "sound", "channel": 1},  # Vocal
            3: {"type": "sound", "channel": 2},  # Brass/Flute
            4: {"type": "sound", "channel": 3},  # Perc
            5: {"type": "sound", "channel": 4},  # Siren/Air Horn
            6: {"type": "sound", "channel": 5},  # Low Rumble
            7: {"type": "sound", "channel": 6},  # Scratch
            }

input_output = {13: [2],  # Sensor/Screen 1
                19: [3],  # Sensor/Screen 2
                26: [5],  # Sensor/Screen 3
                16: [4],  # Sensor/Screen 4
                20: [6, 1],  # Sensor/Screen 5
                21: [7, 0]  # Sensor/Screen 6
                }

# input_output = {13: [3],  # Sensor/Screen 1
#                 19: [1, 6],  # Sensor/Screen 2
#                 26: [5],  # Sensor/Screen 3
#                 16: [4],  # Sensor/Screen 4
#                 20: [7],  # Sensor/Screen 5
#                 21: [2]  # Sensor/Screen 6
#                 }

sound_files = {1: [".\\music\\Coke1 AudioClip1 Vocal.ogg",
                   ".\\music\\Coke2 AudioClip1 Vocal.ogg",
                   ".\\music\\Coke AudioClip1 Vocal.ogg"],
               2: [".\\music\\Coke1 AudioClip2 Brass.ogg",
                   ".\\music\\Coke2 AudioClip2 Brass.ogg",
                   ".\\music\\Coke AudioClip2 Flute.ogg"],
               3: [".\\music\\Coke1 AudioClip3 Perc.ogg",
                   ".\\music\\Coke2 AudioClip3 Perc.ogg",
                   ".\\music\\Coke AudioClip3 Perc.ogg"],
               4: [".\\music\\Coke1 AudioClip4 Airhorn.ogg",
                   ".\\music\\Coke2 AudioClip4 Siren.ogg",
                   ".\\music\\Coke AudioClip4 Siren.ogg"],
               5: [".\\music\\Coke1 AudioClip5 LowRumble.ogg",
                   ".\\music\\Coke2 AudioClip5 LowRumble.ogg",
                   ".\\music\\Coke AudioClip5 LowRumble.ogg"],
               6: [".\\music\\Coke1 AudioClip6 Scratch.ogg",
                   ".\\music\\Coke2 AudioClip6 Scratch.ogg",
                   ".\\music\\Coke AudioClip6 Scratch.ogg"]
               }

output_pins = [outcomes[i]["pin"] for i in outcomes.keys() if outcomes[i]["type"] == "GPIO"]

GPIO.setmode(GPIO.BCM)

for i_pin in input_pins.keys():
    GPIO.setup(i_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

for o_pin in output_pins:
    GPIO.setup(o_pin, GPIO.OUT)

# Sound File Setup
path = "/home/pi/Documents/"
pygame.mixer.init()
speaker_volume = 1.0  # 100% Volume
pygame.mixer.music.set_volume(speaker_volume)

for i in range(len(sound_files)):
    pygame.mixer.Channel(i).play(pygame.mixer.Sound(path + sound_files[i]), loops=-1)
    pygame.mixer.Channel(i).set_volume(0.0)

pygame.mixer.Channel(0).set_volume(1.0)

### Main Loop
while True:
    for in_pin in input_pins.keys():

        previous_state = input_pins[in_pin]
        current_state = GPIO.input(in_pin)

        if current_state and not previous_state:
            print("====")
            print("Input Pin " + str(in_pin) + " rising")

            for event in input_output[in_pin]:
                if outcomes[event]["type"] == "GPIO":
                    GPIO.output(outcomes[event]["pin"], 1)
                    print("Output Pin " + str(outcomes[event]["pin"]) + " high.")
                elif outcomes[event]["type"] == "sound":
                    pygame.mixer.Channel(outcomes[event]["channel"]).set_volume(1.0)
                    print("Channel " + str(outcomes[event]["channel"]) + " high.")

        elif not current_state and previous_state:
            print("====")
            print("Input Pin " + str(in_pin) + " falling")

            for event in input_output[in_pin]:
                if outcomes[event]["type"] == "GPIO":
                    GPIO.output(outcomes[event]["pin"], 1)
                    print("Output Pin " + str(outcomes[event]["pin"]) + " low.")
                elif outcomes[event]["type"] == "sound":
                    pygame.mixer.Channel(outcomes[event]["channel"]).set_volume(1.0)
                    print("Channel " + str(outcomes[event]["channel"]) + " low.")

        input_pins[in_pin] = current_state
    time.sleep(0.01)
