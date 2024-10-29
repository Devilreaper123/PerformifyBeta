from django.core.management.base import BaseCommand
from videoapp.models import Video
import json

class Command(BaseCommand):
    help = 'Imports videos from a JSON file into the database'

    def handle(self, *args, **kwargs):
        with open('./videoapp/beta2.json', 'r', encoding='utf-8') as f:
            video_data = json.load(f)

        for video in video_data:
            video_url = video['url']

            # Check if the URL is in the shortened "youtu.be" format and convert it to the embed format
            if "youtu.be" in video_url:
                video_id = video_url.split('/')[-1].split('?')[0]  # Extract the video ID from the youtu.be link
                video_url = f"https://www.youtube.com/watch/{video_id}"

            video_obj = Video(
                title=video['title'],
                artist=video['artist'],
                description=video['description'],
                tags=", ".join(video['tags']),
                artist_description=video['artist_description'],
                url=video_url  # Use the converted embed URL
            )
            video_obj.save()

        self.stdout.write(self.style.SUCCESS('Successfully imported videos from JSON'))
