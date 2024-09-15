import cv2
import numpy as np
from PIL import ImageGrab, ImageTk, Image as PilImage
from tkinter import *
import pyaudio
import wave
import threading
from moviepy.editor import VideoFileClip, AudioFileClip

# Parameters for audio recording
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
AUDIO_OUTPUT_FILE = "output_audio.wav"

# Parameters for video recording
VIDEO_OUTPUT_FILE = "screen_recorded.avi"
FINAL_OUTPUT_FILE = "final_output.mp4"
FPS = 20.0

# Function to record audio
def record_audio():
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Recording audio...")

    frames = []

    while screen_recording:  # Keep recording audio until the screen recording stops
        data = stream.read(CHUNK)
        frames.append(data)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the recorded audio
    wf = wave.open(AUDIO_OUTPUT_FILE, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

# Function to record the screen
def screen_record():
    global screen_recording
    screen_recording = True
    
    image = ImageGrab.grab()  # Grabbing the screen
    img_arr = np.array(image)  # Converting to numpy array
    shape = img_arr.shape  # Getting shape of the captured screen

    # Create a video writer
    screen_cap_writer = cv2.VideoWriter(VIDEO_OUTPUT_FILE, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), FPS, (shape[1], shape[0]))

    print("Recording screen...")
    
    while screen_recording:
        image = ImageGrab.grab()  # Capture screen
        img_np_arr = np.array(image)  # Convert to numpy array
        final_img = cv2.cvtColor(img_np_arr, cv2.COLOR_RGB2BGR)  # Convert RGB to BGR for OpenCV

        # Write to the video file
        screen_cap_writer.write(final_img)

        # Optional: To view your screen recording simultaneously in a separate window
        cv2.imshow("Screen Recording", final_img)

        # Stop and exit screen recording when 'e' is pressed
        if cv2.waitKey(1) == ord('e'):
            screen_recording = False

    # Release the video writer and close windows
    screen_cap_writer.release()
    cv2.destroyAllWindows()
    
    # Combine video and audio after recording stops
    combine_audio_video(VIDEO_OUTPUT_FILE, AUDIO_OUTPUT_FILE)

# Function to combine audio and video using moviepy
def combine_audio_video(video_file, audio_file, output_file=FINAL_OUTPUT_FILE):
    video_clip = VideoFileClip(video_file)
    audio_clip = AudioFileClip(audio_file)
    
    final_clip = video_clip.set_audio(audio_clip)
    final_clip.write_videofile(output_file, codec="libx264")

# Function to start both screen and audio recording simultaneously
def start_recording():
    audio_thread = threading.Thread(target=record_audio)
    screen_thread = threading.Thread(target=screen_record)

    # Start both audio and screen recording threads
    audio_thread.start()
    screen_thread.start()

    # Wait for both threads to finish
    audio_thread.join()
    screen_thread.join()

# Define the user interface for Screen Recorder using tkinter
screen_recorder = Tk()
screen_recorder.geometry("340x340")
screen_recorder.title("Dipraj's Screen Recorder")

# Set custom styles to simulate CSS (you can change these as you want)
screen_recorder.configure(bg="#ffffff")  # Background color

# Load the image using the renamed PilImage to avoid conflicts
try:
    img = PilImage.open(r"C:\Users\dipra\OneDrive\Documents\Python code\Screen Recoder\Shiv.JPG")
except FileNotFoundError:
    print("Image file not found. Please check the path.")
    exit()

# Convert the image to a PhotoImage for tkinter
bg_img = ImageTk.PhotoImage(img)

# Show image using label
label1 = Label(screen_recorder, image=bg_img, bd=0)
label1.pack()

# Create and place the components with custom styling
title_label = Label(screen_recorder, text="Dipraj's Screen Recorder", font=("Helvetica", 16, "bold"), bg="#02b9e5", fg="#ffffff", padx=10, pady=10)
title_label.place(relx=0.5, rely=0.1, anchor=CENTER)

info_label = Label(screen_recorder, text="Press 'e' to exit recording", font=("Helvetica", 10), bg="#02b9e5", fg="#ffffff", padx=5, pady=5)
info_label.place(relx=0.5, rely=0.3, anchor=CENTER)

# Define the button that starts screen recording with some styling
screen_button = Button(screen_recorder, text="Record Screen & Audio", command=start_recording, bg="#0a8dff", fg="#ffffff", font=("Helvetica", 12), padx=10, pady=5, relief=RAISED)
screen_button.place(relx=0.5, rely=0.6, anchor=CENTER)

screen_recorder.mainloop()
