from transcriber import Transcriber
from ytmp3 import YTtoMP3

# Path to the file containing the YouTube URLs
urls_file = '/Users/sam/Desktop/cloudflarehacky/videos.txt'

# Initialize Transcriber and YTtoMP3
trans = Transcriber()
ytmp3 = YTtoMP3()

# Open the file and process each URL
with open(urls_file, 'r') as file:
    for line in file:
        video_url = line.strip()  # Strip any trailing newlines or spaces
        if not video_url:
            continue  # Skip empty lines
        
        try:
            print(f"Processing video: {video_url}")
            
            # Download the MP3 from the YouTube URL
            mp3 = ytmp3.download_youtube_mp3(video_url)
            
            # Transcribe the downloaded MP3
            trans.transcribe(mp3)
            
            print(f"Finished processing {video_url}")
        
        except Exception as e:
            print(f"Error processing {video_url}: {e}")