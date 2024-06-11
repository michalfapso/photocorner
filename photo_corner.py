from __future__ import print_function
import os
import time
import pickle
import io
from PIL import Image, ImageTk
import tkinter as tk
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import threading
import schedule
import random

# Set up Google Drive API
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
folder_id = 'YOUR_GOOGLE_DRIVE_FOLDER_ID'  # Replace with your folder ID
downloaded_photos = set()
new_photo_display_event = threading.Event()

def authenticate_google_drive():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build('drive', 'v3', credentials=creds)

def download_photos(service):
    print('download_photos()')
    global downloaded_photos
    results = service.files().list(
        q=f"'{folder_id}' in parents",
        pageSize=100, fields="files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        if not os.path.exists('photos'):
            os.makedirs('photos')
        for item in items:
            if item['name'] not in downloaded_photos:
                request = service.files().get_media(fileId=item['id'])
                fh = io.FileIO(os.path.join('photos', item['name']), 'wb')
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                print(f"Downloaded {item['name']}")
                downloaded_photos.add(item['name'])
                new_photo_display_event.set()

def load_downloaded_photos():
    global downloaded_photos
    if os.path.exists('photos'):
        downloaded_photos = set(os.listdir('photos'))
    else:
        os.makedirs('photos')

def display_slideshow():
    root = tk.Tk()
    root.title("Wedding Photo Slideshow")
    root.attributes('-fullscreen', True)
    root.configure(bg='black')

    lbl = tk.Label(root)
    lbl.pack(expand=True)

    def update_image(image_path):
        print('update_image() image_path:', image_path)
        img = Image.open(image_path)
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        img_ratio = img.width / img.height
        screen_ratio = screen_width / screen_height

        if img_ratio > screen_ratio:
            new_width = screen_width
            new_height = int(screen_width / img_ratio)
        else:
            new_height = screen_height
            new_width = int(screen_height * img_ratio)

        img = img.resize((new_width, new_height), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        lbl.config(image=img)
        lbl.image = img

    def slideshow():
        while True:
            photos = sorted(os.listdir('photos'))
            random.shuffle(photos)
            if photos:
                for photo in photos:
                    if not new_photo_display_event.is_set():
                        update_image(os.path.join('photos', photo))
                        time.sleep(5)  # Display each photo for 5 seconds
                    else:
                        new_photo_display_event.wait()
                        new_photo_display_event.clear()
                        show_latest_photo()
                        time.sleep(20)  # Display each photo for 5 seconds
                        break

    def show_latest_photo():
        print('show_latest_photo()')
        photos = sorted(os.listdir('photos'), key=lambda x: os.path.getmtime(os.path.join('photos', x)), reverse=True)
        if photos:
            update_image(os.path.join('photos', photos[0]))
        #root.after(30000, start_slideshow)

    def start_slideshow():
        slideshow_thread = threading.Thread(target=slideshow)
        slideshow_thread.start()

    start_slideshow()
    root.mainloop()

def check_for_new_photos(service):
    download_photos(service)

if __name__ == '__main__':
    import threading
    service = authenticate_google_drive()
    load_downloaded_photos()
    download_photos(service)

    # Schedule the check for new photos every minute
    schedule.every(10).seconds.do(check_for_new_photos, service)

    # Run the slideshow
    slideshow_thread = threading.Thread(target=display_slideshow)
    slideshow_thread.start()

    # Run the schedule in the main thread
    while True:
        schedule.run_pending()
        time.sleep(1)

