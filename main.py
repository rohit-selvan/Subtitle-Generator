import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy.editor import AudioFileClip
import speech_recognition as sr
import os

class SubtitleGenerator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("YouTube Subtitle Generator")
        self.geometry("600x300")
        self.configure(bg="#f0f4f8")  # Soft pastel background
        self.create_widgets()

    def create_widgets(self):
        # Title
        tk.Label(self, text="YouTube Subtitle Generator", font=("Verdana", 20, "bold"), bg="#f0f4f8", fg="#2c3e50").pack(pady=20)
        
        # Select Video Button
        tk.Button(self, text="Select Video File", command=self.select_file, font=("Verdana", 14), bg="#3498db", fg="white", width=20).pack(pady=20)
        
        # Status Label
        self.status_label = tk.Label(self, text="", font=("Verdana", 12), bg="#f0f4f8", fg="#2c3e50")
        self.status_label.pack(pady=10)

    def select_file(self):
        file_path = filedialog.askopenfilename(title="Select a Video File", filetypes=[("Video Files", "*.mp4 *.mkv *.avi *.mov")])
        if file_path:
            self.generate_subtitles(file_path)

    def generate_subtitles(self, file_path):
        self.status_label.config(text="Processing... Please wait.")
        self.update()
        
        try:
            # Extract audio from video
            audio_path = "temp_audio.wav"
            video = AudioFileClip(file_path)
            video.write_audiofile(audio_path, codec="pcm_s16le")
            
            # Recognize speech from audio
            recognizer = sr.Recognizer()
            with sr.AudioFile(audio_path) as source:
                audio_data = recognizer.record(source)
                subtitles = recognizer.recognize_google(audio_data)
            
            # Save subtitles to .srt file
            srt_path = os.path.splitext(file_path)[0] + ".srt"
            with open(srt_path, "w") as srt_file:
                srt_file.write("1\n00:00:00,000 --> 00:00:30,000\n" + subtitles + "\n")
            
            self.status_label.config(text=f"Subtitles generated: {srt_path}")
            messagebox.showinfo("Success", f"Subtitles saved to {srt_path}")
            
            # Clean up temporary audio file
            os.remove(audio_path)
        except Exception as e:
            self.status_label.config(text="An error occurred.")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    app = SubtitleGenerator()
    app.mainloop()
