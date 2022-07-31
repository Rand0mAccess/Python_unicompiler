from tkinter import *
from tkinter import filedialog,messagebox
from pytube import YouTube,Playlist
import os


def select_path():
  path = filedialog.askdirectory()
  path_label.config(text=path)

def download():
  get_link = text.get()
  path = path_label.cget("text") 

  if check.get() == 1:
    yt=YouTube(get_link)
    screen.title('Downloading...')
    yt.streams.get_highest_resolution().download(path)
    messagebox.showinfo('Success','Video Downloaded Successfully')
    screen.title('Youtube Video Downloader')
    os.startfile(path)

  if check.get() == 2:
    yt_plst=Playlist(get_link)
    screen.title('Downloading...')
    for videos in yt_plst.videos:
      videos.streams.get_highest_resolution().download(path)
    messagebox.showinfo('Success','Playlist Downloaded Succesfully')
    screen.title('Youtube Video Downloader')
    os.startfile(path)



# GUI Part
screen = Tk()
p = PhotoImage(file = 'icon.png')
screen.iconphoto(False, p)   
screen.title('Youtube Video Downloader')


frame1 = Frame(screen, bd=5)
frame1.grid(row=0, column=0, pady=30, padx=30)

yt_logo = PhotoImage(file='yt.png')
yt_logo = yt_logo.subsample(2, 2)
ytlabel = Label(frame1, image=yt_logo)
ytlabel.grid(row=0, column=0, pady=18)

# <-- Start video / Playlist
frame2 = LabelFrame(frame1, text='DOWNLOAD', font=('Montserrat', 13, 'bold'))
frame2.grid(row=1, column=0, pady=30)

radioImage = PhotoImage(file='video.png')
check=IntVar()
videobtn = Radiobutton(frame2, image=radioImage, text='  Single Video', compound=LEFT, variable=check, value=1, font=('Montserrat', 12, 'bold'))
videobtn.grid(row=0, column=0, padx=20, pady=20)

playlistImage = PhotoImage(file='playlist.png')
playlistbtn = Radiobutton(frame2, image=playlistImage, text='  Playlist', compound=LEFT, variable=check, value=2, font=('Montserrat', 12, 'bold'))
playlistbtn.grid(row=0, column=1, padx=20, pady=20)
# end video / playlist --->


link_label = Label(frame1, text="Enter Download Url : ", font=('Courgette', 13))
link_label.grid(row=2, column=0, padx=10, pady=5)

# <-- start link field
text = StringVar()
link_field = Entry(frame1, width=40, font=('Courgette', 13), justify = CENTER, textvariable=text, fg='gray')
link_field.grid(row=3, column=0, padx=10, pady=10)
text.set('Enter URL')

def click(event):
    link_field.delete(0, END)
    link_field.config(fg='black')
link_field.bind('<Button-1>', click)
# end link field -->

path_label = Label(frame1, text="Select Path For Download", font=('Courgette', 12))
path_label.grid(row=4, column=0, padx=10, pady=15)
select_btn =  Button(frame1, text="Select Path", bg='dodger blue',font=('Montserrat', 11, 'bold'), fg='#fff', command=select_path)
select_btn.grid(row=5, column=0, padx=10, pady=10)

download_btn = Button(frame1, text="Download File",bg='SpringGreen4',font=('Montserrat', 11, 'bold'), fg='#fff', command=download)
download_btn.grid(row=6, column=0, padx=10, pady=10)


screen.mainloop()

