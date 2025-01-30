from tkinter import *
from PIL import Image, ImageTk
import sounddevice as sd
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

recording = False
myrecording = None
fs = 48000

def toggle_recording():
    global recording, myrecording
    if recording:
        sd.stop()
        recording = False
        # save as FLAC file
        sf.write('my_Audio.flac', myrecording, fs)
        update_graph()
    else:
        recording = True
        duration = 60  # seconds
        myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2, dtype='float64')

def update_graph():
    fig, ax = plt.subplots()
    ax.plot(myrecording)
    ax.set_title('Audio Waveform')
    ax.set_xlabel('Samples')
    ax.set_ylabel('Amplitude')
    canvas = FigureCanvasTkAgg(fig, master=master)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=True)

def minimize_window():
    print("Minimize button clicked")  # Debugging statement
    master.iconify()

def close_window():
    master.destroy()

def start_move(event):
    global x, y
    x = event.x
    y = event.y

def stop_move(event):
    global x, y
    x = None
    y = None

def on_motion(event):
    global x, y
    deltax = event.x - x
    deltay = event.y - y
    new_x = master.winfo_x() + deltax
    new_y = master.winfo_y() + deltay
    master.geometry(f"+{new_x}+{new_y}")

master = Tk()
master.geometry("300x200")
master.configure(bg='#2C3E50')
master.overrideredirect(True)  # Remove the default title bar

# Create a custom title bar
title_bar = Frame(master, bg='#2C3E50', relief='raised', bd=0)
title_bar.pack(side=TOP, fill=X)

# Bind events to the title bar for dragging
title_bar.bind("<ButtonPress-1>", start_move)
title_bar.bind("<ButtonRelease-1>", stop_move)
title_bar.bind("<B1-Motion>", on_motion)

# Add title label
title_label = Label(title_bar, text="Audio Recorder", bg='#2C3E50', fg='white', font=("Helvetica", 12))
title_label.pack(side=LEFT, padx=10)

# Add minimize button
minimize_button = Button(title_bar, text='-', command=minimize_window, bg='#2C3E50', fg='white', bd=0)
minimize_button.pack(side=RIGHT, padx=5)

# Add close button
close_button = Button(title_bar, text='x', command=close_window, bg='#2C3E50', fg='white', bd=0)
close_button.pack(side=RIGHT)

# Create a canvas for the button with a white outline circle
canvas = Canvas(master, width=70, height=70, bg='#2C3E50', highlightthickness=0)
canvas.pack(pady=20)
canvas.create_oval(5, 5, 65, 65, outline='white', width=2)

# Load and resize the microphone icon
mic_image = Image.open('images/microphone.png')
mic_image = mic_image.resize((50, 50), Image.LANCZOS)  # Resize to 50x50 pixels
mic_icon = ImageTk.PhotoImage(mic_image)

# Place the button in the middle of the canvas
b_toggle = Button(canvas, image=mic_icon, command=toggle_recording, bg="#2C3E50", bd=0, highlightthickness=0)
b_toggle.place(x=10, y=10)

mainloop()