# How it works

1. Create a folder in your Google Drive and create a sharing link with edit permissions.
2. Share this link with people on the event (e.g. print a QR code)
3. Everyone can take a photo on their own phone and upload it to the shared folder.
4. The script downloads photos from the shared folder and shows them in a slideshow in random order.
5. It keeps checking the folder and when a new picture is uploaded to the shared folder, it's downloaded locally and shown for 20 seconds. Then the slideshow continues.

# Using Google Forms

Uploading photos directly to the shared Google Drive folder has the following drawbacks:
- By default, uploading to Google Drive may be restricted to WiFi connection. When people have just mobile internet, they have to force the upload.
- Anyone can remove any photo in the shared folder.

You can create a Google Form with just a single "File upload" question. You can restrict the file type to "Images". There's a "View folder" link in the form editor which redirects you to the Google Drive folder which id you need to set to the `folder_id` variable in the `photo_corner.py` script.

This way, users can only upload their photos and it works well also on a mobile internet.

# Setup

1. Install python libs: `pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib pillow schedule`
2. Edit the script and change the `folder_id = 'YOUR_GOOGLE_DRIVE_FOLDER_ID'`
3. Log into your Google Cloud console, create a service with OAuth and download the credentials json into `credentials.json`
