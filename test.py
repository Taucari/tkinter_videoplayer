import vlc
import tkinter as tk


class Screen(tk.Frame):
    '''
    Screen widget: Embedded video player from local or youtube
    '''

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, bg='black')
        self.parent = parent
        # Creating VLC player
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

    def GetHandle(self):
        # Getting frame ID
        return self.winfo_id()

    def play(self, _source):
        # Function to start player from given source
        media = self.instance.media_new(_source)
        media.get_mrl()
        self.player.set_media(media)
        self.player.set_hwnd(self.winfo_id())
        self.player.play()


r = tk.Tk()
player = Screen(r)
player.place(x=0, y=0, width=1280, height=720)
player.play('clip1.mp4')
r.mainloop()
