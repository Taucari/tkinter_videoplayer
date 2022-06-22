import tkinter
import vlc
import platform
from PIL import ImageTk, Image

# This global current_state variable determines which video and how long to wait for each video
current_state = 0


# Just a class to make it easier to define the vlc player in a tkinter Frame easier
class Screen(tkinter.Frame):
    """
    Screen widget: Embedded video player from local or Youtube
    """

    def __init__(self, parent, *args, **kwargs):
        tkinter.Frame.__init__(self, parent, bg='black')
        self.parent = parent
        # Creating VLC player --high-priority
        # self.instance = vlc.Instance("--verbose=0 --no-xlib --vout mmal_vout --mouse-hide-timeout=0 --no-mouse-events")
        self.instance = vlc.Instance("--verbose=0 --mouse-hide-timeout=0 --no-mouse-events")
        self.player = self.instance.media_player_new()

    # You shouldn't need this stuff
    #    def GetHandle(self):
    #        # Getting frame ID
    #        return self.winfo_id()

    def play(self, _source):
        # Function to start player from given source
        media = self.instance.media_new(_source)
        media.get_mrl()
        self.player.set_media(media)

        # When different functions to be used based on when running on Windows vs on Linux
        if platform.system() == 'Windows':
            print("Running on Windows")
            self.player.set_hwnd(self.winfo_id())
        elif platform.system() == 'Linux':
            print("Running on Linux")
            self.player.set_xwindow(self.winfo_id())

        self.player.play()

    def pause_now(self):
        self.player.set_pause(1)


def hide_button():
    # Function to be called when hiding the button as the player appears
    button.place_forget()


def return_button():
    # Function to be called when un-hiding the button as the player disappears
    button.place(anchor="center", relx=0.5, rely=0.5)


def hide_player():
    # Function to hide the player
    player.pause_now()
    player.place_forget()


def return_player():
    # Function to un-hide the player, probably change width and height for different clips (can insert stator and the
    # clip selector dict for control)
    player.place(x=0, y=0, width=1920, height=1080)


def button_press(event=None):
    # Function that is called when the button is pressed
    # Clip is selected with the stator from the remainder of the division with the clip_selector dict
    global current_state
    clip_selector = {0: {'path': r"clip1.mp4", 'length': 12000},
                     1: {'path': r"clip2.mp4", 'length': 14000},
                     2: {'path': r"clip3.mp4", 'length': 17000}}
    stator = current_state % len(clip_selector)
    print("Button pressed " + str(current_state) + " times.")

    # Hide button and un-hide player
    hide_button()
    return_player()

    # Play the right clip
    player.play(clip_selector[stator]['path'])

    # After the clip is finished, hide the player and return the button
    r.after(clip_selector[stator]['length'], hide_player)
    r.after(clip_selector[stator]['length'], return_button)

    # Increment the counter
    current_state += 1


def close(event=None):
    # Function to be called when 'ESC' button is pressed
    print("Program User Terminated")
    r.destroy()


# Start of the actual configuration of tkinter gui
r = tkinter.Tk()  # root definition
r.configure(background='black')
r.resizable(False, False)
r.attributes("-fullscreen", True)
r.config(cursor="none")

# file_name = tkinter.PhotoImage(file=r"C:\Users\wangh\PycharmProjects\tkinter_videoplayer\background.png")
file_name = ImageTk.PhotoImage(Image.open("background.png"))
background_label = tkinter.Label(r, image=file_name)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Initial creation of a screen object
player = Screen(r)

# Loading the image to be used as a button
photo = tkinter.PhotoImage(file=r"C:\Users\wangh\PycharmProjects\tkinter_videoplayer\check.png")
button = tkinter.Label(r, image=photo)
# Binding the left mouse click on the image as a button
button.bind('<Button-1>', button_press)

# Binding the escape key to close the program whenever
r.bind('<Escape>', close)

# Button Init
return_button()

# Start main gui loop
r.mainloop()
