import cv2
import tkinter as tk
from PIL import Image, ImageTk
import threading
import time
import os
from datetime import datetime
from tkinter import simpledialog, messagebox
import subprocess
import atexit

HD_720 = 1   #Select 1 for 720P and 0 for 480P
if HD_720 == 1:
    vid_height, vid_width = 960, 1280
elif HD_720 == 0:
    vid_height, vid_width = 480, 640

class WebcamApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Webcam Capture to Video")
        self.root.geometry("470x550")  # Set the fixed size of the window to 500x500 pixels

        self.interval = tk.IntVar(value=1000)  # Default to 1000ms = 1 second
        self.capturing = False
        self.paused = False
        self.fps = 30  # 30 frames per second
        self.video_file = None
        self.webcam = None  # Webcam will be selected by user
        self.video_folder = './output_videos/'
        self.start_time = None  # Store the start time of the recording
        self.elapsed_time = 0  # Store the elapsed time
        self.video_file_path = None  # Store the path of the saved video file

        # Create directories if they don't exist
        os.makedirs(self.video_folder, exist_ok=True)

        # Register exit handler to cleanup video file if app closes unexpectedly
        atexit.register(self.cleanup)

        self.setup_gui()

    def setup_gui(self):
        # Label and Entry for interval
        tk.Label(self.root, text="Capture Interval (milliseconds):").pack(pady=5)
        self.interval_entry = tk.Entry(self.root, textvariable=self.interval)
        self.interval_entry.pack(pady=5)

        # Button to select camera device
        self.select_camera_button = tk.Button(self.root, text="Select Camera", command=self.select_camera)
        self.select_camera_button.pack(pady=5)

        # Start, Stop, and Pause buttons
        self.start_button = tk.Button(self.root, text="Start", command=self.start_capture, state=tk.DISABLED)
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_capture, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

        self.pause_button = tk.Button(self.root, text="Pause", command=self.toggle_pause, state=tk.DISABLED)
        self.pause_button.pack(pady=5)

        # Frame to hold the video label (500x375 size)
        self.video_frame = tk.Frame(self.root, width=400, height=300)
        self.video_frame.pack(pady=5)
        
        self.video_label = tk.Label(self.video_frame)
        self.video_label.pack(fill=tk.BOTH, expand=True)

        # Label to show elapsed time at the bottom
        self.elapsed_time_label = tk.Label(self.root, text="Elapsed Time: 00:00")
        self.elapsed_time_label.pack(side=tk.BOTTOM, pady=5)

    def select_camera(self):
        camera_id = simpledialog.askinteger("Input", "Enter camera device ID (0 for default, 1 for external, etc.):", minvalue=0)
        if camera_id is not None:
            self.webcam = cv2.VideoCapture(camera_id)
            if not self.webcam.isOpened():
                messagebox.showerror("Error", f"Cannot access camera with device ID {camera_id}")
                self.webcam = None
            else:
                messagebox.showinfo("Success", f"Camera with device ID {camera_id} selected.")
                self.start_button.config(state=tk.NORMAL)

    def start_capture(self):
        if self.webcam is None:
            messagebox.showerror("Error", "Please select a camera first.")
            return

        interval_value = self.interval.get()
        if interval_value <= 0:
            messagebox.showerror("Error", "Interval must be greater than 0")
            return

        self.start_time = time.time()
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        self.video_file_path = os.path.join(self.video_folder, f'video_{timestamp}.mp4')

        frame_width = int(self.webcam.get(3))
        frame_height = int(self.webcam.get(4))

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')

        new_width, new_height = vid_width, vid_height
        self.video_file = cv2.VideoWriter(self.video_file_path, fourcc, self.fps, (new_width, new_height))

        self.capturing = True
        self.paused = False
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.NORMAL)
        threading.Thread(target=self.capture_video, daemon=True).start()
        threading.Thread(target=self.update_elapsed_time, daemon=True).start()

    def capture_video(self):
        while self.capturing:
            if not self.paused:
                ret, frame = self.webcam.read()
                if ret:
                    frame = cv2.resize(frame, (vid_width, vid_height))

                    current_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

                    font = cv2.FONT_HERSHEY_SIMPLEX
                    if HD_720 == 1:
                        cv2.putText(frame, current_time, (30, 50), font, 2, (255, 255, 255), 3, cv2.LINE_AA) 
                    elif HD_720 == 0:
                        cv2.putText(frame, current_time, (10, 25), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
                        

                    self.video_file.write(frame)

                    # Resize the frame to fit into the video display area (500x375)
                    resized_frame = cv2.resize(frame, (400, 300))

                    cv2_image = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
                    img = Image.fromarray(cv2_image)
                    imgtk = ImageTk.PhotoImage(image=img)
                    self.video_label.imgtk = imgtk
                    self.video_label.configure(image=imgtk)

                    time.sleep(self.interval.get() / 1000.0)
            else:
                time.sleep(0.1)  # Small delay to prevent busy waiting when paused

    def update_elapsed_time(self):
        while self.capturing:
            if not self.paused:
                self.elapsed_time = int(time.time() - self.start_time)
                minutes = self.elapsed_time // 60
                seconds = self.elapsed_time % 60
                self.elapsed_time_label.config(text=f"Elapsed Time: {minutes:02}:{seconds:02}")
            time.sleep(1)

    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            self.pause_button.config(text="Resume")
        else:
            self.pause_button.config(text="Pause")
            self.start_time = time.time() - self.elapsed_time  # Adjust start time when resuming

    def stop_capture(self):
        self.capturing = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.DISABLED)

        if self.video_file:
            # Release the video writer before compressing
            self.video_file.release()

            # Get the path of the saved video file (from self.video_file_path)
            if self.video_file_path:
                # Define the compressed output file path (e.g., adding "_compressed" to the filename)
                compressed_video_path = os.path.splitext(self.video_file_path)[0] + "_compressed.mp4"

                # Compress the video using FFmpeg
                self.compress_video(self.video_file_path, compressed_video_path)

                # After compression, delete the original file
                os.remove(self.video_file_path)

                messagebox.showinfo("Success", f"Video capture stopped, compressed, and saved to {compressed_video_path}.")
            else:
                messagebox.showerror("Error", "No video file was created.")

    def compress_video(self, input_file, output_file, scale_factor=1, crf=23, preset="medium"):
        try:
            # Get original video dimensions
            probe = subprocess.run(
                ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", input_file],
                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True
            )
            width, height = map(int, probe.stdout.strip().split(','))

            # Calculate new dimensions while maintaining aspect ratio
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)

            # Ensure dimensions are divisible by 2 (required by most codecs)
            new_width -= new_width % 2
            new_height -= new_height % 2

            # FFmpeg command for compression with scaling
            command = [
                "ffmpeg", "-i", input_file,
                "-vf", f"scale={new_width}:{new_height}",
                "-vcodec", "libx264", "-crf", str(crf), "-preset", preset,
                "-acodec", "aac", "-b:a", "128k", "-strict", "experimental",
                output_file
            ]

            # Run the command
            subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"Compressed: {input_file} -> {output_file} (Resolution: {new_width}x{new_height})")
        except subprocess.CalledProcessError as e:
            print(f"Error compressing {input_file}: {e}")
        except Exception as e:
            print(f"Unexpected error with {input_file}: {e}")

    def cleanup(self):
        """Ensure the video file is closed properly before exiting."""
        if self.video_file:
            self.video_file.release()

        if self.webcam:
            self.webcam.release()

    def close(self):
        self.capturing = False
        self.cleanup()

# Create the main window
root = tk.Tk()
app = WebcamApp(root)

# Run the GUI
root.mainloop()
