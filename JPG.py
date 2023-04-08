import os
import exifread
import time

# Set the root directory containing the photos
root_dir = 'Directory/to/images'
no_date = 0
last_date = 0
# Loop through all the files and directories in the root directory
for root, dirs, files in os.walk(root_dir):
    for filename in files:
        if filename.endswith('.jpg'):  # Only process JPEG files
            filepath = os.path.join(root, filename)
            with open(filepath, 'rb') as f:
                tags = exifread.process_file(f)
                if 'EXIF DateTimeOriginal' in tags:
                    # Get the 'Date Taken' value from the EXIF data
                    date_taken = str(tags['EXIF DateTimeOriginal'])
                    # Convert the date string to a Unix timestamp
                    timestamp = time.mktime(time.strptime(date_taken, '%Y:%m:%d %H:%M:%S'))
                    # Set the 'Date Modified' and 'Date Created' values to the 'Date Taken' value
                    os.utime(filepath, (timestamp, timestamp))
                    last_date = timestamp
                    print(f"Changed 'Date Modified' and 'Date Created' of {filename} to '{date_taken}'")
                else:
                    print(f"No 'Date Taken' found for {filename}")
                    os.utime(filepath, (last_date, last_date))
                    no_date += 1
print('nodate = {no_date}')