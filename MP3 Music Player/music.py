from tkinter import *
import pygame
import os
import threading
import time
from mutagen.mp3 import MP3
from tkinter.filedialog import askdirectory
from tkinter.messagebox import *
from tkinter import ttk
from PIL import Image, ImageTk


class Player:
  def __init__(self, master):
    self.master = master
    pygame.init()
    pygame.mixer.init()
    self.threads = []
     
    def get_icon():
      self.winicon = PhotoImage(file="icon.png")
      master.iconphoto(False, self.winicon)
     
    def icon():
      myth = threading.Thread(target=get_icon)
      self.threads.append(myth)
      myth.start()
    icon()

    PLAY = "▶️"
    PAUSE = "⏸️"
    RWD = "⏮"
    FWD = "⏭"
    STOP = "⏹️"
    UNPAUSE = "||"
    mute = "🔇"
    unmute = "🔊"
    vol_mute = 0.0
    vol_unmute = 1

    # listbox
    self.scroll = Scrollbar(master)
    self.play_list = Listbox(master, font="Courgette 12 ", bd=5, bg="lavender", width=37, height=19, selectbackground="black")
    self.play_list.place(x=600, y=77)
    self.scroll.place(x=946, y=80, height=389, width=15)
    self.scroll.config(command=self.play_list.yview)
    self.play_list.config(yscrollcommand=self.scroll.set)
    
    self.img1 = Image.open('bg.jpg')
    self.img1 =  self.img1.resize((600, 470), Image.ANTIALIAS)
    self.img = ImageTk.PhotoImage(self.img1)
    self.lab = Label(master)
    self.lab.grid(row=0, column=0)
    self.lab["compound"] = LEFT
    self.lab["image"] = self.img
   
    # Show play
    self.var = StringVar()
    self.var.set("")
    self.song_title = Label(master, font="Courgette 12 bold", bg="gray10", fg="white", width=60, textvariable=self.var)
    self.song_title.place(x=3, y=0)

    # Music listbox
    def append_listbox():
      global song_list
      try:
        directory = askdirectory()
        os.chdir(directory)  # change current dir
        song_list = os.listdir()
        song_list.reverse()
        for item in song_list:  # returns song list
          pos = 0
          self.play_list.insert(pos, item)
          pos += 1
        global size
        index = 0
        size = len(song_list)
        self.play_list.selection_set(index)
        self.play_list.see(index)
        self.play_list.activate(index)
        self.play_list.selection_anchor(index)
          
      except:
        showerror("File Selected Error!", "Please Select a file Correclty") 

    # Add Songs
    def add_songs_playlist():
      myth = threading.Thread(target=append_listbox)
      self.threads.append(myth)
      myth.start()

    # get music time
    def get_time():
      current_time = pygame.mixer.music.get_pos() / 1000
      formated_time = time.strftime("%H:%M:%S", time.gmtime(current_time))
      next_one = self.play_list.curselection()
      song = self.play_list.get(next_one)
      song_timer = MP3(song)
      song_length = int(song_timer.info.length)
      format_for_length = time.strftime("%H:%M:%S", time.gmtime(song_length))
      self.label_time.config(text=f"{ format_for_length} / {formated_time}")
      self.progress["maximum"] = song_length
      self.progress["value"] = int(current_time)
      master.after(100, get_time)
    
    # play music
    def Play_music():
      try:
        track = self.play_list.get(ACTIVE)
        pygame.mixer.music.load(track)
        self.var.set(track)
        pygame.mixer.music.play()
        get_time()
      except:
        showerror("No Music", "Please load the Music!!")


    def playAll():
      try:
        index = 0
        for i in range(size):
          self.play_list.select_clear(0, END)
          self.play_list.selection_set(index, last=None)
          self.play_list.see(index)
          self.play_list.activate(index)
          self.play_list.selection_anchor(index)
          track = self.play_list.get(index)
          pygame.mixer.music.load(track)
          self.var.set(track)
          pygame.mixer.music.play()
          current_song = self.play_list.curselection()
          song = self.play_list.get(current_song)
          song_timer = MP3(song)
          song_length = int(song_timer.info.length) * 1000
          get_time()
          index += 1      
      except:
        showerror("No Songs in Playlist", "Please add Music")
    def play_all():
      myth = threading.Thread(target=playAll)
      self.threads.append(myth)
      myth.start()
            
    # pause / unpause btn
    def pause_unpause():
      if self.btn_pause['text'] == PAUSE:
        pygame.mixer.music.pause()
        self.btn_pause['text'] = UNPAUSE
      elif self.btn_pause['text'] == UNPAUSE:
        pygame.mixer.music.unpause()
        self.btn_pause['text'] = PAUSE

    # play music on diffent thread
    def play_thread():
      myth = threading.Thread(target=Play_music)
      self.threads.append(myth)
      myth.start()
    master.bind("<space>", lambda x: play_thread())

    # Stop btn
    def stop():
      pygame.mixer.music.stop()

    # Volume increase / decrease
    def volume(x):
      pygame.mixer.music.set_volume(self.volume_slider.get())

    # mute / unmute
    def muted():
      if self.btn_mute['text'] == unmute:
        pygame.mixer.music.set_volume(vol_mute)
        self.volume_slider.set(vol_mute)
        self.btn_mute['fg'] = "red"
        self.btn_mute['text'] = mute
      elif self.btn_mute['text'] == mute:
        pygame.mixer.music.set_volume(vol_unmute)
        self.volume_slider.set(vol_unmute)
        self.btn_mute['fg'] = "white"
        self.btn_mute['text'] = unmute

    # next song
    def nextSong():
      try:
        next_one = self.play_list.curselection()
        next_one = next_one[0]+1
        song = self.play_list.get(next_one)
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()
        self.play_list.select_clear(0, END)
        self.play_list.activate(next_one)
        self.play_list.selection_set(next_one, last=None)
        self.var.set(song)
        get_time()
        self.play_list.see(next_one)
      except:
        showerror("No Next Song", "Please press the previous button")
    def next():
      myth = threading.Thread(target=nextSong)
      self.threads.append(myth)
      myth.start()

    # previous song
    def prevSong():
      try:
        next_one = self.play_list.curselection()
        next_one = next_one[0]-1
        song = self.play_list.get(next_one)
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()
        self.play_list.select_clear(0, END)
        self.play_list.activate(next_one)
        self.play_list.selection_set(next_one, last=None)
        self.var.set(song)
        get_time()
        self.play_list.see(next_one)
      except:
        showerror("No previous Song", "Please press the Next button")
    def prev():
      myth = threading.Thread(target=prevSong)
      self.threads.append(myth)
      myth.start()

    self.master.bind('<Left>', lambda x: prev())
    self.master.bind('<Right>', lambda x: next())


    # Buttons
    self.btn_prev = Button(master, text=RWD, width=4, bd=4, bg="black", fg="white", font="Montserrat, 15", command=prev)
    self.btn_prev.place(x=10, y=418)
    self.btn_pause = Button(master, text=PAUSE, width=4, bd=4, font="Montserrat, 15", bg="black", fg="white", command=pause_unpause)
    self.btn_pause.place(x=78, y=418)
    self.btn_play = Button(master, text=PLAY, width=4, bd=4, bg="black", fg="white", font="Montserrat, 15", command=play_thread)
    self.btn_play.place(x=146, y=418)
    self.btn_stop = Button(master, text=STOP, width=4, bd=4, font="Montserrat, 15", bg="black", fg="white", command=stop)
    self.btn_stop.place(x=213, y=418)
    self.btn_next = Button(master, text=FWD, width=4, bd=4, font="Montserrat, 15", bg="black", fg="white", command=next)
    self.btn_next.place(x=281, y=418)
    self.buttonPlayall = Button(self.master, text='\U0001F500', bg='black', fg='white', font='Montserrat, 15', bd=4, width=4, command=play_all)
    self.buttonPlayall.place(x=348, y=418)
    self.btn_mute = Button(master, text=unmute, width=4, bd=4, font="Montserrat, 15", bg="black", fg="white", command=muted)
    self.btn_mute.place(x=414, y=418)
    self.label_playlist = Label(master, text=u" ♫ Music Playlist ♫ ", width=31, font="Courgette 15", bg="lavender")
    self.label_playlist.place(x=610, y=6)
    self.button_load_music = Button(master, text="♫ Upload Music ♫", width=43, bd=3, font="Courgette 11", bg="black", fg="white", command=add_songs_playlist)
    self.button_load_music.place(x=605, y=43)
    self.style = ttk.Style()
    self.style.configure("myStyle.Horizontal.TScale", background="#505050")
    self.volume_slider = ttk.Scale(self.lab, from_=0, to=1, orient=HORIZONTAL, value=1, length=120, style="myStyle.Horizontal.TScale", command=volume)
    self.volume_slider.place(x=475, y=426)
    self.progress = ttk.Progressbar(self.lab, orient=HORIZONTAL, value=0, length = 453, mode = 'determinate')
    self.progress.place(x=0, y=389)
    self.label_time = Label(master, text="00:00:00 / 00:00:00", width=17, font="Montserrat, 10", bg="black", fg="white")
    self.label_time.place(x=460, y=391)


def main():
  root = Tk()
  playerapp = Player(root)
  root.geometry("963x470+200+100")
  root.title("Mp3 Music Player")
  root.configure(bg="gray10")
  root.resizable(width=0, height=0)
  root.mainloop()

if __name__ == "__main__":
   main()
