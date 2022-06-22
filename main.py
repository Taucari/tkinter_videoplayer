import tkinter
import vlc
import platform
from PIL import ImageTk, Image

current_state = 0


class Screen(tkinter.Frame):
    """
    Screen widget: Embedded video player from local or Youtube
    """

    def __init__(self, parent, *args, **kwargs):
        tkinter.Frame.__init__(self, parent, bg='black')
        self.parent = parent
        # Creating VLC player --high-priority
        self.instance = vlc.Instance("--verbose=0 --no-xlib --vout mmal_vout --mouse-hide-timeout=0 --no-mouse-events")
        self.player = self.instance.media_player_new()

    def GetHandle(self):
        # Getting frame ID
        return self.winfo_id()

    def play(self, _source):
        # Function to start player from given source
        media = self.instance.media_new(_source)
        media.get_mrl()
        self.player.set_media(media)

        if platform.system() == 'Windows':
            print("Running on Windows")
            self.player.set_hwnd(self.winfo_id())
        elif platform.system() == 'Linux':
            print("Running on Linux")
            self.player.set_xwindow(self.winfo_id())

        self.player.play()


def hide_button():
    button.place_forget()


def return_button():
    button.place(anchor="center", relx=0.5, rely=0.5)


def hide_player():
    player.place_forget()


def return_player():
    player.place(x=0, y=0, width=1920, height=1080)


def button_press(event=None):
    global current_state
    clip_selector = {0: {'path': r"clip1.mp4", 'length': 30000},
                     1: {'path': r"clip2.mp4", 'length': 30000},
                     2: {'path': r"clip3.mp4", 'length': 30000}}
    stator = current_state % len(clip_selector)

    hide_button()
    return_player()
    player.play(clip_selector[stator]['path'])

    r.after(clip_selector[stator]['length'], hide_player)
    r.after(clip_selector[stator]['length'], return_button)
    current_state += 1


def close(event=None):
    print("Program User Terminated")
    r.destroy()


r = tkinter.Tk()
r.configure(background='black')
r.resizable(False, False)
r.attributes("-fullscreen", True)
r.config(cursor="none")



# file_name = tkinter.PhotoImage(file=r"C:\Users\wangh\PycharmProjects\tkinter_videoplayer\background.png")
file_name = ImageTk.PhotoImage(Image.open("background.png"))
background_label = tkinter.Label(r, image=file_name)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

player = Screen(r)

photo = tkinter.PhotoImage(file=r"C:\Users\wangh\PycharmProjects\tkinter_videoplayer\check.png")
button = tkinter.Label(r, image=photo)
button.bind('<Button-1>', button_press)

r.bind('<Escape>', close)

return_button()

r.mainloop()
