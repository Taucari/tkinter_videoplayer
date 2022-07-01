import pygame
import time
import RPi.GPIO

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

path = "/home/pi/music/"
sound_files = {1: [{"name": "Coke1 AudioClip1 Vocal.ogg", "volume": 0.25},
                   {"name": "Coke2 AudioClip1 Vocal.ogg", "volume": 0.25},
                   {"name": "Coke3 AudioClip1 Vocal.ogg", "volume": 0.25}],
               2: [{"name": "Coke1 AudioClip2 Brass.ogg", "volume": 0.25},
                   {"name": "Coke2 AudioClip2 Brass.ogg", "volume": 0.25},
                   {"name": "Coke3 AudioClip2 Flute.ogg", "volume": 0.25}],
               3: [{"name": "Coke1 AudioClip3 Perc.ogg", "volume": 0.25},
                   {"name": "Coke2 AudioClip3 Perc.ogg", "volume": 0.25},
                   {"name": "Coke3 AudioClip3 Perc.ogg", "volume": 0.25}],
               4: [{"name": "Coke1 AudioClip4 Airhorn.ogg", "volume": 0.25},
                   {"name": "Coke2 AudioClip4 Siren.ogg", "volume": 0.25},
                   {"name": "Coke3 AudioClip4 Siren.ogg", "volume": 0.25}],
               5: [{"name": "Coke1 AudioClip5 LowRumble.ogg", "volume": 0.25},
                   {"name": "Coke2 AudioClip5 LowRumble.ogg", "volume": 0.25},
                   {"name": "Coke3 AudioClip5 LowRumble.ogg", "volume": 0.25}],
               6: [{"name": "Coke1 AudioClip6 Scratch.ogg", "volume": 0.25},
                   {"name": "Coke2 AudioClip6 Scratch.ogg", "volume": 0.25},
                   {"name": "Coke3 AudioClip6 Scrape.ogg", "volume": 0.25}]
               }

output_pins = [outcomes[i]["pin"] for i in outcomes.keys() if outcomes[i]["type"] == "GPIO"]

RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setup(25, RPi.GPIO.OUT)

for i_pin in input_pins.keys():
    RPi.GPIO.setup(i_pin, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)

for o_pin in output_pins:
    RPi.GPIO.setup(o_pin, RPi.GPIO.OUT)

# define own event type
NEXT = pygame.USEREVENT + 1

header = "/home/pi/music/"
footer = ['Coke1 Main.ogg', 'Coke2 Main.ogg', 'Coke3 Main.ogg']
main_track_volume = [0.25, 0.25, 0.25]
playlist = [header + foot for foot in footer]
# playlist = ['Coke1_Main.ogg', 'Coke2_Main.ogg', 'Coke3_Main.wav']

tracks_number = len(playlist)
current_track = 0

# pygame init and all that
pygame.init()
pygame.mixer.init(48000, -16, 2, 1024)

# start first track
pygame.mixer.music.load(playlist[current_track])
pygame.mixer.music.play()
pygame.mixer.music.set_volume(main_track_volume[current_track])

# Set static light mode
RPi.GPIO.output(25, 1)

# send event NEXT every time tracks ends
pygame.mixer.music.set_endevent(NEXT)

print("Playing Track: " + str(playlist[current_track]))
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == NEXT:

            # get next track (modulo number of tracks)
            current_track = (current_track + 1) % tracks_number

            print("Playing Track: " + str(playlist[current_track]))

            pygame.mixer.music.load(playlist[current_track])
            pygame.mixer.music.play()

    for in_pin in input_pins.keys():

        previous_state = input_pins[in_pin]
        current_state = RPi.GPIO.input(in_pin)

        if current_state and not previous_state:
            print("====")
            print("Input Pin " + str(in_pin) + " rising")

            for event in input_output[in_pin]:
                if outcomes[event]["type"] == "GPIO":
                    RPi.GPIO.output(outcomes[event]["pin"], 1)
                    print("Output Pin " + str(outcomes[event]["pin"]) + " high.")
                elif outcomes[event]["type"] == "sound":
                    channel_number = outcomes[event]["channel"]
                    print("Triggering: " + str(sound_files[channel_number][current_track]["name"]))
                    sound_effect = pygame.mixer.Sound(path + sound_files[channel_number][current_track]["name"])
                    pygame.mixer.Channel(channel_number).play(sound_effect)
                    pygame.mixer.Channel(channel_number).set_volume(sound_files[channel_number][current_track]["volume"])
                    print("Channel " + str(outcomes[event]["channel"]) + " high.")

        elif not current_state and previous_state:
            print("====")
            print("Input Pin " + str(in_pin) + " falling")

            for event in input_output[in_pin]:
                if outcomes[event]["type"] == "GPIO":
                    RPi.GPIO.output(outcomes[event]["pin"], 1)
                    print("Output Pin " + str(outcomes[event]["pin"]) + " low.")
                elif outcomes[event]["type"] == "sound":
                    # pygame.mixer.Channel(outcomes[event]["channel"]).set_volume(1.0)
                    print("Channel " + str(outcomes[event]["channel"]) + " low.")

        input_pins[in_pin] = current_state
    time.sleep(0.01)

pygame.quit()
