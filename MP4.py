import os
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
import datetime


# Set the root directory containing the videos
root_dir = 'Directory/to/videos'
error = 0
no_date = 0
def makePrintable(data, charset='utf-8'):
    if isinstance(data, datetime.datetime):
        return str(data)
    try:
        # Try to decode the data as a byte string
        return str(data, charset)
    except (UnicodeDecodeError, TypeError):
        # If decoding fails, return a printable representation of the data
        return repr(data)
    
for root, dirs, files in os.walk(root_dir):
    for filename in files:
        if filename.lower().endswith('.mp4'):  # Only process MP4 files
            filepath = os.path.join(root, filename)
            try:
                # Use Hachoir library to extract metadata from the file
                parser = createParser(filepath)
                metadata = extractMetadata(parser)
                # Get the 'Media Create Date' value from the metadata
                create_date = metadata.get('creation_date', None)
                if create_date and create_date.year >= 2000:
                    # Convert the 'Media Create Date' value to a datetime object
                    date_str = makePrintable(create_date, metadata.get('charset', 'utf-8'))
                    date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                    # Convert the datetime object to a UTC timestamp value
                    timestamp = int(date_obj.timestamp())
                    # Set the 'Date Modified' and 'Date Created' values to the timestamp value
                    os.utime(filepath, (timestamp, timestamp))
                    # Get the file's current creation time
                    creation_time = os.stat(filepath).st_ctime_ns
                    # Set the file's creation time to the timestamp value
                    os.utime(filepath, (creation_time, timestamp))
                    print(f"Changed 'Date Modified' and 'Date Created' of {filename} to '{date_str}'")
                elif not create_date:
                    print(f"No 'Media Create Date' found for {filename}")
                    no_date += 1
                else:
                    print(f"Skipping file {filename} with date before year 2000")
            except ValueError as e:
                print(f"File format not recognized: {filename}")
                error += 1
print(f'no_date = {no_date} error = {error}')