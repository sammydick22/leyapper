import os
import yt_dlp

class YTtoMP3:
    def __init__(self):
        self.output_folder = None

    def ensure_mp3s_folder(self):
        # Create a 'mp3s' folder in the same directory as the script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.output_folder = os.path.join(script_dir, 'mp3s')
        os.makedirs(self.output_folder, exist_ok=True)
        return self.output_folder

    def download_youtube_mp3(self, url):
        if not self.output_folder:
            self.ensure_mp3s_folder()

        # Placeholder for the output path, will be set in the hook
        output_file = []

        def ydl_hook(d):
            if d['status'] == 'finished':
                # Replace .webm with .mp3 in the final filename
                output_file.append(d['filename'].replace('.webm', '.mp3'))

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            # Ensure the output template always uses .mp3 extension
            'outtmpl': os.path.join(self.output_folder, '%(title)s.%(ext)s'),
            'verbose': True,
            'progress_hooks': [ydl_hook],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([url])
                print("Download complete!")
            except Exception as e:
                print(f"An error occurred: {str(e)}")

        # Return the path to the .mp3 file
        return output_file[0] if output_file else None

    def run(self, url_file_path):
        with open(url_file_path, 'r') as file:
            urls = file.readlines()
            for url in urls:
                url = url.strip()  # Remove leading/trailing whitespaces and newlines
                if url:  # Check if the URL is not empty
                    output_path = self.download_youtube_mp3(url)
                    if output_path:
                        print(f"Downloaded and saved to: {output_path}")
                    else:
                        print(f"Failed to download: {url}")