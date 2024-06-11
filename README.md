# How it works

1. Create a folder in your Google Drive and create a sharing link with edit permissions.
2. Share this link with people on the event (e.g. print a QR code)
3. Everyone can take a photo on their own phone and upload it to the shared folder.
4. The script downloads photos from the shared folder and shows them in a slideshow in random order.
5. It keeps checking the folder and when a new picture is uploaded there, it's downloaded locally and shown for 20 seconds. Then the slideshow continues.

# Setup
1. Install python libs: `pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib pillow schedule`
2. Edit the script and change the `folder_id = 'YOUR_GOOGLE_DRIVE_FOLDER_ID'`
3. Log into your Google Cloud console, create a service with OAuth and download the credentials json into `credentials.json`
